from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from .models import *
from controller.crud import create_objects, get_object, get_by_id, update_object, update_info
import json
import logging


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

# log configuration

logger = logging.getLogger('patients.views')




########################## ----------------- STUDENTS VIEWS ----------------- ##############################



# endpoint -> # Internal operation 
def create_students(data):
    logger.info("Starting create_students function.")
    
    if data is not None:
        if isinstance(data, list):
            logger.debug(f"Received data is a list with {len(data)} items.")
            create_objects(Student, data)
            logger.info("Students successfully created.")
            return {'status': 'success'}
        else:
            logger.warning("Invalid data format, expected a list of objects.")
            return {'status': 'error', 'message': 'Invalid data format, expected a list of objects'}
    else:
        logger.warning("No data provided.")
        return {'status': 'error', 'message': 'No data provided'}

# endpoint - /students/create/info -> # User operation
@csrf_exempt
def create_student_info(request):
    if request.method == 'POST':
        try:
            logger.info("Received POST request to create/update student info")
            data = json.loads(request.body)
            logger.debug(f"Request data: {data}")
            

            if not isinstance(data, dict):
                logger.error("Invalid data format, expected a dictionary")
                return JsonResponse({'status': 'error', 'message': 'Invalid data format, expected a dictionary'}, status=400)
            
            student_id = data.get('student_id')
            allergies = data.get('allergies')
            patient_notes = data.get('patient_notes')

            if not student_id:
                logger.error("Missing required field: student_id")
                return JsonResponse({'status': 'error', 'message': 'Missing required field: student_id'}, status=400)

           
            logger.info(f"Calling update_info for student_id: {student_id}")
            updated_info = update_info(StudentInfo, student_id, 'student_id', allergies, patient_notes)
            logger.info(f"Student info updated successfully for student_id: {student_id}")
            
            return JsonResponse({'status': 'success', 'message': 'Student info updated successfully', 'data': updated_info.id}, status=200)

        except json.JSONDecodeError:
            logger.error("Invalid JSON format in request")
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    
    else:
        logger.error(f"Invalid request method: {request.method}")
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    
# endpoint -> # Internal operation 
def create_class_group(data):
    logger.info("Starting create_class_group function.")
    
    if data is not None:
        if isinstance(data, list):
            logger.debug(f"Received data is a list with {len(data)} items.")
            create_objects(ClassGroup, data)
            logger.info("Class groups successfully created.")
            return {'status': 'success'}
        else:
            logger.warning("Invalid data format, expected a list of objects.")
            return {'status': 'error', 'message': 'Invalid data format, expected a list of objects'}
    else:
        logger.warning("No data provided.")
        return {'status': 'error', 'message': 'No data provided'}


###


# endpoint - /students/search -> # Internal operation
def search_student(name, registry):    
    logger.info(f"Starting search for student with name: {name} and registry: {registry}.")
    
    try:
        students = get_object(Student, name=name, registry=registry, related_fields=['info', 'class_group'])
        logger.debug(f"{len(students)} students found with the given criteria.")
        
        if len(students) > 1:
            logger.warning("More than one record found for the given information.")
            return JsonResponse({'status': 'error', 'message': 'More than one record found for the given information.'}, status=400)
        
        student = students[0]
        student_data = model_to_dict(student)
        student_info_data = model_to_dict(student.info)
        student_data['info'] = student_info_data
        student_data['class_group_name'] = student.class_group.name if student.class_group else None

        logger.info(f"Student found: {student_data}")
        return student_data
    
    except Http404:
        logger.warning("No records found for the given criteria.")
        return None

# endpoint - /students/search/name -> # User operation
def search_student_by_name(request):
    query = request.GET.get('q', '')
    logger.info(f"Starting search for student by name with query: {query}")
    
    if query:
        try: 
            results = get_object(Student, name=query, related_fields=['class_group'])
            logger.debug(f"{len(results)} students found with the query '{query}'.")

            data = [
                {
                    'name': student.name,
                    'registry': student.registry,
                    'age': student.age,
                    'class_group_name': student.class_group.name if student.class_group else None
                }
                for student in results
            ]
        except Http404:
            logger.warning(f"No students found for the query '{query}'.")
            data = []
    else: 
        logger.info("No query provided, returning empty results.")
        data = []
    
    logger.info("Returning search results.")
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
    logger.info("Starting create_employees function.")
    
    if data is not None:
        if isinstance(data, list):
            logger.debug(f"Received data is a list with {len(data)} items.")
            create_objects(Employee, data)
            logger.info("Employees successfully created.")
            return {'status': 'success'}
        else:
            logger.warning("Invalid data format, expected a list of objects.")
            return {'status': 'error', 'message': 'Invalid data format, expected a list of objects'}
    else:
        logger.warning("No data provided.")
        return {'status': 'error', 'message': 'No data provided'}

