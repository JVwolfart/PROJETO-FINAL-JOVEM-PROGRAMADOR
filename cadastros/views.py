from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from cadastros.models import FormaPagamento, GrupoDespesa, TipoDespesa

# Create your views here.

@login_required(login_url='login')
def cadastros(request):
    return render(request, 'cadastros.html')

@login_required(login_url='login')
def grupos(request):
    user = request.user
    grupos = GrupoDespesa.objects.all().filter(
        Q(usuario=user) | Q(padrao=True)
    )
    return render(request, 'grupos.html', {"grupos":grupos})

@login_required(login_url='login')
def adicionar_grupo(request):
    user = request.user
    if request.method != 'POST':
        return redirect('grupos')
    else:
        grupo = request.POST.get('grupo').strip().title()
        if not grupo or len(grupo) < 5:
            messages.add_message(request, messages.ERROR, 'Para cadastrar um novo grupo precisa ter pelo menos 5 caracteres')
            return redirect('grupos')
        else:
            novo_grupo = GrupoDespesa.objects.create(grupo=grupo, padrao=False, usuario=user, ativo=True)
            novo_grupo.save()
            messages.add_message(request, messages.SUCCESS, f'Grupo {grupo} cadastrado com sucesso')
            return redirect('grupos')

@login_required(login_url='login')
def alterar_grupo(request, id):
    user = request.user
    #grupo = GrupoDespesa.objects.get(id=id)
    grupo = get_object_or_404(GrupoDespesa, id=id)
    if request.method != "POST":
        return render(request, 'alterar_grupo.html', {"grupo":grupo})
    else:
        if grupo.usuario != user:
            messages.add_message(request, messages.ERROR, 'ERRO! Este grupo não pertence a esse usuário')
            return redirect('grupos')
        if grupo.padrao:
            messages.add_message(request, messages.ERROR, 'ERRO! Grupos padrão não podem ser alterados')
            return redirect('grupos')
        else:
            nome_grupo = request.POST.get('grupo').strip().title()
            if not nome_grupo or len(nome_grupo) < 5:
                messages.add_message(request, messages.ERROR, 'O grupo precisa ter pelo menos 5 caracteres')
                return redirect('grupos')
            else:
                grupo.grupo = nome_grupo
                grupo.save()
                messages.add_message(request, messages.SUCCESS, f'Grupo {grupo} alterado com sucesso')
                return redirect('grupos')

@login_required(login_url='login')
def desativar_grupo(request, id):
    grupo = get_object_or_404(GrupoDespesa, id=id)
    if grupo.ativo:
        grupo.ativo = False
        tipos = TipoDespesa.objects.all().filter(
            grupo=grupo
        )
        for t in tipos:
            t.ativo = False
            t.save()
    else:
        grupo.ativo = True
        tipos = TipoDespesa.objects.all().filter(
            grupo=grupo
        )
        for t in tipos:
            t.ativo = True
            t.save()
    grupo.save()
    return redirect('grupos')

@login_required(login_url='login')
def tipos(request):
    user = request.user
    grupos = GrupoDespesa.objects.all().filter(
        Q(usuario=user) | Q(padrao=True), Q(ativo=True)
    ).order_by('grupo')
    tipos = TipoDespesa.objects.all().filter(
        Q(usuario=user) | Q(padrao=True)   
    ).order_by('grupo__grupo', 'tipo')
    return render(request, 'tipos.html', {"grupos":grupos, "tipos":tipos})

@login_required(login_url='login')
def adicionar_tipo(request):
    user = request.user
    grupos = GrupoDespesa.objects.all().filter(
        Q(usuario=user) | Q(padrao=True), Q(ativo=True)
    ).order_by('grupo')
    tipos = TipoDespesa.objects.all().filter(
        Q(usuario=user) | Q(padrao=True)   
    ).order_by('grupo__grupo', 'tipo')
    if request.method != 'POST':
        return redirect('tipos')
    else:
        tipo = request.POST.get('tipo').strip().title()
        id_grupo = request.POST.get('grupo')
        if not id_grupo or id_grupo == '':
            messages.add_message(request, messages.WARNING, 'ATENÇÃO: Selecione um grupo para essa despesa')
            return render(request, 'tipos.html', {'grupos':grupos, 'tipos':tipos})
        grupo = GrupoDespesa.objects.get(id=id_grupo)
        if not tipo or len(tipo) < 5:
            messages.add_message(request, messages.ERROR, 'Para cadastrar um novo tipo de despesa precisa ter pelo menos 5 caracteres')
            return render(request, 'tipos.html', {'grupos':grupos, 'tipos':tipos})
        else:
            novo_tipo = TipoDespesa.objects.create(tipo=tipo, grupo=grupo, padrao=False, usuario=user, ativo=True)
            novo_tipo.save()
            messages.add_message(request, messages.SUCCESS, f'Tipo {tipo} cadastrado com sucesso')
            return redirect('tipos')

