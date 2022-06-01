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
def relatorios(request):
    hoje = datetime.today()
    hoje = datetime.strftime(hoje, '%Y-%m-%d')
    return render(request, 'relatorios.html', {'hoje':hoje})

@login_required(login_url='login')
def despesas_por_data(request):
    user = request.user
    despesas = Despesa.objects.all().filter(
        usuario=user
    ).values('data').annotate(total=Sum('valor'), count=Count('data')).order_by('-data')
    if len(despesas) == 0:
        messages.add_message(request, messages.WARNING, 'Não existem registros para esse usuário')
        return redirect('home')
    total = despesas.aggregate(Sum('total'))
    total = f"{total['total__sum']:.2f}"
    for d in despesas:
        d['total'] = f'{d["total"]:.2f}'
    paginator = Paginator(despesas, 10)
    page = request.GET.get('p')
    despesas = paginator.get_page(page)
    return render(request, 'despesas_por_data.html', {'despesas':despesas, 'total':total})

@login_required(login_url='login')
def ver_despesas(request, data):
    format = "%Y-%m-%d"
    try:
        data_valida = bool(datetime.strptime(data, format))
    except ValueError:
        data_valida = False
    if data_valida:
        user = request.user
        despesas = Despesa.objects.all().filter(
            usuario=user, data=data
        )
        if len(despesas) == 0:
            messages.add_message(request, messages.WARNING, 'Não existem registros para esse usuário')
            return redirect('home')
        total = despesas.aggregate(Sum('valor'))
        total = f"{total['valor__sum']:.2f}"
        paginator = Paginator(despesas, 5)
        page = request.GET.get('p')
        despesas = paginator.get_page(page)
        return render(request, 'ver_despesas.html', {'despesas':despesas, 'total':total})
    else:
        messages.add_message(request, messages.ERROR, 'Data inválida')
        return redirect('despesas_por_data')

@login_required(login_url='login')
def despesas_por_intervalo(request):
    user = request.user
    data_inicial_sf = request.GET.get('data_inicial')
    data_final_sf = request.GET.get('data_final')
    data_inicial = datetime.strptime(data_inicial_sf, '%Y-%m-%d')
    data_final = datetime.strptime(data_final_sf, '%Y-%m-%d')
    if data_inicial > data_final:
        messages.add_message(request, messages.WARNING, 'Data inicial não pode ser maior que a data final, verifique')
        return redirect('relatorios')
    despesas = Despesa.objects.all().filter(
        usuario=user, data__range=(data_inicial, data_final)
    ).values('data').annotate(total=Sum('valor'), count=Count('data')).order_by('data')
    if len(despesas) == 0:
        messages.add_message(request, messages.WARNING, 'Nenhum registro para o intervalo de datas informado, tente novamente')
        return redirect('relatorios')
    total = despesas.aggregate(Sum('total'))
    total = f"{total['total__sum']:.2f}"
    for d in despesas:
        d['total'] = f'{d["total"]:.2f}'
    if len(despesas) == 0:
        messages.add_message(request, messages.INFO, 'Sem registros nesse intervalo de datas')
    paginator = Paginator(despesas, 10)
    page = request.GET.get('p')
    despesas = paginator.get_page(page)
    return render(request, 'despesas_por_intervalo.html', {'despesas':despesas, 'data_inicial':data_inicial, 'data_final':data_final, 'data_inicial_sf':data_inicial_sf, 'data_final_sf':data_final_sf, 'total':total})

@login_required(login_url='login')
def despesas_por_tipo(request):
    user = request.user
    despesas = Despesa.objects.all().filter(
        usuario=user
    ).values('tipo__tipo', 'tipo').annotate(total=Sum('valor'), count=Count('tipo')).order_by('-total')
    if len(despesas) == 0:
        messages.add_message(request, messages.WARNING, 'Não existem registros para esse usuário')
        return redirect('home')
    for d in despesas:
        d['total'] = f'{d["total"]:.2f}'
    total = despesas.aggregate(Sum('total'))
    total = f"{total['total__sum']:.2f}"        
    des = Despesa.objects.all().filter(
        usuario=user
    ).values('tipo__tipo', 'tipo').annotate(total=Sum('valor'), count=Count('tipo')).order_by('-total')
    for d in des:
        d['tot'] = round(d['total'])
    #print(despesas)
    paginator = Paginator(despesas, 5)
    page = request.GET.get('p')
    despesas = paginator.get_page(page)
    return render(request, 'despesas_por_tipo.html', {'despesas':despesas, 'des':des, 'total':total})

