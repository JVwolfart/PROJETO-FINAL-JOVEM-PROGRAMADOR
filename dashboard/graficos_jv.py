def resumo_ano(despesas):
    ano = [
    {"mes":"Janeiro", "total": 0, "registros":0, "cor":"#006400"},
    {"mes":"Fevereiro", "total": 0, "registros":0, "cor":"#00FF00"},
    {"mes":"Março", "total": 0, "registros":0, "cor":"#DAA520"},
    {"mes":"Abril", "total": 0, "registros":0, "cor":"#A0522D"},
    {"mes":"Maio", "total": 0, "registros":0, "cor":"#F4A460"},
    {"mes":"Junho", "total": 0, "registros":0, "cor":"#8A2BE2"},
    {"mes":"Julho", "total": 0, "registros":0, "cor":"#4B0082"},
    {"mes":"Agosto", "total": 0, "registros":0, "cor":"#DC143C"},
    {"mes":"Setembro", "total": 0, "registros":0, "cor":"#8B0000"},
    {"mes":"Outubro", "total": 0, "registros":0, "cor":"#FF4500"},
    {"mes":"Novembro", "total": 0, "registros":0, "cor":"#FFFF00"},
    {"mes":"Dezembro", "total": 0, "registros":0, "cor":"#0000FF"},
    ]

    grafico = [
    {"mes":"Janeiro", "total": 0, "registros":0, "cor":"#006400"},
    {"mes":"Fevereiro", "total": 0, "registros":0, "cor":"#00FF00"},
    {"mes":"Março", "total": 0, "registros":0, "cor":"#DAA520"},
    {"mes":"Abril", "total": 0, "registros":0, "cor":"#A0522D"},
    {"mes":"Maio", "total": 0, "registros":0, "cor":"#F4A460"},
    {"mes":"Junho", "total": 0, "registros":0, "cor":"#8A2BE2"},
    {"mes":"Julho", "total": 0, "registros":0, "cor":"#4B0082"},
    {"mes":"Agosto", "total": 0, "registros":0, "cor":"#DC143C"},
    {"mes":"Setembro", "total": 0, "registros":0, "cor":"#8B0000"},
    {"mes":"Outubro", "total": 0, "registros":0, "cor":"#FF4500"},
    {"mes":"Novembro", "total": 0, "registros":0, "cor":"#FFFF00"},
    {"mes":"Dezembro", "total": 0, "registros":0, "cor":"#0000FF"},
    ]
    total = 0
    resumo = {'grafico':grafico, 'ano':ano, 'total':total}
    for d in despesas:
        d['total'] = round(d['total'], 2)
        resumo['total'] += d['total']
        if d['data__month'] == 1:
            resumo['grafico'][0]['total'] = int(d['total'])
            resumo['ano'][0]['total'] = d['total']
            resumo['ano'][0]['registros'] = d['count']
        
        elif d['data__month'] == 2:
            resumo['grafico'][1]['total'] = int(d['total'])
            resumo['ano'][1]['total'] = d['total']
            resumo['ano'][1]['registros'] = d['count']

        elif d['data__month'] == 3:
            resumo['grafico'][2]['total'] = int(d['total'])
            resumo['ano'][2]['total'] = d['total']
            resumo['ano'][2]['registros'] = d['count']

        elif d['data__month'] == 4:
            resumo['grafico'][3]['total'] = int(d['total'])
            resumo['ano'][3]['total'] = d['total']
            resumo['ano'][3]['registros'] = d['count']

        elif d['data__month'] == 5:
            resumo['grafico'][4]['total'] = int(d['total'])
            resumo['ano'][4]['total'] = d['total']
            resumo['ano'][4]['registros'] = d['count']

        elif d['data__month'] == 6:
            resumo['grafico'][5]['total'] = int(d['total'])
            resumo['ano'][5]['total'] = d['total']
            resumo['ano'][5]['registros'] = d['count']

        elif d['data__month'] == 7:
            resumo['grafico'][6]['total'] = int(d['total'])
            resumo['ano'][6]['total'] = d['total']
            resumo['ano'][6]['registros'] = d['count']
        
        elif d['data__month'] == 8:
            resumo['grafico'][7]['total'] = int(d['total'])
            resumo['ano'][7]['total'] = d['total']
            resumo['ano'][7]['registros'] = d['count']
        
        elif d['data__month'] == 9:
            resumo['grafico'][8]['total'] = int(d['total'])
            resumo['ano'][8]['total'] = d['total']
            resumo['ano'][8]['registros'] = d['count']
        
        elif d['data__month'] == 10:
            resumo['grafico'][9]['total'] = int(d['total'])
            resumo['ano'][9]['total'] = d['total']
            resumo['ano'][9]['registros'] = d['count']
        
        elif d['data__month'] == 11:
            resumo['grafico'][10]['total'] = int(d['total'])
            resumo['ano'][10]['total'] = d['total']
            resumo['ano'][10]['registros'] = d['count']

        elif d['data__month'] == 12:
            resumo['grafico'][11]['total'] = int(d['total'])
            resumo['ano'][11]['total'] = d['total']
            resumo['ano'][11]['registros'] = d['count']
    
    resumo['total'] = round(resumo['total'], 2)
    return resumo