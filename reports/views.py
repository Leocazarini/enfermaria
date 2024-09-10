import logging
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from patients.views import search_student, search_employee
from appointments.models import StudentAppointment, EmployeeAppointment
from controller.crud import get_appointment





logger = logging.getLogger('reports.views')



def student_search(request):

    if request.method == 'GET':
        
        return render(request, 'student_search_record.html')
    

def student_record(request):
    if request.method == 'GET':
        
        name = request.GET.get('name', None)
        registry = request.GET.get('registry', None)
        
        if not name and not registry:
            logger.error('No name or registry provided')
            return JsonResponse({'status': 'error', 'message': 'Missing required fields: name or registry'}, status=400)
        
        # Busca o estudante
        student = search_student(name, registry)
    
        if student is None:
            logger.error('Student not found')
            return render(request, 'student_search_record.html', {'error_message': 'Estudante não encontrado.'}) 

        # Identifica o campo correto do ID
        identifier_field = 'student_id' 

        # Obtém os dados dos atendimentos do paciente
        appointment = get_appointment(StudentAppointment, identifier_field, patient_id=student['id'])

        logger.debug(f'Appointments found: {appointment}')

        list_appointments = list(appointment)

        return render(request, 'student_record.html', {'student': student, 'appointment': list_appointments})
        




        

def employee_search(request):

    if request.method == 'GET':
        return render(request, 'employee_search_record.html')
    

def employee_record(request):
    if request.method == 'GET':
        
        name = request.GET.get('name', None)
        registry = request.GET.get('registry', None)
        
        if not name and not registry:
            logger.error('No name or registry provided')
            return JsonResponse({'status': 'error', 'message': 'Missing required fields: name or registry'}, status=400)
        
        # Busca o estudante
        employee = search_employee(name, registry)
    
        if employee is None:
            logger.error('Employee not found')
            return render(request, 'employee_search_record.html', {'error_message': 'Estudante não encontrado.'}) 

        # Identifica o campo correto do ID
        identifier_field = 'employee_id' 

        # Obtém os dados dos atendimentos do paciente
        appointment = get_appointment(EmployeeAppointment, identifier_field, patient_id=employee['id'])

        logger.debug(f'Appointments found: {appointment}')

        list_appointments = list(appointment)

        return render(request, 'employee_record.html', {'employee': employee, 'appointment': list_appointments})