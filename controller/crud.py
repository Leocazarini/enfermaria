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





def get_object(model, name=None, registry=None):
    if name:
        objs = model.objects.filter(name__icontains=name)
        if not objs.exists():
            raise Http404('No records found.')
        return objs  
    elif registry:
        obj = get_object_or_404(model, registry=registry)
        return obj  
    else:
        raise Http404('Name or registry must be provided.')


def get_by_id(model, pk):
    obj = get_object_or_404(model, pk=pk)
    return obj





def update_object(model, pk, data):
    obj = get_object_or_404(model, pk=pk)
    for key, value in data.items():
        setattr(obj, key, value)
    obj.save()
    return JsonResponse({'status': 'success', 'data': model_to_dict(obj)})



def delete_object(model, pk):
    obj = get_object_or_404(model, pk=pk)
    obj.delete()
    return JsonResponse({'status': 'success', 'message': 'Deleted successfully'})




