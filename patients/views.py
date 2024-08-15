from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from .models import *
from controller.crud import create_objects, get_object, get_by_id
import json


############################################################################################################
''' 
    Module responsible for the functionalities to be rendered on pages that require patient information.

    Each patient entity has its own functions for data manipulation, 
    insertion, and deletion, where the function receives the request, 
    handles error processing, and calls a CRUD function from the 
    controller app to persist the data in the database.

'''
############################################################################################################
'''  
    Alterar as funções para que elas estabaleçam uma relação entre si internamente, 
    e disponibilizem um endpoint apenas quando for necessária a interação com o usuário.

'''
############################################################################################################

########################## ----------------- STUDENTS VIEWS ----------------- ##############################



# endpoint -> # Internal operation 
def create_students(data):
    if data is not None:
        if isinstance(data, list):
            create_objects(Student, data)
            return {'status': 'success'}
        else:
            return {'status': 'error', 'message': 'Invalid data format, expected a list of objects'}
    else:
        return {'status': 'error', 'message': 'No data provided'}


# endpoint - /students-info/create -> # User operation
@csrf_exempt
def create_student_info(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if isinstance(data, list):
                return create_objects(StudentInfo, data)
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid data format, expected a list of objects'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


# endpoint -> # Internal operation 
def create_class_group(data):
    if data is not None:
        if isinstance(data, list):
            create_objects(ClassGroup, data)
            return {'status': 'success'}
        else:
            return {'status': 'error', 'message': 'Invalid data format, expected a list of objects'}
    else:
        return {'status': 'error', 'message': 'No data provided'}


###


# endpoint - /students/search -> # Internal operation
def search_student(name, registry):    
    try:
        students = get_object(Student, name=name, registry=registry, related_fields=['info', 'class_group'])
        if len(students) > 1:
            return JsonResponse({'status': 'error', 'message': 'More than one record found for the given information.'}, status=400)
        
        student = students[0]
        student_data = model_to_dict(student)
        student_info_data = model_to_dict(student.info)
        student_data['info'] = student_info_data
        student_data['class_group_name'] = student.class_group.name if student.class_group else None

        return student_data
    except Http404:
        return JsonResponse({'status': 'error', 'message': 'No records found'}, status=404)

# endpoint - /students/search/name -> # User operation
def search_student_by_name(request):
    query = request.GET.get('q', '')
    if query:
        try: 
            results = get_object(Student, name__icontains=query, related_fields=['class_group'])

            data = [
                {
                    'id': student.id,
                    'name': student.name,
                    'registry': student.registry,
                    'class_group_name': student.class_group.name if student.class_group else None
                }
                for student in results
            ]
        except Http404:
            data = []
    else: 
        data = []
    return JsonResponse({'results': data}, status=200)    

# endpoint  -> # Internal operation 
def search_student_by_id(request):
    pk = request.GET.get('id', None)
    try:
        obj = get_by_id(Student, pk, related_fields=['info', 'class_group'])
        data = model_to_dict(obj)
        
        data['info'] = model_to_dict(obj.info) if hasattr(obj, 'info') else None
        data['class_group_name'] = obj.class_group.name if obj.class_group else None
        
        return JsonResponse({'status': 'success', 'data': data}, status=200)
    except Http404:
        return JsonResponse({'status': 'error', 'message': 'No records found'}, status=404)

    

############################################################################################################

########################## ----------------- EMPLOYEES VIEWS ----------------- ##############################

# endpoint --> # Internal operation

def create_employees(data):
    if data is not None:
        if isinstance(data, list):
            create_objects(Employee, data)
            return {'status': 'success'}
        else:
            return {'status': 'error', 'message': 'Invalid data format, expected a list of objects'}
    else:
        return {'status': 'error', 'message': 'No data provided'}

# endpoint - /employees-info/create -> # User operation
@csrf_exempt 
def create_employee_info(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if isinstance(data, list):
                return create_objects(EmployeeInfo, data)
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid data format, expected a list of objects'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

# endpoint - /departments/create -> # Internal operation 

def create_department(data):
    if data is not None:
        if isinstance(data, list):
            create_objects(Department, data)
            return {'status': 'success'}
        else:
            return {'status': 'error', 'message': 'Invalid data format, expected a list of objects'}
    else:
        return {'status': 'error', 'message': 'No data provided'}


###


# endpoint --> # Internal operation
def search_employee(name, registry):
    
    try:
        employees = get_object(Employee, name=name, registry=registry, related_fields=['employee_info', 'department'])
        if len(employees) > 1:
            return JsonResponse({'status': 'error', 'message': 'More than one record found for the given information.'}, status=400)
        
        employee = employees[0]
        employee_data = model_to_dict(employee)
        employee_info_data = model_to_dict(employee.employee_info)
        employee_data['info'] = employee_info_data
        employee_data['department_name'] = employee.department.name if employee.department else None
        
        return employee_data
    except Http404:
        return JsonResponse({'status': 'error', 'message': 'No records found'}, status=404)

# endpoint - /employees/search/name -> # User operation
def search_employee_by_name(request):
    query = request.GET.get('q', '')
    if query:
        try: 
            results = get_object(Employee, name__icontains=query, related_fields=['department'])
            data = [
                {
                    'id': employee.id,
                    'name': employee.name,
                    'registry': employee.registry,
                    'department_name': employee.department.name if employee.department else None
                }
                for employee in results
            ]

        except Http404:
            data = []
    return JsonResponse({'results': data}, status=200)

# endpoint - /employees/search/id  -> # Internal operation 
def search_employee_by_id(request):
    pk = request.GET.get('id', None)
    try:
        obj = get_by_id(Employee, pk, related_fields=['employee_info', 'department'])
        data = model_to_dict(obj)
        
        data['info'] = model_to_dict(obj.employee_info) if hasattr(obj, 'employee_info') else None
        data['department_name'] = obj.department.name if obj.department else None
        
        return JsonResponse({'status': 'success', 'data': data}, status=200)
    except Http404:
        return JsonResponse({'status': 'error', 'message': 'No records found'}, status=404)
    



############################################################################################################

########################## ----------------- VISITORS VIEWS ----------------- ##############################

# endpoint - /visitors/create -> # User operation
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

# endpoint - /visitors-info/create -> # User operation
@csrf_exempt
def create_visitor_info(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if isinstance(data, list):
                return create_objects(VisitorInfo, data)
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid data format, expected a list of objects'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


###

# endpoint - /visitors/search -> # Internal operation
def search_visitor(name):
    
    visitors = get_object(Visitor, name=name, related_fields=['visitor_info'])
    try:
        
        visitor = model_to_dict(visitors[0])
        visitor_data = model_to_dict(visitor)
        visitor_info_data = model_to_dict(visitor.visitor_info)
        visitor_data['info'] = visitor_info_data
        
        return JsonResponse({'status': 'success', 'data': visitor_data}, status=200)
    except Http404:
        return JsonResponse({'status': 'error', 'message': 'No records found'}, status=404)
    
# endpoint - /visitors/search/name -> # User operation
def search_visitor_by_name(request):
    query = request.GET.get('q', '')
    if query:
        try: 
            results = get_object(Visitor, name__icontains=query)
            data = [
                {
                    'id': visitor.id,
                    'name': visitor.name
                }
                for visitor in results
            ]
        except Http404:
            data = []
    else: 
        data = []
    return JsonResponse({'results': data}, status=200)

# endpoint - /visitors/search/id -> # Internal operation 
def search_visitor_by_id(request):
    pk = request.GET.get('id', None)
    try:
        obj = get_by_id(Visitor, pk, related_fields=['visitor_info'])
        data = model_to_dict(obj)
        return JsonResponse({'status': 'success', 'data': data}, status=200)
    except Http404:
        return JsonResponse({'status': 'error', 'message': 'No records found'}, status=404)