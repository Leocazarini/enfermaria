import logging
import json
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import *
from patients.models import Student, Employee, Visitor
from patients.views import search_student, search_employee, search_visitor, manage_visitor_data

from controller.crud import (create_objects, create_info, get_object, 
                             get_info_by_patient, update_info, update_visitor_info)




logger = logging.getLogger('appointments.views')




# Home view

@login_required
def home(request):
    if request.method == 'GET':

        return render(request, 'index.html')
    


def student_identify(request):
    if request.method == 'GET':
        return render(request, 'search_student.html')
    

def employee_identify(request):
    if request.method == 'GET':
        return render(request, 'search_employee.html')
    

def visitor_identify(request):
    if request.method == 'GET':
        return render(request, 'search_visitor.html')



        

# Appointments views

@login_required
def student_appointment(request):
    """
    View function for handling student appointment.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The HTTP response object.

    """
    if request.method == 'GET':
        name = request.GET.get('name', None)
        registry = request.GET.get('registry', None)
        if not name and not registry:
            logger.error('No name or registry provided')
            return  JsonResponse({'status': 'error', 'message': 'Missing required fields: name or registry'}, status=400)
        student = search_student(name, registry)
       
        if student is None:
            logger.error('Student not found')
            return render(request, 'search_student.html', {'error_message': 'Estudante não encontrado.'}) 

        return render(request, 'ap_student.html', {'student': student})





@login_required
def employee_appointment(request):
    if request.method == 'GET':
        name = request.GET.get('name', None)
        registry = request.GET.get('registry', None)
        employee = search_employee(name, registry)

        if employee is None:
            logger.error('Employee not found')
            return render(request, 'search_employee.html', {'error_message': 'Colaborador não encontrado.'})

        return render(request, 'ap_employee.html', {'employee': employee})

 
    


@login_required
def visitor_appointment(request):
    """
    View function for handling visitor appointments.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The HTTP response object.
    Raises:
        None
    """
    ...
    if request.method == 'GET':
        name = request.GET.get('name', None)
        email = request.GET.get('email', None)

        if not name and not email:
            return render(request, 'ap_visitor.html')

        visitor = search_visitor(name, email)
        

        if visitor is None:
            logger.error('Visitor not found')
            return render(request, 'search_visitor.html', {'error_message': 'Visitante não encontrado.'})

        return render(request, 'ap_visitor.html', {'visitor': visitor}) 
              
    
    



@csrf_exempt
def student_record(request):
    if request.method == 'POST':
        try:
            # Lendo o JSON da requisição
            data = json.loads(request.body)

            # Extraindo os campos do JSON
            student_id = data.get('student_id')
            allergies = data.get('allergies')
            patient_notes = data.get('patient_notes')
            infirmary = data.get('infirmary')
            nurse = data.get('nurse')
            current_class = data.get('current_class')
            date = data.get('date')
            reason = data.get('reason')
            treatment = data.get('treatment')
            notes = data.get('notes')
            revaluation = data.get('revaluation')
            contact_parents = data.get('contact_parents')

            # Desempacotando os valores da lista para os dados do aluno
            data_info_list = [
                student_id,
                allergies,
                patient_notes
            ]

            # Verificar e atualizar os dados do aluno se necessário
            info = get_info_by_patient(StudentInfo, student_id, 'student')
            logger.debug('Info: %s', info)
            if info:
                if allergies != info.allergies or patient_notes != info.patient_notes:
                    update_info(StudentInfo, student_id, 'student', allergies, patient_notes)
                    logger.debug('Data updated successfully: %s', data_info_list)
                else:
                    logger.debug('No update needed for student info')
            else:
                # Caso não exista informação prévia, crie-a
                create_info(StudentInfo, student_id, 'student', allergies, patient_notes)
                logger.debug('New student info created: %s', data_info_list)

            # Montando o dicionário para os dados de atendimento
            data_dict = {
                'student_id': student_id,
                'infirmary': infirmary,
                'nurse': nurse,
                'current_class': current_class,
                'date': date,
                'reason': reason,
                'treatment': treatment,
                'notes': notes,
                'revaluation': revaluation,
                'contact_parents': contact_parents
            }

            # Criar uma lista de dicionários para enviar para create_objects
            data_list = [data_dict]

            # Criar registro na tabela de atendimentos
            response = create_objects(StudentAppointment, data_list)
            logger.debug('Response: %s', response)

            # Retornar a resposta de sucesso ou erro
            return response

        except json.JSONDecodeError:
            logger.error('Failed to decode JSON', exc_info=True)
            return JsonResponse({'error': 'Falha ao decodificar JSON'}, status=400)
        except Exception as e:
            logger.error('An error occurred: %s', e, exc_info=True)
            return JsonResponse({'error': str(e)}, status=500)

    # Se a requisição não for POST, retornar um erro
    logger.error('Method not allowed')
    return JsonResponse({'error': 'Método não permitido'}, status=405)





