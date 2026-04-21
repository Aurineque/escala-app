from django.shortcuts import render, get_object_or_404, redirect
from .models import Evento
from .forms import EscalaForm

# Esta é a view que você já tinha:
def lista_eventos(request):
    eventos = Evento.objects.all().order_by('data')
    return render(request, 'escala/lista_eventos.html', {'eventos': eventos})

# Esta é a view NOVA:
def voluntariar(request, evento_id):
    # Busca o evento que a pessoa clicou ou dá erro 404 se não existir
    evento = get_object_or_404(Evento, id=evento_id)
    
    if request.method == 'POST':
        form = EscalaForm(request.POST)
        if form.is_valid():
            # Pausa o salvamento para podermos preencher qual é o evento
            escala = form.save(commit=False)
            escala.evento = evento
            escala.save() # Agora sim, salva no banco!
            return redirect('lista_eventos') # Volta para a lista
    else:
        form = EscalaForm()

    return render(request, 'escala/voluntariar.html', {'evento': evento, 'form': form})