@login_required(login_url='login')
def alterar_tipo(request, id):
    user = request.user
    #grupo = GrupoDespesa.objects.get(id=id)
    grupos = GrupoDespesa.objects.all().filter(
        Q(usuario=user) | Q(padrao=True), Q(ativo=True)
    ).order_by('grupo')
    tipo = get_object_or_404(TipoDespesa, id=id)
    if not tipo.grupo.ativo:
        messages.add_message(request, messages.WARNING, 'ATENÇÃO: O grupo dessa despesa não está ativo, para fazer alterações no tipo primeiro reative o grupo')
        return redirect('tipos')
    if request.method != "POST":
        return render(request, 'alterar_tipo.html', {"tipo":tipo, "grupos":grupos})
    else:
        if tipo.usuario != user:
            messages.add_message(request, messages.ERROR, 'ERRO! Essa despesa não pertence a esse usuário')
            return redirect('tipos')
        if tipo.padrao:
            messages.add_message(request, messages.ERROR, 'ERRO! Tipos de despesa padrão não podem ser alterados')
            return redirect('tipos')
        else:
            nome_tipo = request.POST.get('tipo').strip().title()
            id_grupo = request.POST.get('grupo')
            grupo = GrupoDespesa.objects.get(id=id_grupo)
            if not nome_tipo or len(nome_tipo) < 5:
                messages.add_message(request, messages.ERROR, 'O grupo precisa ter pelo menos 5 caracteres')
                return render(request, 'alterar_tipo.html', {"tipo":tipo, "grupos":grupos})
            else:
                tipo.tipo = nome_tipo
                tipo.grupo = grupo
                tipo.save()
                messages.add_message(request, messages.SUCCESS, f'Despesa {tipo} alterada com sucesso')
                return redirect('tipos')

@login_required(login_url='login')
def desativar_tipo(request, id):
    tipo = get_object_or_404(TipoDespesa, id=id)
    if tipo.grupo.ativo:
        if tipo.ativo:
            tipo.ativo = False
        else:
            tipo.ativo = True
        tipo.save()
    else:
        messages.add_message(request, messages.WARNING, f'ATENÇÃO, o grupo de despesas {tipo.grupo} não está ativo, para proseguir com a operação primeiro reative o grupo')
        return redirect('tipos')
    return redirect('tipos')

@login_required(login_url='login')
def fpags(request):
    user = request.user
    fpags = FormaPagamento.objects.all().filter(
        Q(usuario=user) | Q(padrao=True)   
    )
    return render(request, 'fpag.html', {"fpags":fpags})

@login_required(login_url='login')
def adicionar_fpag(request):
    user = request.user
    fpags = FormaPagamento.objects.all().filter(
        Q(usuario=user) | Q(padrao=True)   
    )
    if request.method != 'POST':
        return render(request, 'fpag.html', {"fpags":fpags})
    else:
        fpag = request.POST.get('fpag').strip().title()
        if not fpag or len(fpag) < 2:
            messages.add_message(request, messages.ERROR, 'Nome da forma de pagamento precisa ter ao menos dois digitos')
            return render(request, 'fpag.html', {"fpags":fpags})
        else:
            nova_forma = FormaPagamento.objects.create(forma=fpag, usuario=user, padrao=False, ativo=True)
            nova_forma.save()
            messages.add_message(request, messages.SUCCESS, f'Forma de pagamento {fpag} cadastrada com sucesso')
            return redirect('fpags')

@login_required(login_url='login')
def alterar_fpag(request, id):
    user = request.user
    #grupo = GrupoDespesa.objects.get(id=id)
    fpag = get_object_or_404(FormaPagamento, id=id)
    if request.method != "POST":
        return render(request, 'alterar_fpag.html', {"fpag":fpag})
    else:
        if fpag.usuario != user:
            messages.add_message(request, messages.ERROR, 'ERRO! Este grupo não pertence a esse usuário')
            return redirect('fpags')
        if fpag.padrao:
            messages.add_message(request, messages.ERROR, 'ERRO! Grupos padrão não podem ser alterados')
            return redirect('fpags')
        else:
            forma = request.POST.get('fpag').strip().title()
            if not forma or len(forma) < 2:
                messages.add_message(request, messages.ERROR, 'Nome da forma de pagamento precisa ter ao menos dois digitos')
                return redirect('fpags')
            else:
                fpag.forma = forma
                fpag.save()
                messages.add_message(request, messages.SUCCESS, f'Forma de pagamento {fpag} alterada com sucesso')
                return redirect('fpags')

@login_required(login_url='login')
def desativar_fpag(request, id):
    fpag = get_object_or_404(FormaPagamento, id=id)
    if fpag.ativo:
        fpag.ativo = False
    else:
        fpag.ativo = True
    fpag.save()
    return redirect('fpags')
