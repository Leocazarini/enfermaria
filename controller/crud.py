from django.shortcuts import get_object_or_404
from django.http import JsonResponse, Http404
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict



def create_objects(model, data_list):
    try:
        objects = []
        for data in data_list:
            obj = model.objects.create(**data)
            obj.save()
            objects.append(model_to_dict(obj))
        return JsonResponse({'status': 'success', 'data': objects}, status=201)
    except ValidationError as e:
        return JsonResponse({'status': 'error', 'message': e.message_dict}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)





def get_object(model, name=None, registry=None, related_fields=None):

    query = model.objects.all()
    if related_fields:
        if isinstance(related_fields, list):
            query = query.select_related(*related_fields)
        else:
            query = query.select_related(related_fields)
    
    if name:
        objs = query.filter(name__icontains=name)
        if not objs.exists():
            raise Http404('No records found.')
        return list(objs)  
    elif registry:
        obj = get_object_or_404(query, registry=registry)
        return [obj]  
    else:
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

    try:
        obj = get_object_or_404(model, registry=registry)
        for key, value in data.items():
            setattr(obj, key, value)
        obj.save()
        return JsonResponse({'status': 'success', 'data': model_to_dict(obj)})
    except Http404:
        return JsonResponse({'status': 'error', 'message': 'Object not found'}, status=404)
    except ValidationError as e:
        return JsonResponse({'status': 'error', 'message': e.message_dict}, status=400)





def delete_object(model, registry):
    try:
        obj = get_object_or_404(model, registry=registry)
        obj.delete()
        return JsonResponse({'status': 'success', 'message': 'Deleted successfully'})    
    except Http404:
        return JsonResponse({'status': 'error', 'message': 'Object not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)