@login_required(login_url='login')
def ver_despesas_tipo(request, id):
    user = request.user
    tipo = get_object_or_404(TipoDespesa, id=id)
    despesas = Despesa.objects.all().filter(
        usuario=user, tipo=tipo
    ).order_by('-data')
    if len(despesas) == 0:
        messages.add_message(request, messages.WARNING, 'Não existem registros para esse usuário')
        return redirect('home')
    total = despesas.aggregate(Sum('valor'))
    total = f"{total['valor__sum']:.2f}"
    paginator = Paginator(despesas, 10)
    page = request.GET.get('p')
    despesas = paginator.get_page(page)
    return render(request, 'ver_despesas_tipo.html', {'despesas':despesas, 'tipo':tipo, 'total':total})

@login_required(login_url='login')
def despesas_por_tipo_intervalo(request):
    user = request.user
    data_inicial_sf = request.GET.get('data_inicial_tipo')
    data_final_sf = request.GET.get('data_final_tipo')
    #print(data_inicial_sf)
    #print(data_final_sf)
    data_inicial = datetime.strptime(data_inicial_sf, '%Y-%m-%d')
    data_final = datetime.strptime(data_final_sf, '%Y-%m-%d')
    if data_inicial > data_final:
        messages.add_message(request, messages.WARNING, 'Data inicial não pode ser maior que a data final, verifique')
        return redirect('relatorios')
    despesas = Despesa.objects.all().filter(
        usuario=user, data__range=(data_inicial, data_final)
    ).values('tipo__tipo', 'tipo').annotate(total=Sum('valor'), count=Count('tipo')).order_by('-total')
    if len(despesas) == 0:
        messages.add_message(request, messages.WARNING, 'Nenhum registro para o intervalo de datas informado, tente novamente')
        return redirect('relatorios')
    for d in despesas:
        d['tot'] = round(d['total'])
        d['total'] = f'{d["total"]:.2f}'
    total = despesas.aggregate(Sum('total'))
    total = f"{total['total__sum']:.2f}"
    des = Despesa.objects.all().filter(
        usuario=user, data__range=(data_inicial, data_final)
    ).values('tipo__tipo', 'tipo').annotate(total=Sum('valor'), count=Count('tipo')).order_by('-total')
    for d in des:
        d['tot'] = round(d['total'])
    if len(despesas) == 0:
        messages.add_message(request, messages.INFO, 'Sem registros nesse intervalo de datas')
    paginator = Paginator(despesas, 5)
    page = request.GET.get('p')
    despesas = paginator.get_page(page)
    return render(request, 'despesas_por_tipo_intervalo.html', {'despesas':despesas, 'data_inicial':data_inicial, 'data_final':data_final, 'data_inicial_sf':data_inicial_sf, 'data_final_sf':data_final_sf, 'des':des, 'total':total})

@login_required(login_url='login')
def ver_despesas_tipo_intervalo(request, id):
    user = request.user
    data_inicial_sf = request.GET.get('data_inicial_tipo')
    data_final_sf = request.GET.get('data_final_tipo')
    #print(data_inicial_sf)
    #print(data_final_sf)
    data_inicial = datetime.strptime(data_inicial_sf, '%Y-%m-%d')
    data_final = datetime.strptime(data_final_sf, '%Y-%m-%d')
    tipo = get_object_or_404(TipoDespesa, id=id)
    despesas = Despesa.objects.all().filter(
        usuario=user, tipo=tipo, data__range=(data_inicial, data_final)
    ).order_by('-data')
    if len(despesas) == 0:
        messages.add_message(request, messages.WARNING, 'Não existem registros para esse usuário')
        return redirect('home')
    total = despesas.aggregate(Sum('valor'))
    total = f"{total['valor__sum']:.2f}"
    paginator = Paginator(despesas, 10)
    page = request.GET.get('p')
    despesas = paginator.get_page(page)
    return render(request, 'ver_despesas_tipo.html', {'despesas':despesas, 'tipo':tipo, 'data_inicial_sf':data_inicial_sf,'data_final_sf':data_final_sf, 'total':total})

@login_required(login_url='login')
def despesas_por_grupo(request):
    user = request.user
    despesas = Despesa.objects.all().filter(
        usuario=user
    ).values('tipo__grupo__grupo', 'tipo__grupo').annotate(total=Sum('valor'), count=Count('tipo__grupo')).order_by('-total')
    if len(despesas) == 0:
        messages.add_message(request, messages.WARNING, 'Não existem registros para esse usuário')
        return redirect('home')
    for d in despesas:
        d['tot'] = round(d['total'])
        d['total'] = f'{d["total"]:.2f}'
    total = despesas.aggregate(Sum('total'))
    total = f"{total['total__sum']:.2f}"
    des = Despesa.objects.all().filter(
        usuario=user
    ).values('tipo__grupo__grupo', 'tipo__grupo').annotate(total=Sum('valor'), count=Count('tipo__grupo')).order_by('-total')
    for d in des:
        d['tot'] = round(d['total'])
    paginator = Paginator(despesas, 5)
    page = request.GET.get('p')
    despesas = paginator.get_page(page)
    return render(request, 'despesas_por_grupo.html', {'despesas':despesas, 'des':des, 'total':total})

