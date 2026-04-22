from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages # Importamos o "mensageiro" do Django
from .models import Evento, Escala  # Precisamos importar a Escala aqui também
from .forms import EscalaForm

def lista_eventos(request):
    eventos = Evento.objects.all().order_by('data')
    return render(request, 'escala/lista_eventos.html', {'eventos': eventos})

def voluntariar(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    
    if request.method == 'POST':
        form = EscalaForm(request.POST)
        if form.is_valid():
            # Pega qual membro a pessoa escolheu na caixinha antes de salvar
            membro_escolhido = form.cleaned_data['membro']
            
            # TRATAMENTO DE ERRO: Verifica se já existe uma escala com esse membro + esse evento
            if Escala.objects.filter(evento=evento, membro=membro_escolhido).exists():
                # Dispara a mensagem de erro e NÃO salva
                messages.error(request, f"Atenção: {membro_escolhido.nome} já está escalado(a) para este evento!")
            else:
                # Se não existir, salva normalmente!
                escala = form.save(commit=False)
                escala.evento = evento
                escala.save()
                
                # Dispara a mensagem de sucesso
                messages.success(request, f"Sucesso! Presença de {membro_escolhido.nome} confirmada com alegria!")
                
                # Manda o usuário de volta para a tela inicial
                return redirect('lista_eventos') 
    else:
        form = EscalaForm()

    return render(request, 'escala/voluntariar.html', {'evento': evento, 'form': form})