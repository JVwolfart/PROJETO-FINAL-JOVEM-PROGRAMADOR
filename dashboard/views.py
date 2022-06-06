from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.aggregates import Count, Sum
from despesas.models import Despesa
from cadastros.models import GrupoDespesa
from datetime import datetime
from django.core.paginator import Paginator
from .graficos_jv import resumo_ano

@login_required(login_url='login')
def dashboard(request):
    hoje = datetime.today()
    mes = hoje.month
    ano = hoje.year
    user = request.user
    total_full = 0
    despesas_full = Despesa.objects.all().filter(
        usuario=user
    ).values('data__year').annotate(total=Sum('valor'), count=Count('data__year')).order_by('data__year')
    if len(despesas_full) == 0:
        total_full = 0
        messages.add_message(request, messages.INFO, f'Sem registros para listar')
        print(total_full)
        return render(request, 'dashboard.html', {'total_full':total_full})
    for d in despesas_full:
        d['total'] = round(d['total'], 2)
        total_full += d['total']
        d['tot'] = int(d['total'])
    atividade = Despesa.objects.all().filter(
        usuario=user
    ).values('data__month', 'data__year').annotate(count=Count('data__month')).order_by('-data__year', '-data__month')
    ativ_ano = Despesa.objects.all().filter(
        usuario=user
    ).values('data__year').annotate(count=Count('data__year')).order_by('-data__year')
    for a in atividade:
        a['mes'] = str(a['data__month'])
        a['mes'] = datetime.strptime(a['mes'], '%m')        
    despesas = Despesa.objects.all().filter(
        usuario=user, data__month=mes, data__year=ano
    ).values('tipo__grupo__grupo', 'tipo__grupo').annotate(total=Sum('valor'), count=Count('tipo__grupo')).order_by('-total')
    registros = 0
    despesas_ano = Despesa.objects.all().filter(
        usuario=user, data__year=ano
    ).values('data__month').annotate(total=Sum('valor'), count=Count('data__month'))
    if len(despesas_ano) == 0:
        despesas = []
        des = []
        total = 0
        grafico_ano = {'total':0}
        messages.add_message(request, messages.INFO, f"Nenhuma despesa registrada nesse ano para {user.first_name} {user.last_name}, clique em lançar despesas e inclua registros para visualizar os resultados no dashboard")
        return render(request, 'dashboard.html', {'total':total, 'grafico_ano':grafico_ano, 'ativ_ano':ativ_ano, 'total_full':total_full, 'despesas_full':despesas_full, 'atividade':atividade})
    grafico_ano = resumo_ano(despesas_ano)
    if len(despesas) == 0:
        messages.add_message(request, messages.INFO, 'Nenhuma despesa registrada nesse mês')
        despesas = []
        des = []
        total = 0
        return render(request, 'dashboard.html', {'despesas':despesas, 'des':des, 'total':total, 'grafico_ano':grafico_ano, 'ativ_ano':ativ_ano, 'total_full':total_full, 'despesas_full':despesas_full, 'atividade':atividade})
    for d in despesas:
        registros += d['count']
        d['tot'] = round(d['total'])
        d['total'] = f'{d["total"]:.2f}'
    total = despesas.aggregate(Sum('total'))
    total = f"{total['total__sum']:.2f}"
    des = Despesa.objects.all().filter(
        usuario=user, data__month=mes, data__year=ano
    ).values('tipo__grupo__grupo', 'tipo__grupo').annotate(total=Sum('valor'), count=Count('tipo__grupo')).order_by('-total')
    for d in des:
        d['tot'] = round(d['total'])
    return render(request, 'dashboard.html', {'despesas':despesas, 'des':des, 'total':total, 'atividade':atividade, 'grafico_ano':grafico_ano, 'registros':registros, 'ativ_ano':ativ_ano, 'despesas_full':despesas_full, 'total_full':total_full})

@login_required(login_url='login')
def despesas_dashboard(request, id):
    hoje = datetime.today()
    mes = hoje.month
    ano = hoje.year
    user = request.user
    grupo = get_object_or_404(GrupoDespesa, id=id)
    if not grupo.padrao and grupo.usuario != user:
        messages.add_message(request, messages.ERROR, 'Esse grupo não pertence a esse usuário')
        return redirect('home')
    despesas = Despesa.objects.all().filter(
        usuario=user, tipo__grupo=grupo, data__month=mes, data__year=ano
    ).order_by('-data')
    if len(despesas) == 0:
        messages.add_message(request, messages.INFO, 'Nenhuma despesa registrada para esse grupo no mês corrente')
        return redirect('home')
    total = despesas.aggregate(Sum('valor'))
    total = f"{total['valor__sum']:.2f}"
    paginator = Paginator(despesas, 10)
    page = request.GET.get('p')
    despesas = paginator.get_page(page)
    return render(request, 'ver_despesas_grupo_dashboard.html', {'despesas':despesas, 'grupo':grupo, 'total':total})

