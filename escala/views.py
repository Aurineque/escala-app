from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages # Importamos o "mensageiro" do Django
from .models import Evento, Escala  # Precisamos importar a Escala aqui também
from .forms import EscalaForm
from django.utils import timezone  # Precisamos disso para saber a data de hoje

def lista_eventos(request):
    agora = timezone.now()
    
    # 1. Definimos o início: dia 1º do mês atual, à meia-noite
    inicio_mes = agora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # 2. Descobrimos qual é o próximo mês (com proteção para a virada de ano!)
    if agora.month == 12:
        mes_que_vem = 1
        ano_que_vem = agora.year + 1
    else:
        mes_que_vem = agora.month + 1
        ano_que_vem = agora.year
        
    # 3. Definimos o limite: dia 7 do próximo mês, no finalzinho do dia
    limite_dias = agora.replace(
        year=ano_que_vem, 
        month=mes_que_vem, 
        day=7, 
        hour=23, 
        minute=59, 
        second=59
    )
    
    # 4. Filtramos criando um "sanduíche" de datas
    eventos = Evento.objects.filter(
        data__gte=inicio_mes,   # gte = Greater Than or Equal (Maior ou igual ao dia 1º)
        data__lte=limite_dias   # lte = Less Than or Equal (Menor ou igual ao dia 7 do proximo mês)
    ).order_by('data')
    
    return render(request, 'escala/lista_eventos.html', {'eventos': eventos})

def voluntariar(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    
    if request.method == 'POST':
        form = EscalaForm(request.POST)
        
        if form.is_valid():
            membro = form.cleaned_data['membro']
            
            # --- REGRA 1: Impede de se escalar duas vezes no MESMO evento ---
            if Escala.objects.filter(evento=evento, membro=membro).exists():
                messages.error(request, f"Ops! {membro.nome} já está escalado(a) neste evento.")
                return redirect('voluntariar', evento_id=evento.id)
            
            # --- REGRA 2: Limite máximo escalas no mês ---
            escalas_no_mes = Escala.objects.filter(
                membro=membro,
                evento__data__month=evento.data.month,
                evento__data__year=evento.data.year
            ).count()
            
            if escalas_no_mes >= 6:
                messages.error(request, f"{membro.nome} já atingiu o limite de 6 escalas para este mês!")
                return redirect('voluntariar', evento_id=evento.id) 
            
            # --- Se passou pelos dois bloqueios, salva com sucesso ---
            escala = form.save(commit=False)
            escala.evento = evento
            escala.save()
            
            messages.success(request, "Presença confirmada com sucesso!")
            return redirect('lista_eventos')
            
    else:
        form = EscalaForm()
        
    return render(request, 'escala/voluntariar.html', {'form': form, 'evento': evento})