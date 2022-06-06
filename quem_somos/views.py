from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='login')
def tutorial(request):
    return render(request, 'tutorial.html')

def tutorial_nl(request):
    user = request.user
    if user.is_authenticated:
        return redirect('tutorial')
    else:
        return render(request, 'tutorial_nl.html')

def documentacao(request):
    return render(request, 'documentacao.html')

@login_required(login_url='login')
def desenvolvedores(request):
    return render(request, 'desenvolvedores.html')

def desenvolvedores_nl(request):
    user = request.user
    if user.is_authenticated:
        return redirect('desenvolvedores')
    else:
        return render(request, 'desenvolvedores_nl.html')