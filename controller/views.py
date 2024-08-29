from django.shortcuts import render
from django.contrib.auth.decorators import login_required


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