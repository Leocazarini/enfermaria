from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict

# Create your views here.




def create_object(model, data):
    try:
        obj = model.objects.create(**data)
        obj.save()
        return JsonResponse({'status': 'success', 'id': obj.id}, status=201)
    
    except ValidationError as e:
        return JsonResponse({'status': 'error', 'message': e.message_dict}, status=400)
    


def get_object(model, name=None, record=None):
    if name:
        obj = get_object_or_404(model, name=name)
    elif record:
        obj = get_object_or_404(model, record=record)
    else:
        return JsonResponse({'status': 'error', 'message': 'Name or record must be provided'}, status=400)
    
    return JsonResponse({'status': 'success', 'data': model_to_dict(obj)})



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