# endpoint - /employees-info/create -> # User operation
@csrf_exempt 
def create_employee_info(request):
    if request.method == 'POST':
        try:
            logger.info("Received POST request to create/update employee info")
            data = json.loads(request.body)
            logger.debug(f"Request data: {data}")
            
            if not isinstance(data, dict):
                logger.error("Invalid data format, expected a dictionary")
                return JsonResponse({'status': 'error', 'message': 'Invalid data format, expected a dictionary'}, status=400)
            
            employee_id = data.get('employee_id')
            allergies = data.get('allergies')
            patient_notes = data.get('patient_notes')

            if not employee_id:
                logger.error("Missing required field: employee_id")
                return JsonResponse({'status': 'error', 'message': 'Missing required field: employee_id'}, status=400)

            logger.info(f"Calling update_info for employee_id: {employee_id}")
            updated_info = update_info(EmployeeInfo, employee_id, 'employee_id', allergies, patient_notes)
            logger.info(f"Employee info updated successfully for employee_id: {employee_id}")
            
            return JsonResponse({'status': 'success', 'message': 'Employee info updated successfully', 'data': updated_info.id}, status=200)

        except json.JSONDecodeError:
            logger.error("Invalid JSON format in request")
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    
    else:
        logger.error(f"Invalid request method: {request.method}")
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

# endpoint - /departments/create -> # Internal operation 
def create_department(data):
    logger.info("Starting create_department function.")
    
    if data is not None:
        if isinstance(data, list):
            logger.debug(f"Received data is a list with {len(data)} items.")
            create_objects(Department, data)
            logger.info("Departments successfully created.")
            return {'status': 'success'}
        else:
            logger.warning("Invalid data format, expected a list of objects.")
            return {'status': 'error', 'message': 'Invalid data format, expected a list of objects'}
    else:
        logger.warning("No data provided.")
        return {'status': 'error', 'message': 'No data provided'}


###


# endpoint --> # Internal operation
def search_employee(name, registry):
    logger.info(f"Starting search for employee with name: {name} and registry: {registry}.")
    
    try:
        employees = get_object(Employee, name=name, registry=registry, related_fields=['info', 'department'])
        logger.debug(f"{len(employees)} employees found with the given criteria.")
        
        if len(employees) > 1:
            logger.warning("More than one record found for the given information.")
            return JsonResponse({'status': 'error', 'message': 'More than one record found for the given information.'}, status=400)
        
        employee = employees[0]
        employee_data = model_to_dict(employee)
        employee_info_data = model_to_dict(employee.info)
        employee_data['info'] = employee_info_data
        employee_data['department_name'] = employee.department.name if employee.department else None
        
        logger.info(f"Employee found: {employee_data}")
        return employee_data
    
    except Http404:
        logger.warning("No records found for the given criteria.")
        return None

# endpoint - /employees/search/name -> # User operation
def search_employee_by_name(request):
    query = request.GET.get('q', '')
    logger.info(f"Starting search for employee by name with query: {query}")
    
    if query:
        try: 
            results = get_object(Employee, name=query, related_fields=['department'])
            logger.debug(f"{len(results)} employees found with the query '{query}'.")

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
            logger.warning(f"No employees found for the query '{query}'.")
            data = []
    else:
        logger.info("No query provided, returning empty results.")
        data = []

    logger.info("Returning search results.")
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
        logger.info("Received a POST request to create visitors.")
        
        try:
            data = json.loads(request.body)
            logger.debug(f"Request body successfully parsed: {data}")
            
            if isinstance(data, list):
                logger.debug(f"Data is a list with {len(data)} items.")
                return create_objects(Visitor, data)
            else:
                logger.warning("Invalid data format, expected a list of objects.")
                return JsonResponse({'status': 'error', 'message': 'Invalid data format, expected a list of objects'}, status=400)
        
        except json.JSONDecodeError:
            logger.error("Failed to parse JSON from request body.")
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    else:
        logger.error(f"Invalid request method: {request.method}")
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

###

# endpoint - /visitors/search -> # Internal operation
def search_visitor(name, email):
    try:
        visitors = get_object(Visitor, name=name, email=email)
        
        if not visitors:
            raise Http404('No records found.')
        
        visitor = visitors[0]  
        visitor_data = model_to_dict(visitor)
        logger.info(f"Visitor found: {visitor_data}")
        return visitor_data
    
    except Http404:
        return None
    
# endpoint - /visitors/search/name -> # User operation
def search_visitor_by_name(request):
    query = request.GET.get('q', '')
    logger.info(f"Starting search for visitor by name with query: {query}")
    
    if query:
        try: 
            results = get_object(Visitor, name=query)
            logger.debug(f"{len(results)} visitors found with the query '{query}'.")

            data = [
                {
                
                    'name': visitor.name,
                    'age': visitor.age,
                    'email': visitor.email,
                }
                for visitor in results
            ]
        except Http404:
            logger.warning(f"No visitors found for the query '{query}'.")
            data = []
    else: 
        logger.info("No query provided, returning empty results.")
        data = []
    
    logger.info("Returning search results.")
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