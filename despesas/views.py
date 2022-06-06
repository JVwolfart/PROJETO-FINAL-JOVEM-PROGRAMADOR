from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.aggregates import Count, Sum
from despesas.models import Despesa
from cadastros.models import FormaPagamento, GrupoDespesa, TipoDespesa
from datetime import datetime
from django.core.paginator import Paginator
# Create your views here.





@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')


@login_required(login_url='login')
def despesa(request):
    hoje = datetime.today()
    hoje = datetime.strftime(hoje, '%Y-%m-%d')
    user = request.user
    fpags = FormaPagamento.objects.all().filter(
        Q(ativo=True,  usuario=user) | Q(padrao=True)
    ).order_by('forma')
    tipos = TipoDespesa.objects.all().filter(
        Q(ativo=True,  usuario=user) | Q(padrao=True)
    ).order_by('tipo')
    despesas = Despesa.objects.all().filter(
        usuario=user
    ).order_by('-id')[:5]
    return render(request, 'lancamentos.html', {'fpags':fpags, 'tipos':tipos, 'hoje':hoje, 'despesas':despesas})

@login_required(login_url='login')
def lancar_despesa(request):
    hoje = datetime.today()
    hoje = datetime.strftime(hoje, '%Y-%m-%d')
    user = request.user
    fpags = FormaPagamento.objects.all().filter(
        Q(ativo=True,  usuario=user) | Q(padrao=True)
    ).order_by('forma')
    tipos = TipoDespesa.objects.all().filter(
        Q(ativo=True,  usuario=user) | Q(padrao=True)
    ).order_by('tipo')
    despesas = Despesa.objects.all().filter(
        usuario=user
    ).order_by('-id')[:5]
    if request.method != 'POST':
        return render(request, 'lancamentos.html', {'fpags':fpags, 'tipos':tipos, 'hoje':hoje, 'despesas':despesas})
    else:
        id_tipo = request.POST.get('tipo')
        id_fpag = request.POST.get('fpag')
        data = request.POST.get('data')
        valor = request.POST.get('valor')
        despesa = request.POST.get('despesa').strip().title()
        if len(data) > 10:
            messages.add_message(request, messages.ERROR, 'Data inválida')
            return render(request, 'lancamentos.html', {'fpags':fpags, 'tipos':tipos, 'hoje':hoje, 'despesas':despesas})
        if not valor or valor == '':
            valor = 0
        if not id_tipo or id_tipo == '':
            messages.add_message(request, messages.WARNING, 'Selecione o tipo de despesa')
            return render(request, 'lancamentos.html', {'fpags':fpags, 'tipos':tipos, 'hoje':hoje, 'despesas':despesas})
        if not id_fpag or id_fpag == '':
            messages.add_message(request, messages.WARNING, 'Selecione a forma de pagamento')
            return render(request, 'lancamentos.html', {'fpags':fpags, 'tipos':tipos, 'hoje':hoje, 'despesas':despesas})
        tipo = TipoDespesa.objects.get(id=id_tipo)
        fpag = FormaPagamento.objects.get(id=id_fpag)
        valor = float(valor)
        if valor <= 0:
            messages.add_message(request, messages.ERROR, 'Valor inválido, precisa ser maior que zero')
            return render(request, 'lancamentos.html', {'fpags':fpags, 'tipos':tipos, 'hoje':hoje, 'despesas':despesas})
        lancamento = Despesa.objects.create(despesa=despesa, tipo=tipo, data=data, usuario=user, fpag=fpag, valor=valor)
        lancamento.save()
        messages.add_message(request, messages.SUCCESS, 'Lançamento incluido com sucesso')
        return redirect('despesa')

