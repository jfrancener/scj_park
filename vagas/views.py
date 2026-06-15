from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from .models import Estacionamento

@ensure_csrf_cookie
def index(request):
    estacionamento = Estacionamento.obter_instancia()
    context = {
        'estacionamento': estacionamento
    }
    return render(request, 'vagas/index.html', context)

@require_GET
def status_vagas(request):
    estacionamento = Estacionamento.obter_instancia()
    return JsonResponse({
        'vagas_totais': estacionamento.vagas_totais,
        'vagas_ocupadas': estacionamento.vagas_ocupadas,
        'vagas_disponiveis': estacionamento.vagas_disponiveis
    })

@require_POST
def registrar_entrada(request):
    estacionamento = Estacionamento.obter_instancia()
    
    if estacionamento.vagas_ocupadas < estacionamento.vagas_totais:
        estacionamento.vagas_ocupadas += 1
        estacionamento.save()
        status = 'success'
        mensagem = 'Entrada registrada com sucesso.'
    else:
        status = 'error'
        mensagem = 'Estacionamento lotado!'
        
    return JsonResponse({
        'status': status,
        'mensagem': mensagem,
        'vagas_totais': estacionamento.vagas_totais,
        'vagas_ocupadas': estacionamento.vagas_ocupadas,
        'vagas_disponiveis': estacionamento.vagas_disponiveis
    })

@require_POST
def registrar_saida(request):
    estacionamento = Estacionamento.obter_instancia()
    
    if estacionamento.vagas_ocupadas > 0:
        estacionamento.vagas_ocupadas -= 1
        estacionamento.save()
        status = 'success'
        mensagem = 'Saída registrada com sucesso.'
    else:
        status = 'error'
        mensagem = 'Estacionamento já está vazio!'
        
    return JsonResponse({
        'status': status,
        'mensagem': mensagem,
        'vagas_totais': estacionamento.vagas_totais,
        'vagas_ocupadas': estacionamento.vagas_ocupadas,
        'vagas_disponiveis': estacionamento.vagas_disponiveis
    })

@require_POST
def configurar_estacionamento(request):
    try:
        # Tenta ler do body JSON ou form data
        if request.content_type == 'application/json':
            dados = json.loads(request.body)
            vagas_totais = int(dados.get('vagas_totais', 100))
            vagas_ocupadas = dados.get('vagas_ocupadas', None)
        else:
            vagas_totais = int(request.POST.get('vagas_totais', 100))
            vagas_ocupadas = request.POST.get('vagas_ocupadas', None)
            
        if vagas_totais < 0:
            return JsonResponse({'status': 'error', 'mensagem': 'O total de vagas não pode ser negativo.'}, status=400)
            
        estacionamento = Estacionamento.obter_instancia()
        estacionamento.vagas_totais = vagas_totais
        
        if vagas_ocupadas is not None:
            vagas_ocupadas_int = int(vagas_ocupadas)
            if 0 <= vagas_ocupadas_int <= vagas_totais:
                estacionamento.vagas_ocupadas = vagas_ocupadas_int
            else:
                return JsonResponse({'status': 'error', 'mensagem': 'Vagas ocupadas inválidas.'}, status=400)
        
        # Garante que as ocupadas não fiquem maiores que as totais novas
        if estacionamento.vagas_ocupadas > vagas_totais:
            estacionamento.vagas_ocupadas = vagas_totais
            
        estacionamento.save()
        
        return JsonResponse({
            'status': 'success',
            'mensagem': 'Capacidade configurada com sucesso.',
            'vagas_totais': estacionamento.vagas_totais,
            'vagas_ocupadas': estacionamento.vagas_ocupadas,
            'vagas_disponiveis': estacionamento.vagas_disponiveis
        })
    except (ValueError, TypeError, json.JSONDecodeError) as e:
        return JsonResponse({'status': 'error', 'mensagem': f'Dados inválidos: {str(e)}'}, status=400)
