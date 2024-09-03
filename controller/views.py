from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required
def index(request):
    if request.method == 'GET':
        full_name = request.user.first_name
        context = {
        'first_name': full_name,
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