@login_required(login_url='login')
def alterar_despesa(request, id):
    user = request.user
    despesa = get_object_or_404(Despesa, id=id)
    fpags = FormaPagamento.objects.all().filter(
        Q(ativo=True,  usuario=user) | Q(padrao=True)
    ).order_by('forma')
    tipos = TipoDespesa.objects.all().filter(
        Q(ativo=True,  usuario=user) | Q(padrao=True)
    ).order_by('tipo')
    valor_despesa = str(despesa.valor)
    data = despesa.data
    data = datetime.strftime(data, '%Y-%m-%d')
    if despesa.usuario != user:
        messages.add_message(request, messages.ERROR, 'Essa despesa não pertence a esse usuário')
        return redirect('despesa')
    if request.method != 'POST':
        return render(request, 'alterar_despesa.html',{'fpags':fpags, 'tipos':tipos, 'despesa':despesa, 'data':data, 'valor_despesa':valor_despesa})
    
    else:
        id_tipo = request.POST.get('tipo')
        id_fpag = request.POST.get('fpag')
        data_despesa = request.POST.get('data')
        valor = request.POST.get('valor')
        descricao_despesa = request.POST.get('despesa').strip().title()
        if len(data_despesa) > 10:
            messages.add_message(request, messages.ERROR, 'Data inválida')
            return render(request, 'alterar_despesa.html',{'fpags':fpags, 'tipos':tipos, 'despesa':despesa, 'data':data, 'valor_despesa':valor_despesa})
        if not valor or valor == '':
            valor = 0
        if not id_tipo or id_tipo == '':
            messages.add_message(request, messages.WARNING, 'Selecione o tipo de despesa')
            return render(request, 'alterar_despesa.html',{'fpags':fpags, 'tipos':tipos, 'despesa':despesa, 'data':data, 'valor_despesa':valor_despesa})
        if not id_fpag or id_fpag == '':
            messages.add_message(request, messages.WARNING, 'Selecione a forma de pagamento')
            return render(request, 'alterar_despesa.html',{'fpags':fpags, 'tipos':tipos, 'despesa':despesa, 'data':data, 'valor_despesa':valor_despesa})
        tipo = TipoDespesa.objects.get(id=id_tipo)
        fpag = FormaPagamento.objects.get(id=id_fpag)
        valor = float(valor)
        if valor <= 0:
            messages.add_message(request, messages.ERROR, 'Valor inválido, precisa ser maior que zero')
            return render(request, 'alterar_despesa.html',{'fpags':fpags, 'tipos':tipos, 'despesa':despesa, 'data':data, 'valor_despesa':valor_despesa})
        else:
            despesa.data = data_despesa
            despesa.tipo = tipo
            despesa.fpag = fpag
            despesa.valor = valor
            despesa.despesa = descricao_despesa
            despesa.save()
            messages.add_message(request, messages.SUCCESS, f'Despesa {despesa} alterada com sucesso')
            return redirect('despesa')

@login_required(login_url='login')
def excluir_despesa(request, id):
    despesa = get_object_or_404(Despesa, id=id)
    despesa.delete()
    messages.add_message(request, messages.INFO, f'Despesa {despesa} deletada')
    return redirect('despesa')

@login_required(login_url='login')
def manut_despesas(request):
    user = request.user
    despesas = Despesa.objects.all().filter(
        usuario=user
    ).order_by('-data')
    paginator = Paginator(despesas, 10)
    page = request.GET.get('p')
    despesas = paginator.get_page(page)
    return render(request, 'manut_despesa.html', {'despesas':despesas})


@login_required(login_url='login')
def pesquisa(request):
    user = request.user
    termo = request.GET.get('termo').strip()
    if not termo or termo == '':
        messages.add_message(request, messages.INFO, 'Nenhum termo informado, tente novamente')
        return redirect('home')
    else:
        despesas = Despesa.objects.all().filter(
            Q(despesa__icontains=termo) | Q(tipo__tipo__icontains=termo) | Q(tipo__grupo__grupo__icontains=termo), usuario=user
        ).order_by('-data')
        if len(despesas) == 0:
            messages.add_message(request, messages.INFO, f'Não foi encontrado nenhum registro com o termo {termo}, tente novamente')
            return redirect('home')
        else:
            paginator = Paginator(despesas, 5)
            page = request.GET.get('p')
            despesas = paginator.get_page(page)
            return render(request, 'pesquisa.html', {'despesas':despesas, 'termo':termo})