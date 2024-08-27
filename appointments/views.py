from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *
from patients.models import Student, Employee, Visitor
from patients.views import search_student, search_employee, search_visitor
from controller.crud import create_objects
from django.contrib.auth.decorators import login_required
import logging



logger = logging.getLogger('appointments.views')


def create_infirmary(data):
    logger.info("Starting create_infirmary function.")
    
    if data is not None:
        if isinstance(data, list):
            logger.debug(f"Received data is a list with {len(data)} items.")
            create_objects(Infirmary, data)
            logger.info("Infirmaries successfully created.")
            return {'status': 'success'}
        else:
            logger.warning("Invalid data format, expected a list of objects.")
            return {'status': 'error', 'message': 'Invalid data format, expected a list of objects'}
    else:
        logger.warning("No data provided.")
        return {'status': 'error', 'message': 'No data provided'}

def create_nurses(data):
    logger.info("Starting create_nurses function.")
    
    if data is not None:
        if isinstance(data, list):
            logger.debug(f"Received data is a list with {len(data)} items.")
            create_objects(Nurse, data)
            logger.info("Nurses successfully created.")
            return {'status': 'success'}
        else:
            logger.warning("Invalid data format, expected a list of objects.")
            return {'status': 'error', 'message': 'Invalid data format, expected a list of objects'}
    else:
        logger.warning("No data provided.")
        return {'status': 'error', 'message': 'No data provided'}


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
            return JsonResponse({'status': 'error', 'message': 'Student not found'}, status=404)

        return render(request, 'ap_student.html', {'student': student})

    if request.method == 'POST':        
        pass



@login_required
def employee_appointment(request):
    if request.method == 'GET':
        name = request.GET.get('name', None)
        registry = request.GET.get('badge', None)
        employee = search_employee(name, registry)

        return render(request, 'ap_employee.html', {'employee': employee})

    if request.method == 'POST': 
        pass
    



@login_required
def visitor_appointment(request):
    if request.method == 'GET':
        name = request.GET.get('name', None)
        if name:
            visitor = search_visitor(name)

            return render(request, 'ap_visitor.html', {'visitor': visitor}) 
              
        return render(request, 'ap_visitor.html')
    
    if request.method == 'POST':
        pass