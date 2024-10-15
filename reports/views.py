import logging
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator 
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from datetime import datetime, time
from patients.views import search_student, search_employee
from appointments.models import *
from controller.crud import get_appointment, get_all_appointments






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
        list_appointments.sort(key=lambda x: x['date'], reverse=True)

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
            return render(request, 'employee_search_record.html', {'error_message': 'Colaborador não encontrado.'}) 

        # Identifica o campo correto do ID
        identifier_field = 'employee_id' 

        # Obtém os dados dos atendimentos do paciente
        appointment = get_appointment(EmployeeAppointment, identifier_field, patient_id=employee['id'])

        logger.debug(f'Appointments found: {appointment}')

        list_appointments = list(appointment)
        list_appointments.sort(key=lambda x: x['date'], reverse=True)

        return render(request, 'employee_record.html', {'employee': employee, 'appointment': list_appointments})



@login_required
def reports(request):
    if request.method == 'GET':
        return render(request, 'reports.html')

    if request.method == 'POST':
        logger.debug('POST request received')

        date_begin = request.POST.get('date_begin')
        date_end = request.POST.get('date_end')
        infirmaries = request.POST.getlist('infirmaries')
        search_term = request.POST.get('search_term', '').strip()

        logger.debug(f'info: {date_begin}, {date_end}, {infirmaries}, {search_term}')

        # Validações
        errors = []
        if not date_begin:
            errors.append("Por favor, preencha a data de início.")
        if not date_end:
            errors.append("Por favor, preencha a data de fim.")
        if not infirmaries:
            errors.append("Por favor, selecione pelo menos uma enfermaria.")

        if errors:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'errors': errors}, status=400)
            else:
                for error in errors:
                    messages.error(request, error)
                return render(request, 'reports.html')

        # Conversão das datas
        date_begin = datetime.strptime(date_begin, '%Y-%m-%d')
        date_end = datetime.strptime(date_end, '%Y-%m-%d')
        date_end = datetime.combine(date_end.date(), time.max)  # Define a hora para 23:59:59.999999


         # Número de resultados por página
        RESULTS_PER_PAGE = 100 

        # Obtenção dos atendimentos
        all_appointments = get_all_appointments(date_begin, date_end, infirmaries, search_term)

        # Implementação da paginação
        paginator = Paginator(all_appointments, RESULTS_PER_PAGE)

        # Obtenha o número da página atual
        page_number = request.POST.get('page') or 1

        # Obtenha a página desejada
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'date_begin': date_begin,
            'date_end': date_end,
            'paginator': paginator,
            'search_term': search_term,
        }

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Renderiza o template parcial e retorna como HTML
            html = render_to_string('report_results_partial.html', context, request=request)
            return HttpResponse(html)
        else:
            return render(request, 'report_results.html', context)
    else:
        return render(request, 'reports.html')
