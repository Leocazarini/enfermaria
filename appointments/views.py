from django.shortcuts import render
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .models import *
from patients.models import Student, Employee, Visitor
from patients.views import search_student, search_employee, search_visitor
from controller.crud import create_objects, create_info, get_object, get_info_by_patient, update_info, update_visitor_info
from django.contrib.auth.decorators import login_required
import logging
import json



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
        visitor = search_visitor(name, email)
        

        if visitor is None:
            logger.error('Visitor not found')
            return render(request, 'search_visitor.html', {'error_message': 'Visitante não encontrado.'})

        return render(request, 'ap_visitor.html', {'visitor': visitor}) 
              
    return render(request, 'ap_visitor.html')
    



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


@csrf_exempt
def visitor_record(request):
    if request.method == 'POST':
        try:
            # Lendo o JSON da requisição
            data = json.loads(request.body)
            logger.debug('Data: %s', data)

            # Extraindo os campos do JSON
            visitor_id = data.get('visitor_id')
            visitor_name = data.get('visitor_name')
            visitor_age = data.get('visitor_age')
            visitor_email = data.get('visitor_email')
            visitor_gender = data.get('visitor_gender')
            allergies = data.get('allergies')
            visitor_relationship = data.get('visitor_relationship')
            patient_notes = data.get('patient_notes')
            infirmary = data.get('infirmary')
            nurse = data.get('nurse')
            reason = data.get('reason')
            treatment = data.get('treatment')
            notes = data.get('notes')
            revaluation = data.get('revaluation')
            date = data.get('date')


            logger.debug('Visitor ID: %s', visitor_id)
            logger.debug('Visitor Name: %s', visitor_name)
            logger.debug('Visitor Age: %s', visitor_age)
            logger.debug('Visitor Email: %s', visitor_email)
            logger.debug('Visitor Gender: %s', visitor_gender)
            logger.debug('Allergies: %s', allergies)
            logger.debug('Visitor Relationship: %s', visitor_relationship)
            logger.debug('Patient Notes: %s', patient_notes)
            logger.debug('Infirmary: %s', infirmary)
            logger.debug('Nurse: %s', nurse)
            logger.debug('Reason: %s', reason)
            logger.debug('Treatment: %s', treatment)
            logger.debug('Notes: %s', notes)
            logger.debug('Revaluation: %s', revaluation)



            # Montando dicionário de dados do visitante
            visitor_data_dict = {
                'visitor_id': visitor_id,
                'visitor_name': visitor_name,
                'visitor_age': visitor_age,
                'visitor_email': visitor_email,
                'visitor_gender': visitor_gender,
                'allergies': allergies,
                'visitor_relationship': visitor_relationship,
                'patient_notes': patient_notes
            }

            # Obtendo o visitante (lista de resultados)
            visitors = get_object(Visitor, name=visitor_name, email=visitor_email)

            if visitors and len(visitors) > 0:
                visitor = visitors[0]
                visitor_dict = model_to_dict(visitor)


                db_allergies = visitor_dict['allergies']
                db_patient_notes = visitor_dict['patient_notes']
            logger.debug('Visitors: %s', visitor)

            logger.debug('Visitor: %s', visitor)
            logger.debug('Visitor Allergies: %s', db_allergies) 
            logger.debug('Visitor Patient Notes: %s', db_patient_notes)

            if visitor:
                logger.debug('Visitor: %s', visitor)
                if isinstance(visitor, Visitor):  # Verifica se o visitante é um objeto do modelo Visitor
                    logger.debug('Visitor already exists')

                    # Verificar se há diferenças nos dados para atualizar
                    if allergies != db_allergies or patient_notes != db_patient_notes:
                        update_visitor_info(Visitor, visitor_email, allergies, patient_notes)
                        logger.debug('Data updated successfully')
                    else:
                        logger.debug('No update needed for visitor info')
                else:
                    logger.error('First item in visitors list is not a valid Visitor object.')
                    return JsonResponse({'error': 'Invalid visitor object'}, status=400)
            else:
                # Se não houver visitante, crie um novo
                visitor_data_list = [visitor_data_dict]
                create_objects(Visitor, visitor_data_list)

            # Montando dicionário de dados do atendimento
            appointment_data_dict = {
                'visitor_id': visitor_id,
                'infirmary': infirmary,
                'nurse': nurse,
                'reason': reason,
                'treatment': treatment,
                'notes': notes,
                'revaluation': revaluation,
                'date': date
            }

            # Criar lista e gravar os dados do atendimento
            appointment_data_list = [appointment_data_dict]
            response = create_objects(VisitorAppointment, appointment_data_list)
            logger.debug('Response: %s', response)

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
      