@login_required(login_url='login')
def ver_despesas_grupo(request, id):
    user = request.user
    grupo = get_object_or_404(GrupoDespesa, id=id)
    despesas = Despesa.objects.all().filter(
        usuario=user, tipo__grupo=grupo
    ).order_by('-data')
    if len(despesas) == 0:
        messages.add_message(request, messages.WARNING, 'Não existem registros para esse usuário')
        return redirect('home')
    total = despesas.aggregate(Sum('valor'))
    total = f"{total['valor__sum']:.2f}"
    print(total)
    paginator = Paginator(despesas, 10)
    page = request.GET.get('p')
    despesas = paginator.get_page(page)
    return render(request, 'ver_despesas_grupo_tipo.html', {'despesas':despesas, 'grupo':grupo, 'total':total})

@login_required(login_url='login')
def despesas_por_grupo_intervalo(request):
    user = request.user
    data_inicial_sf = request.GET.get('data_inicial_grupo')
    data_final_sf = request.GET.get('data_final_grupo')
    #print(data_inicial_sf)
    #print(data_final_sf)
    data_inicial = datetime.strptime(data_inicial_sf, '%Y-%m-%d')
    data_final = datetime.strptime(data_final_sf, '%Y-%m-%d')
    if data_inicial > data_final:
        messages.add_message(request, messages.WARNING, 'Data inicial não pode ser maior que a data final, verifique')
        return redirect('relatorios')
    despesas = Despesa.objects.all().filter(
        usuario=user, data__range=(data_inicial, data_final)
    ).values('tipo__grupo__grupo', 'tipo__grupo').annotate(total=Sum('valor'), count=Count('tipo__grupo')).order_by('-total')
    if len(despesas) == 0:
        messages.add_message(request, messages.WARNING, 'Nenhum registro para o intervalo de datas informado, tente novamente')
        return redirect('relatorios')
    total = despesas.aggregate(Sum('total'))
    total = f"{total['total__sum']:.2f}"
    for d in despesas:
        d['tot'] = round(d['total'])
        d['total'] = f'{d["total"]:.2f}'
    des = Despesa.objects.all().filter(
        usuario=user, data__range=(data_inicial, data_final)
    ).values('tipo__grupo__grupo', 'tipo__grupo').annotate(total=Sum('valor'), count=Count('tipo__grupo')).order_by('-total')
    for d in des:
        d['tot'] = round(d['total'])
    if len(despesas) == 0:
        messages.add_message(request, messages.INFO, 'Sem registros nesse intervalo de datas')
    paginator = Paginator(despesas, 5)
    page = request.GET.get('p')
    despesas = paginator.get_page(page)
    return render(request, 'despesas_por_grupo_intervalo.html', {'despesas':despesas, 'data_inicial':data_inicial, 'data_final':data_final, 'data_inicial_sf':data_inicial_sf, 'data_final_sf':data_final_sf, 'des':des, 'total':total})

@login_required(login_url='login')
def ver_despesas_grupo_intervalo(request, id):
    user = request.user
    data_inicial_sf = request.GET.get('data_inicial_grupo')
    data_final_sf = request.GET.get('data_final_grupo')
    #print(data_inicial_sf)
    #print(data_final_sf)
    data_inicial = datetime.strptime(data_inicial_sf, '%Y-%m-%d')
    data_final = datetime.strptime(data_final_sf, '%Y-%m-%d')
    grupo = get_object_or_404(GrupoDespesa, id=id)
    despesas = Despesa.objects.all().filter(
        usuario=user, tipo__grupo=grupo, data__range=(data_inicial, data_final)
    ).order_by('-data')
    if len(despesas) == 0:
        messages.add_message(request, messages.WARNING, 'Não existem registros para esse usuário')
        return redirect('home')
    total = despesas.aggregate(Sum('valor'))
    total = f"{total['valor__sum']:.2f}"
    print(total)
    paginator = Paginator(despesas, 10)
    page = request.GET.get('p')
    despesas = paginator.get_page(page)
    return render(request, 'ver_despesas_grupo.html', {'despesas':despesas, 'grupo':grupo, 'data_inicial_sf':data_inicial_sf,'data_final_sf':data_final_sf,'total':total})