@csrf_exempt
def employee_record(request):
    if request.method == 'POST':
        try:
            # Lendo o JSON da requisição
            data = json.loads(request.body)

            # Extraindo os campos do JSON
            employee_id = data.get('employee_id')
            allergies = data.get('allergies')
            patient_notes = data.get('patient_notes')
            infirmary = data.get('infirmary')
            nurse = data.get('nurse')
            date = data.get('date')
            reason = data.get('reason')
            treatment = data.get('treatment')
            notes = data.get('notes')
            revaluation = data.get('revaluation')

            # Desempacotando os valores da lista para os dados do funcionário
            data_info_list = [
                employee_id,
                allergies,
                patient_notes
            ]

            # Verificar e atualizar os dados do funcionário se necessário
            info = get_info_by_patient(EmployeeInfo, employee_id, 'employee')
            logger.debug('Info: %s', info)
            if info:
                if allergies != info.allergies or patient_notes != info.patient_notes:
                    update_info(EmployeeInfo, employee_id, 'employee', allergies, patient_notes)
                    logger.debug('Data updated successfully: %s', data_info_list)
                else:
                    logger.debug('No update needed for employee info')
            else:
                # Caso não exista informação prévia, crie-a
                create_info(EmployeeInfo, employee_id, 'employee', allergies, patient_notes)
                logger.debug('New employee info created: %s', data_info_list)

            # Montando o dicionário para os dados de atendimento
            data_dict = {
                'employee_id': employee_id,
                'infirmary': infirmary,
                'nurse': nurse,
                'date': date,
                'reason': reason,
                'treatment': treatment,
                'notes': notes,
                'revaluation': revaluation,
            }

            # Criar uma lista de dicionários para enviar para create_objects
            data_list = [data_dict]

            # Criar registro na tabela de atendimentos
            response = create_objects(EmployeeAppointment, data_list)
            logger.debug('Response: %s', response)

            # Retornar a resposta de sucesso ou erro
            return response

        except json.JSONDecodeError:
            logger.error('Failed to decode JSON', exc_info=True)
            return JsonResponse({'error': 'Falha ao decodificar JSON'}, status=400)
        except Exception as e:
            logger.error('An error occurred: %s', e, exc_info=True)
            return JsonResponse({'error': str(e)}, status=500)

    # Se a requisição não for POST, retornar um erro
    logger.error('Method not allowed')
    return JsonResponse({'error': 'Método não permitido'}, status=405)





def register_visitor_appointment(visitor, appointment_data):
    """
    Register a visitor appointment based on the provided data.
    
    Args:
        visitor: The visitor object (not just the ID) for whom the appointment is being registered.
        appointment_data (dict): The data for the appointment to be created.
    
    Returns:
        JsonResponse: Success or error response.
    """
    try:
        # Adicionar o objeto visitor à appointment_data
        appointment_data['visitor'] = visitor  # Aqui estamos passando a instância do visitante

        # Criar o registro do atendimento
        appointment_response = create_objects(VisitorAppointment, [appointment_data])

        if appointment_response.status_code != 201:
            logger.error(f"Error creating appointment: {appointment_response.content}")
            return JsonResponse({'status': 'error', 'message': 'Erro ao criar o atendimento'}, status=500)

        logger.info("Appointment created successfully.")
        return JsonResponse({'status': 'success', 'message': 'Atendimento salvo com sucesso!'}, status=201)

    except Exception as e:
        logger.error(f"Error registering appointment: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)




@csrf_exempt
def visitor_record(request):
    if request.method == 'POST':
        try:
            # Lendo o JSON da requisição
            data = json.loads(request.body)
            logger.debug('Data received: %s', data)

            # Extraindo os dados do visitante
            visitor_data = {
                'name': data.get('visitor_name'),
                'age': data.get('visitor_age'),
                'email': data.get('visitor_email'),
                'gender': data.get('visitor_gender'),
                'allergies': data.get('allergies'),
                'relationship': data.get('visitor_relationship'),
                'patient_notes': data.get('patient_notes'),
            }

            logger.debug('Visitor Data Extracted: %s', visitor_data)
            
            # Chamar a função para verificar e gerenciar o visitante
            visitor = manage_visitor_data(visitor_data)
            if not visitor:
                return JsonResponse({'status': 'error', 'message': 'Erro ao gerenciar os dados do visitante'}, status=500)

            # Dados do atendimento
            appointment_data = {
                'infirmary': data.get('infirmary'),
                'nurse': data.get('nurse'),
                'reason': data.get('reason'),
                'treatment': data.get('treatment'),
                'notes': data.get('notes'),
                'revaluation': data.get('revaluation'),
                'date': data.get('date'),
            }

            # Registrar o atendimento
            return register_visitor_appointment(visitor, appointment_data)

        except json.JSONDecodeError:
            logger.error('Failed to decode JSON', exc_info=True)
            return JsonResponse({'error': 'Falha ao decodificar JSON'}, status=400)
        except Exception as e:
            logger.error(f"An error occurred: {e}", exc_info=True)
            return JsonResponse({'error': str(e)}, status=500)

    # Se a requisição não for POST, retornar erro
    logger.error('Method not allowed')
    return JsonResponse({'error': 'Método não permitido'}, status=405)





      