@login_required(login_url='login')
def dashboard_mes(request):
    user = request.user
    periodo = request.POST.get("atividade")
    if not periodo or periodo == "":
        messages.add_message(request, messages.WARNING, 'Nenhum período selecionado, verifique')
        return redirect('home')
    else:
        periodo = periodo.split(',')
        mes = int(periodo[0])
        ano = int(periodo[1])
        atividade = Despesa.objects.all().filter(
            usuario=user
        ).values('data__month', 'data__year').annotate(count=Count('data__month')).order_by('-data__year', '-data__month')
        for a in atividade:
            a['mes'] = str(a['data__month'])
            a['mes'] = datetime.strptime(a['mes'], '%m')
        despesas = Despesa.objects.all().filter(
            usuario=user, data__month=mes, data__year=ano
        ).values('tipo__grupo__grupo', 'tipo__grupo').annotate(total=Sum('valor'), count=Count('tipo__grupo')).order_by('-total')
        if len(despesas) == 0:
            messages.add_message(request, messages.INFO, 'Nenhuma despesa registrada nesse mês')
            despesas = []
            des = []
            total = 0
            return render(request, 'dashboard.html', {'despesas':despesas, 'des':des, 'total':total})
        for d in despesas:
            d['tot'] = round(d['total'])
            d['total'] = f'{d["total"]:.2f}'
        total = despesas.aggregate(Sum('total'))
        total = f"{total['total__sum']:.2f}"
        des = Despesa.objects.all().filter(
            usuario=user, data__month=mes, data__year=ano
        ).values('tipo__grupo__grupo', 'tipo__grupo').annotate(total=Sum('valor'), count=Count('tipo__grupo')).order_by('-total')
        for d in des:
            d['tot'] = round(d['total'])
        return render(request, 'dashboard_mes.html', {'despesas':despesas, 'des':des, 'total':total, 'atividade':atividade, 'mes':mes, 'ano':ano})

@login_required(login_url='login')
def despesas_dashboard_mes(request, id):
    user = request.user
    grupo = get_object_or_404(GrupoDespesa, id=id)
    mes = request.GET.get('mes')
    ano = request.GET.get('ano')
    if not mes or mes == '' or not ano or ano == '':
        messages.add_message(request, messages.WARNING, 'Mês e ano não informados, verifique')
        return redirect('home')
    try:        
        mes = int(mes)
        ano = int(ano)
    except ValueError:
        messages.add_message(request, messages.ERROR, 'Dados informados inválidos')
        return redirect('home')
    if mes < 1 or mes > 12:
        messages.add_message(request, messages.ERROR, 'Mês não existe')
        return redirect('home')

    if len(str(ano)) != 4:
        messages.add_message(request, messages.ERROR, 'Ano inválido')
        return redirect('home')

    else:
        despesas = Despesa.objects.all().filter(
        usuario=user, tipo__grupo=grupo, data__month=mes, data__year=ano
        ).order_by('-data')
        if len(despesas) == 0:
            messages.add_message(request, messages.INFO, 'Nenhuma despesa registrada nesse período')
            return redirect('home')
        total = despesas.aggregate(Sum('valor'))
        total = f"{total['valor__sum']:.2f}"
        paginator = Paginator(despesas, 10)
        page = request.GET.get('p')
        despesas = paginator.get_page(page)
        return render(request, 'ver_despesas_grupo_dashboard.html', {'despesas':despesas, 'grupo':grupo, 'total':total, 'mes':mes, 'ano':ano})


@login_required(login_url='login')
def dashboard_ano(request):
    user = request.user
    ano = request.POST.get('ativ_ano')
    if ano == '':
        messages.add_message(request, messages.WARNING, 'Nenhum ano selecionado, verifique e tente novamente')
        return redirect('home')
    despesas = Despesa.objects.all().filter(
        usuario=user, data__year=ano
    ).values('data__month').annotate(total=Sum('valor'), count=Count('data__month'))
    if len(despesas) == 0:
        messages.add_message(request, messages.INFO, "Nenhuma despesa registrada nesse ano")
        return redirect('home')
    grafico = resumo_ano(despesas)
    
    return render(request, 'dashboard_ano.html', {'grafico':grafico, 'ano':ano})