@login_required(login_url='login')
def despesas_por_fpag(request):
    user = request.user
    despesas = Despesa.objects.all().filter(
        usuario=user
    ).values('fpag__forma', 'fpag').annotate(total=Sum('valor'), count=Count('fpag')).order_by('-total')
    if len(despesas) == 0:
        messages.add_message(request, messages.WARNING, 'Não existem registros para esse usuário')
        return redirect('home')
    total = despesas.aggregate(Sum('total'))
    total = f"{total['total__sum']:.2f}"
    for d in despesas:
        d['tot'] = round(d['total'])
        d['total'] = f'{d["total"]:.2f}'
    des = Despesa.objects.all().filter(
        usuario=user
    ).values('fpag__forma', 'fpag').annotate(total=Sum('valor'), count=Count('fpag')).order_by('-total')
    for d in des:
        d['tot'] = round(d['total'])
    paginator = Paginator(despesas, 5)
    page = request.GET.get('p')
    despesas = paginator.get_page(page)
    return render(request, 'despesas_por_fpag.html', {'despesas':despesas, 'des':des, 'total':total})

@login_required(login_url='login')
def ver_despesas_fpag(request, id):
    user = request.user
    fpag = get_object_or_404(FormaPagamento, id=id)
    despesas = Despesa.objects.all().filter(
        usuario=user, fpag=fpag
    ).order_by('-data')
    if len(despesas) == 0:
        messages.add_message(request, messages.WARNING, 'Não existem registros para esse usuário')
        return redirect('home')
    total = despesas.aggregate(Sum('valor'))
    total = f"{total['valor__sum']:.2f}"
    paginator = Paginator(despesas, 10)
    page = request.GET.get('p')
    despesas = paginator.get_page(page)
    return render(request, 'ver_despesas_fpag.html', {'despesas':despesas, 'fpag':fpag, 'total':total})

@login_required(login_url='login')
def despesas_por_fpag_intervalo(request):
    user = request.user
    data_inicial_sf = request.GET.get('data_inicial_tipo')
    data_final_sf = request.GET.get('data_final_tipo')
    #print(data_inicial_sf)
    #print(data_final_sf)
    data_inicial = datetime.strptime(data_inicial_sf, '%Y-%m-%d')
    data_final = datetime.strptime(data_final_sf, '%Y-%m-%d')
    if data_inicial > data_final:
        messages.add_message(request, messages.WARNING, 'Data inicial não pode ser maior que a data final, verifique')
        return redirect('relatorios')
    despesas = Despesa.objects.all().filter(
        usuario=user, data__range=(data_inicial, data_final)
    ).values('fpag__forma', 'fpag').annotate(total=Sum('valor'), count=Count('fpag')).order_by('-total')
    if len(despesas) == 0:
        messages.add_message(request, messages.WARNING, 'Nenhum registro para o intervalo de datas informado, tente novamente')
        return redirect('relatorios')
    total = despesas.aggregate(Sum('total'))
    total = f"{total['total__sum']:.2f}"
    for d in despesas:
        d['tot'] = round(d['total'])
        d['total'] = f'{d["total"]:.2f}'
    des = Despesa.objects.all().filter(
        usuario=user, data__range=(data_inicial, data_final)
    ).values('fpag__forma', 'fpag').annotate(total=Sum('valor'), count=Count('fpag')).order_by('-total')
    for d in des:
        d['tot'] = round(d['total'])
    if len(despesas) == 0:
        messages.add_message(request, messages.INFO, 'Sem registros nesse intervalo de datas')
    paginator = Paginator(despesas, 5)
    page = request.GET.get('p')
    despesas = paginator.get_page(page)
    return render(request, 'despesas_por_fpag_intervalo.html', {'despesas':despesas, 'data_inicial':data_inicial, 'data_final':data_final, 'data_inicial_sf':data_inicial_sf, 'data_final_sf':data_final_sf, 'des':des, 'total':total})

@login_required(login_url='login')
def ver_despesas_fpag_intervalo(request, id):
    user = request.user
    data_inicial_sf = request.GET.get('data_inicial_tipo')
    data_final_sf = request.GET.get('data_final_tipo')
    #print(data_inicial_sf)
    #print(data_final_sf)
    data_inicial = datetime.strptime(data_inicial_sf, '%Y-%m-%d')
    data_final = datetime.strptime(data_final_sf, '%Y-%m-%d')
    fpag = get_object_or_404(FormaPagamento, id=id)
    despesas = Despesa.objects.all().filter(
        usuario=user, fpag=fpag, data__range=(data_inicial, data_final)
    ).order_by('-data')
    if len(despesas) == 0:
        messages.add_message(request, messages.WARNING, 'Não existem registros para esse usuário')
        return redirect('home')
    total = despesas.aggregate(Sum('valor'))
    total = f"{total['valor__sum']:.2f}"
    paginator = Paginator(despesas, 10)
    page = request.GET.get('p')
    despesas = paginator.get_page(page)
    return render(request, 'ver_despesas_fpag.html', {'despesas':despesas, 'fpag':fpag, 'data_inicial_sf':data_inicial_sf,'data_final_sf':data_final_sf, 'total':total})
