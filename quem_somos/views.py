from django.shortcuts import render

# Create your views here.

def tutorial(request):
    return render(request, 'tutorial.html')

def documentacao(request):
    return render(request, 'documentacao.html')

def desenvolvedores(request):
    return render(request, 'desenvolvedores.html')