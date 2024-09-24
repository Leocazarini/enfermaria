import logging
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict
from django.utils import timezone
from django.db.models import Count
from collections import defaultdict
from appointments.models import StudentAppointment, EmployeeAppointment, VisitorAppointment



logger = logging.getLogger('controller.crud')


########### Generic CRUD functions ###########

def create_objects(model, data_list):
    """
    Create objects in the specified model using the provided data.

    Args:
        model (Model): The model in which the objects will be created.
        data_list (list): A list of dictionaries containing the data for each object.

    Returns:
        JsonResponse: A JSON response containing the status and data of the created objects.

    Raises:
        ValidationError: If there is a validation error while creating the objects.
        Exception: If any other exception occurs during the creation process.
    """
    try:
        logger.info(f"Creating objects in model: {model}")
        logger.info(f"Data received: {data_list}")
        objects = []
        for data in data_list:
            obj = model.objects.create(**data)
            obj.save()
            objects.append(model_to_dict(obj))
            logger.info(f"Created object: {obj}")
        return JsonResponse({'status': 'success', 'data': objects}, status=201)
    except ValidationError as e:
        logger.error(f"Validation Error: {e.message_dict}")
        return JsonResponse({'status': 'error', 'message': e.message_dict}, status=400)
    except Exception as e:
        logger.error(f"Exception: {e}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


def get_object(model, name=None, registry=None, email=None, related_fields=None):
    """
    Retrieve an object from the database based on the provided parameters.
    Args:
        model: The model class to query.
        name (str, optional): The name to filter the objects by. Defaults to None.
        registry (str, optional): The registry to filter the object by. Defaults to None.
        email (str, optional): The email to filter the object by. Defaults to None.
        related_fields (str or list, optional): The related fields to select. Defaults to None.
    Returns:
        list or None: A list of objects matching the provided parameters, or None if no objects are found.
    Raises:
        Http404: If no objects are found with the provided name or registry.
    """
    ...
    logger.info(f"Starting get_object function for model: {model.__name__}.")

    query = model.objects.all()
    
    if related_fields:
        if isinstance(related_fields, list):
            logger.debug(f"Selecting related fields: {related_fields}.")
            query = query.select_related(*related_fields)
        else:
            logger.debug(f"Selecting related field: {related_fields}.")
            query = query.select_related(related_fields)
    
    if email:
        logger.debug(f"Filtering object with email: {email}.")
        try:
            obj = query.get(email=email)
            logger.info(f"Object found with email: {email}.")
            return [obj]
        except model.DoesNotExist:
            logger.warning(f"No records found with email: {email}")
            return None

    if name:
        logger.debug(f"Filtering objects with name containing: {name}.")
        objs = query.filter(name__icontains=name)
        if not objs.exists():
            logger.warning("No records found with the provided name.")
            raise Http404('No records found.')
        logger.info(f"{len(objs)} objects found with the name containing: {name}.")
        return list(objs)  
    elif registry:
        logger.debug(f"Filtering object with registry: {registry}.")
        obj = get_object_or_404(query, registry=registry)
        logger.info(f"Object found with registry: {registry}.")
        return [obj]  
    else:
        logger.error("Neither name nor registry was provided. Raising Http404.")
        raise Http404('Name or registry must be provided.')


def get_by_id(model, pk, related_fields=None):
    query = model.objects.all()
    
    if related_fields:
        if isinstance(related_fields, list):
            query = query.select_related(*related_fields)
        else:
            query = query.select_related(related_fields)
    
    return get_object_or_404(query, pk=pk)


def update_object(model, registry, data):
    logger.info(f"Starting update_object function for model: {model.__name__}, registry: {registry}.")
    
    try:
        obj = get_object_or_404(model, registry=registry)
        logger.debug(f"Object found with registry: {registry}. Updating with data: {data}.")
        
        for key, value in data.items():
            setattr(obj, key, value)
        
        obj.save()
        logger.info(f"Object with registry {registry} updated successfully.")
        return JsonResponse({'status': 'success', 'data': model_to_dict(obj)})
    
    except Http404:
        logger.warning(f"Object with registry {registry} not found.")
        return JsonResponse({'status': 'error', 'message': 'Object not found'}, status=404)
    
    except ValidationError as e:
        logger.error(f"Validation error while updating object with registry {registry}: {e.message_dict}")
        return JsonResponse({'status': 'error', 'message': e.message_dict}, status=400)


def delete_object(model, registry):
    logger.info(f"Starting delete_object function for model: {model.__name__}, registry: {registry}.")
    
    try:
        obj = get_object_or_404(model, registry=registry)
        logger.debug(f"Object found with registry: {registry}. Deleting object.")
        
        obj.delete()
        logger.info(f"Object with registry {registry} deleted successfully.")
        return JsonResponse({'status': 'success', 'message': 'Deleted successfully'})    
    
    except Http404:
        logger.warning(f"Object with registry {registry} not found.")
        return JsonResponse({'status': 'error', 'message': 'Object not found'}, status=404)
    
    except Exception as e:
        logger.error(f"Error occurred while deleting object with registry {registry}: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)



########### Info tables ###########

def get_info_by_patient(info_model, foreign_key_value, foreign_key_field):
    logger.info(f"Starting get_info_by_patient function for model: {info_model.__name__}.")
    logger.debug(f"Looking up {info_model.__name__} with {foreign_key_field} = {foreign_key_value}.")
    
    try:
        result = info_model.objects.get(**{foreign_key_field: foreign_key_value})
        logger.info(f"Information found for {foreign_key_field} = {foreign_key_value}.")
        return result
        
    except info_model.DoesNotExist:
        logger.warning(f"No information found for {foreign_key_field} = {foreign_key_value}.")
        return None



def update_info(info_model, foreign_key_value, foreign_key_field, allergies=None, patient_notes=None):
    logger.info(f"Starting update_info function for model: {info_model.__name__}.")
    logger.debug(f"Updating information for {foreign_key_field} = {foreign_key_value}. Allergies: {allergies}, Notes: {patient_notes}")
    
    info = get_info_by_patient(info_model, foreign_key_value, foreign_key_field)
    
    if info:
        logger.info(f"Information found for {foreign_key_field} = {foreign_key_value}. Updating record.")
        info.allergies = allergies
        info.patient_notes = patient_notes
        info.save()
        logger.info(f"Information updated for {foreign_key_field} = {foreign_key_value}.")
        return info
    else:
        logger.warning(f"No information found for {foreign_key_field} = {foreign_key_value}. Creating new record.")
        
        return create_info(info_model, foreign_key_value, foreign_key_field, allergies, patient_notes)



def create_info(info_model, foreign_key_value, foreign_key_field, allergies=None, patient_notes=None):
    logger.info(f"Starting create_info function for model: {info_model.__name__}.")
    logger.debug(f"Creating information for {foreign_key_field} = {foreign_key_value}. Allergies: {allergies}, Notes: {patient_notes}")
    
    info = info_model.objects.create(**{
        foreign_key_field: foreign_key_value,
        'allergies': allergies,
        'patient_notes': patient_notes
    })
    
    logger.info(f"Information created successfully for {foreign_key_field} = {foreign_key_value}.")
    return info


########### Visitor update info ###########

def update_visitor_info(visitor_model, visitor_email, allergies=None, patient_notes=None):
    """
    Update the information of a visitor.
    Args:
        visitor_model: The model class for the visitor.
        visitor_email: The email of the visitor.
        allergies (optional): The allergies of the visitor. Defaults to None.
        patient_notes (optional): The notes about the patient. Defaults to None.
    Returns:
        A JSON response containing the status and data of the updated visitor if successful,
        or an error message if the visitor is not found.
    """
    # Obter o objeto real do visitante
    visitor = get_object(visitor_model, email=visitor_email)

    if visitor and len(visitor) > 0:
        # Acessar o primeiro visitante da lista
        visitor_obj = visitor[0]

        logger.info(f"Updating visitor: allergies={allergies}, patient_notes={patient_notes}")


        # Atualizar os campos diretamente no objeto
        visitor_obj.allergies = allergies
        visitor_obj.patient_notes = patient_notes

        # Salvar as alterações no banco de dados
        visitor_obj.save()

        logger.info(f"Information updated for visitor with email: {visitor_email}.")
        return JsonResponse({'status': 'success', 'data': model_to_dict(visitor_obj)})
    
    else:
        logger.warning(f"No visitor found with email: {visitor_email}.")
        return JsonResponse({'status': 'error', 'message': 'Visitor not found'}, status=404)
    



########### Appointment search ###########

def get_appointment(model, identifier_field, patient_id=None, appointment_date=None):
    logger.info(f"Starting get_appointment function for model: {model.__name__}.")
    
    if patient_id is None and appointment_date is None:
        logger.warning("No search parameters provided.")
        return []

    # Inicia a query base
    query = model.objects.all()

    # Filtro dinâmico por patient_id (student_id ou employee_id)
    if patient_id:
        filter_kwargs = {identifier_field: patient_id}  # Usamos o identificador dinâmico
        query = query.filter(**filter_kwargs)
        logger.debug(f"Filtering appointments by {identifier_field} = {patient_id}.")

    # Filtro por appointment_date
    if appointment_date:
        query = query.filter(appointment_date=appointment_date)
        logger.debug(f"Filtering appointments by appointment_date = {appointment_date}.")

    # Verifica se há resultados
    if not query.exists():
        logger.warning(f"No appointments found for the given criteria: {identifier_field} = {patient_id}, appointment_date = {appointment_date}.")
        return []

    # Converte os resultados em dicionários
    results = list(query.values())
    logger.info(f"Appointments found: {len(results)} record(s) found.")
    
    return results




########### Reports Module ###########

def get_nurse_appointments_current_year():
    # Obter o ano atual
    current_year = timezone.now().year

    # Filtrar atendimentos do ano atual para cada modelo
    student_appointments = StudentAppointment.objects.filter(date__year=current_year)
    employee_appointments = EmployeeAppointment.objects.filter(date__year=current_year)
    visitor_appointments = VisitorAppointment.objects.filter(date__year=current_year)

    # Combinar os querysets em uma lista
    all_appointments = list(student_appointments) + list(employee_appointments) + list(visitor_appointments)

    # Dicionário para armazenar a contagem por enfermeira
    nurse_counts = defaultdict(int)

    # Iterar sobre todos os atendimentos e contar por enfermeira
    for appointment in all_appointments:
        nurse = appointment.nurse
        nurse_counts[nurse] += 1

    # Converter o dicionário em uma lista de dicionários para o template
    nurse_appointments = [{'nurse': nurse, 'count': count} for nurse, count in nurse_counts.items()]

    return nurse_appointments


def get_total_appointments_current_year():
    current_year = timezone.now().year

    total_students = StudentAppointment.objects.filter(date__year=current_year).count()
    total_employees = EmployeeAppointment.objects.filter(date__year=current_year).count()
    total_visitors = VisitorAppointment.objects.filter(date__year=current_year).count()

    total_appointments = total_students + total_employees + total_visitors

    return total_appointments



def get_total_appointments_today():
    today = timezone.now().date()

    total_students = StudentAppointment.objects.filter(date__date=today).count()
    total_employees = EmployeeAppointment.objects.filter(date__date=today).count()
    total_visitors = VisitorAppointment.objects.filter(date__date=today).count()

    total_appointments = total_students + total_employees + total_visitors

    return total_appointments


def get_total_appointments_infirmary_current_year(infirmary):
    if not infirmary:
        print("Infirmary is None or empty.")
        return 0  # Retornar 0 se infirmary é None ou vazio

    current_year = timezone.now().year
    infirmary_normalized = infirmary.strip()

    total_students = StudentAppointment.objects.filter(
        date__year=current_year,
        infirmary__iexact=infirmary_normalized
    ).count()
    total_employees = EmployeeAppointment.objects.filter(
        date__year=current_year,
        infirmary__iexact=infirmary_normalized
    ).count()
    total_visitors = VisitorAppointment.objects.filter(
        date__year=current_year,
        infirmary__iexact=infirmary_normalized
    ).count()

    total_appointments = total_students + total_employees + total_visitors

    print(f"Total appointments for infirmary '{infirmary}': {total_appointments}")
    return total_appointments



def get_total_appointments_infirmary_today(infirmary):
    if not infirmary:
        print("Infirmary is None or empty.")
        return 0  # Retornar 0 se infirmary é None ou vazio

    today = timezone.now().date()
    infirmary_normalized = infirmary.strip()

    total_students = StudentAppointment.objects.filter(
        date__date=today,
        infirmary__iexact=infirmary_normalized
    ).count()
    total_employees = EmployeeAppointment.objects.filter(
        date__date=today,
        infirmary__iexact=infirmary_normalized
    ).count()
    total_visitors = VisitorAppointment.objects.filter(
        date__date=today,
        infirmary__iexact=infirmary_normalized
    ).count()

    total_appointments = total_students + total_employees + total_visitors

    print(f"Total appointments for infirmary '{infirmary}': {total_appointments}")
    return total_appointments



def get_chart_data(request):
    # Agregar as contagens por enfermaria
    labels = ["Infantil", "Fundamental", "Ensino Médio", "Externo"]
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

    # Retornar os dados em formato JSON
    return JsonResponse({'labels': labels, 'data': data})