@login_required(login_url='login')
def dashboard_print(request):
    hoje = datetime.today()
    mes = hoje.month
    ano = hoje.year
    user = request.user
    total_full = 0
    despesas_full = Despesa.objects.all().filter(
        usuario=user
    ).values('data__year').annotate(total=Sum('valor'), count=Count('data__year')).order_by('data__year')
    if len(despesas_full) == 0:
        total_full = 0
        messages.add_message(request, messages.INFO, f'Sem registros para listar')
        print(total_full)
        return render(request, 'print/dashboard.html', {'total_full':total_full})
    for d in despesas_full:
        d['total'] = round(d['total'], 2)
        total_full += d['total']
        d['tot'] = int(d['total'])
    atividade = Despesa.objects.all().filter(
        usuario=user
    ).values('data__month', 'data__year').annotate(count=Count('data__month')).order_by('-data__year', '-data__month')
    ativ_ano = Despesa.objects.all().filter(
        usuario=user
    ).values('data__year').annotate(count=Count('data__year')).order_by('-data__year')
    for a in atividade:
        a['mes'] = str(a['data__month'])
        a['mes'] = datetime.strptime(a['mes'], '%m')
    despesas = Despesa.objects.all().filter(
        usuario=user, data__month=mes, data__year=ano
    ).values('tipo__grupo__grupo', 'tipo__grupo').annotate(total=Sum('valor'), count=Count('tipo__grupo')).order_by('-total')
    registros = 0
    despesas_ano = Despesa.objects.all().filter(
        usuario=user, data__year=ano
    ).values('data__month').annotate(total=Sum('valor'), count=Count('data__month'))
    if len(despesas_ano) == 0:
        despesas = []
        des = []
        total = 0
        grafico_ano = {'total':0}
        messages.add_message(request, messages.INFO, f"Nenhuma despesa registrada nesse ano para {user.first_name} {user.last_name}, clique em lançar despesas e inclua registros para visualizar os resultados no dashboard")
        return render(request, 'print/dashboard.html', {'total':total, 'grafico_ano':grafico_ano, 'ativ_ano':ativ_ano, 'total_full':total_full, 'despesas_full':despesas_full, 'atividade':atividade})
    grafico_ano = resumo_ano(despesas_ano)
    if len(despesas) == 0:
        messages.add_message(request, messages.INFO, 'Nenhuma despesa registrada nesse mês')
        despesas = []
        des = []
        total = 0
        return render(request, 'print/dashboard.html', {'despesas':despesas, 'des':des, 'total':total, 'grafico_ano':grafico_ano, 'ativ_ano':ativ_ano, 'total_full':total_full, 'despesas_full':despesas_full, 'atividade':atividade})
    for d in despesas:
        registros += d['count']
        d['tot'] = round(d['total'])
        d['total'] = f'{d["total"]:.2f}'
    total = despesas.aggregate(Sum('total'))
    total = f"{total['total__sum']:.2f}"
    des = Despesa.objects.all().filter(
        usuario=user, data__month=mes, data__year=ano
    ).values('tipo__grupo__grupo', 'tipo__grupo').annotate(total=Sum('valor'), count=Count('tipo__grupo')).order_by('-total')
    for d in des:
        d['tot'] = round(d['total'])
    return render(request, 'print/dashboard.html', {'despesas':despesas, 'des':des, 'total':total, 'atividade':atividade, 'grafico_ano':grafico_ano, 'registros':registros, 'ativ_ano':ativ_ano, 'despesas_full':despesas_full, 'total_full':total_full})

@login_required(login_url='login')
def dashboard_mes_print(request):
    user = request.user
    mes = request.GET.get('mes')
    ano = request.GET.get('ano')
    if not mes or not ano:
        messages.add_message(request, messages.WARNING, 'Nenhum período selecionado, verifique')
        return redirect('home')
    else:
        mes = int(mes)
        ano = int(ano)
        despesas = Despesa.objects.all().filter(
            usuario=user, data__month=mes, data__year=ano
        ).values('tipo__grupo__grupo', 'tipo__grupo').annotate(total=Sum('valor'), count=Count('tipo__grupo')).order_by('-total')
        if len(despesas) == 0:
            messages.add_message(request, messages.INFO, 'Nenhuma despesa registrada nesse mês')
            despesas = []
            des = []
            total = 0
            return redirect('home')
        for d in despesas:
            d['tot'] = round(d['total'])
            d['total'] = f'{d["total"]:.2f}'
        total = despesas.aggregate(Sum('total'))
        total = f"{total['total__sum']:.2f}"
        des = Despesa.objects.all().filter(
            usuario=user, data__month=mes, data__year=ano
        ).values('tipo__grupo__grupo', 'tipo__grupo').annotate(total=Sum('valor'), count=Count('tipo__grupo')).order_by('-total')
        for d in des:
            d['tot'] = round(d['total'])
        return render(request, 'print/dashboard_mes.html', {'despesas':despesas, 'des':des, 'total':total, 'mes':mes, 'ano':ano})

@login_required(login_url='login')
def dashboard_ano_print(request):
    user = request.user
    ano = request.GET.get('ano')
    if not ano or ano == '':
        messages.add_message(request, messages.WARNING, 'Nenhum ano selecionado, verifique e tente novamente')
        return redirect('home')
    despesas = Despesa.objects.all().filter(
        usuario=user, data__year=ano
    ).values('data__month').annotate(total=Sum('valor'), count=Count('data__month'))
    if len(despesas) == 0:
        messages.add_message(request, messages.INFO, "Nenhuma despesa registrada nesse ano")
        return redirect('home')
    grafico = resumo_ano(despesas)
    
    return render(request, 'print/dashboard_ano.html', {'grafico':grafico, 'ano':ano})