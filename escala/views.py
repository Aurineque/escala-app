from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages # Importamos o "mensageiro" do Django
from .models import Evento, Escala  # Precisamos importar a Escala aqui também
from .forms import EscalaForm
from django.utils import timezone  # Precisamos disso para saber a data de hoje

def lista_eventos(request):
    agora = timezone.now()
    
    # Filtramos onde o mês e o ano da 'data' sejam iguais aos atuais
    eventos = Evento.objects.filter(
        data__month=agora.month,
        data__year=agora.year
    ).order_by('data') # Mantém a ordem cronológica
    
    return render(request, 'escala/lista_eventos.html', {'eventos': eventos})

def voluntariar(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    
    if request.method == 'POST':
        form = EscalaForm(request.POST) # Lembre-se de usar o nome correto do seu form
        
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