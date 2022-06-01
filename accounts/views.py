from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.core.validators import  validate_email
# Create your views here.

def login(request):
    if request.method != 'POST':
        return render(request, 'login.html')
    else:
        #usuario = request.POST.get('usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        email_existe = User.objects.all().filter(email=email).exists()
        if not email_existe:
            messages.add_message(request, messages.ERROR, f'ERRO! Email ou senha inválidos')    
            return render(request, 'login.html')
        else:
            usuario = User.objects.get(email=email)
            user = auth.authenticate(request, username=usuario.username, password=senha)
            if not user:
                messages.add_message(request, messages.ERROR, f'ERRO! Email ou senha inválidos')
                return render(request, 'login.html')
            else:
                auth.login(request, user)
                messages.add_message(request, messages.SUCCESS, f'Login feito com sucesso!')
                return redirect('home')

def cadastro(request):
    if request.method != 'POST':
        return render(request, 'cadastro.html')
    nome = request.POST.get('nome').strip().title()
    sobrenome = request.POST.get('sobrenome').strip().title()
    email = request.POST.get('email').strip()
    usuario = request.POST.get('usuario').strip()
    senha = request.POST.get('senha').strip()
    senha2 = request.POST.get('senha2').strip()

    try: 
        validate_email(email)
    except:
        messages.add_message(request, messages.ERROR, 'Email inválido')
        return render(request, 'cadastro.html')

    if not nome or not sobrenome or not email or not usuario or not senha or not senha2:
        messages.add_message(request, messages.ERROR, 'ERRO! nenhum campo pode ficar vazio')
        return render(request, 'cadastro.html')
    
    if senha != senha2:
        messages.add_message(request, messages.ERROR, 'ERRO! senhas não conferem')
        return render(request, 'cadastro.html')

    if len(senha) < 8:
        messages.add_message(request, messages.ERROR, 'ERRO! senha deve ter mais de 8 caracteres')
        return render(request, 'cadastro.html')

    if senha.isnumeric():
        messages.add_message(request, messages.ERROR, 'ERRO! senha não pode ser somente numérica')
        return render(request, 'cadastro.html')

    if User.objects.filter(username=usuario).exists():
        messages.add_message(request, messages.ERROR, f'ERRO! Usuário {usuario} já existe')
        return render(request, 'cadastro.html')

    if User.objects.filter(email=email).exists():
        messages.add_message(request, messages.ERROR, f'ERRO! Email {email} já existe')
        return render(request, 'cadastro.html')
    else:
        user = User.objects.create_user(username=usuario, email=email,  password=senha, first_name=nome, last_name=sobrenome)
        user.save()
        messages.add_message(request, messages.SUCCESS, f'Cadastro de {usuario} feito com sucesso, faça seu login')
        return redirect('login')

def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.SUCCESS, 'Logout feito com sucesso')
    return redirect('login')