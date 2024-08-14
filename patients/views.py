from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from .models import Student, Employee, Visitor
from controller.crud import create_objects, get_object, get_by_id
import json



''' 
    Module responsible for the functionalities to be rendered on pages that require patient information.

    Each patient entity has its own functions for data manipulation, 
    insertion, and deletion, where the function receives the request, 
    handles error processing, and calls a CRUD function from the 
    controller app to persist the data in the database.

'''

#### ----------------- STUDENTS VIEWS ----------------- ####

@csrf_exempt
def create_students(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if isinstance(data, list):
                return create_objects(Student, data)
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid data format, expected a list of objects'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


def search_student(request):
    name = request.GET.get('name', None)
    ra = request.GET.get('ra', None)
    try:
        student = get_object(Student, name=name, registry=ra)
        if isinstance(student, Student):
            student_data = model_to_dict(student)
        else:
            student_data = [model_to_dict(obj) for obj in student]
        return JsonResponse({'status': 'success', 'data': student_data}, status=200)
    except Http404:
        return JsonResponse({'status': 'error', 'message': 'No records found'}, status=404)


def search_student_by_name(request):
    query = request.GET.get('q', '')
    if query:
        try: 
            results = get_object(Student, name__icontains=query)
            data = list(results.value('id', 'name', 'class_group.name'))
        except Http404:
            data = []
    else: 
        data = []
    return JsonResponse({'results': data}, status=200)    



def search_student_by_id(request):
    pk = request.GET.get('id', None)
    try:
        obj = get_by_id(Student, pk)
        data = model_to_dict(obj)
        return JsonResponse({'status': 'success', 'data': data}, status=200)
    except Http404:
        return JsonResponse({'status': 'error', 'message': 'No records found'}, status=404)
    



#### ----------------- EMPLOYEES VIEWS ----------------- ####
@csrf_exempt
def create_employees(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if isinstance(data, list):
                return create_objects(Employee, data)
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid data format, expected a list of objects'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


def search_employee(request):
    name = request.GET.get('name', None)
    badge = request.GET.get('badge', None)
    try:
        employee = get_object(Employee, name=name, registry=badge)
        if isinstance(employee, Employee):
            employee_data = model_to_dict(employee)
        else:
            employee_data = [model_to_dict(obj) for obj in employee]
        return JsonResponse({'status': 'success', 'data': employee_data}, status=200)
    except Http404:
        return JsonResponse({'status': 'error', 'message': 'No records found'}, status=404)

def search_employee_by_name(request):
    query = request.GET.get('q', '')
    if query:
        try: 
            results = get_object(Employee, name__icontains=query)
            data = list(results.value('id', 'name', 'registry'))
        except Http404:
            data = []
    else: 
        data = []
    return JsonResponse({'results': data}, status=200)


def search_employee_by_id(request):
    pk = request.GET.get('id', None)
    try:
        obj = get_by_id(Employee, pk)
        data = model_to_dict(obj)
        return JsonResponse({'status': 'success', 'data': data}, status=200)
    except Http404:
        return JsonResponse({'status': 'error', 'message': 'No records found'}, status=404)
    

#### ----------------- VISITORS VIEWS ----------------- ####
@csrf_exempt
def create_visitor(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if isinstance(data, list):
                return create_objects(Visitor, data)
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid data format, expected a list of objects'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)


def search_visitor(request):
    name = request.GET.get('name', None)
    try:
        visitor = get_object(Visitor, name=name)
        if isinstance(visitor, Visitor):
            visitor_data = model_to_dict(visitor)
        else:
            visitor_data = [model_to_dict(obj) for obj in visitor] 
        return JsonResponse({'status': 'success', 'data': visitor_data}, status=200)
    except Http404:
        return JsonResponse({'status': 'error', 'message': 'No records found'}, status=404)
    
def search_visitor_by_name(request):
    query = request.GET.get('q', '')
    if query:
        try: 
            results = get_object(Visitor, name__icontains=query)
            data = list(results.value('id', 'name', 'company'))
        except Http404:
            data = []
    else: 
        data = []
    return JsonResponse({'results': data}, status=200)



def search_visitor_by_id(request):
    pk = request.GET.get('id', None)
    try:
        obj = get_by_id(Visitor, pk)
        data = model_to_dict(obj)
        return JsonResponse({'status': 'success', 'data': data}, status=200)
    except Http404:
        return JsonResponse({'status': 'error', 'message': 'No records found'}, status=404)