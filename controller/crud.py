from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict
import logging


logger = logging.getLogger('controller.crud')



def create_objects(model, data_list):
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
    # Obter o objeto real do visitante
    visitor = get_object(visitor_model, email=visitor_email)

    if visitor and len(visitor) > 0:
        # Acessar o primeiro visitante da lista
        visitor_obj = visitor[0]

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