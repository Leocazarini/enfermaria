from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from urllib.parse import unquote
from appointments.models import StudentAppointment, EmployeeAppointment, VisitorAppointment
from .crud import (get_nurse_appointments_current_year, get_total_appointments_current_year, 
                   get_total_appointments_today, get_total_appointments_infirmary_current_year, 
                   get_total_appointments_infirmary_today)


@login_required
def index(request):
    if request.method == 'GET':
        selected_infirmary = request.COOKIES.get('infirmary')
        if selected_infirmary:
            selected_infirmary = unquote(selected_infirmary)
            selected_infirmary = selected_infirmary.strip()
            print(f"Selected infirmary after decoding: '{selected_infirmary}'")
        else:
            selected_infirmary = None  # Ou defina um valor padrão, se necessário

        nurse_appointments = get_nurse_appointments_current_year()
        total_appointments_year = get_total_appointments_current_year()
        total_appointments_today = get_total_appointments_today()
        total_appointments_infirmary_year = get_total_appointments_infirmary_current_year(selected_infirmary)
        total_appointments_infirmary_today = get_total_appointments_infirmary_today(selected_infirmary)

        full_name = request.user.first_name
        context = {
            'first_name': full_name,
            'nurse_appointments': nurse_appointments,
            'total_appointments_year': total_appointments_year,
            'total_appointments_today': total_appointments_today,
            'total_appointments_infirmary_year': total_appointments_infirmary_year,
            'total_appointments_infirmary_today': total_appointments_infirmary_today,
            'selected_infirmary': selected_infirmary,
        }
        return render(request, 'index.html', context)
    



def logout(request):
    if request.method == 'GET':
        return render(request, 'user/account/logout.html')


def get_user_info(request):
    if request.user.is_authenticated:
        full_name = request.user.first_name
        return JsonResponse({'first_name': full_name})
    else:
        return JsonResponse({'error': 'Usuário não autenticado'}, status=401)
    


def get_chart_data(request):
    # Agregar as contagens por enfermaria
    labels = ["Infantil", "Fundamental", "Ensino Médio", "Atendimento Externo"]
    infirmary_counts = {label: 0 for label in labels}

    # Agregar contagens do StudentAppointment
    student_counts = StudentAppointment.objects.values('infirmary').annotate(count=Count('id'))
    for item in student_counts:
        infirmary = item['infirmary']
        if infirmary in infirmary_counts:
            infirmary_counts[infirmary] += item['count']

    # Agregar contagens do EmployeeAppointment
    employee_counts = EmployeeAppointment.objects.values('infirmary').annotate(count=Count('id'))
    for item in employee_counts:
        infirmary = item['infirmary']
        if infirmary in infirmary_counts:
            infirmary_counts[infirmary] += item['count']

    # Agregar contagens do VisitorAppointment
    visitor_counts = VisitorAppointment.objects.values('infirmary').annotate(count=Count('id'))
    for item in visitor_counts:
        infirmary = item['infirmary']
        if infirmary in infirmary_counts:
            infirmary_counts[infirmary] += item['count']

    # Preparar os dados para o gráfico
    data = [infirmary_counts[label] for label in labels]

    # Retornar os dados em formato JSON com ensure_ascii=False
    return JsonResponse(
        {'labels': labels, 'data': data},
        json_dumps_params={'ensure_ascii': False}
    )