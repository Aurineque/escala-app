import calendar  # Importamos a biblioteca de calendário do Python para descobrir o último dia do mês que vem

from django.contrib import messages  # Importamos o "mensageiro" do Django
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone  # Precisamos disso para saber a data de hoje

from .forms import EscalaForm
from .models import Escala, Evento  # Precisamos importar a Escala aqui também


def lista_eventos(request):
    agora = timezone.now()

    # CAMINHO 1: Antes do dia 25, mostra apenas o mês atual normalmente
    if agora.day < 25:
        eventos = Evento.objects.filter(data__month=agora.month, data__year=agora.year).order_by(
            'data'
        )

    # CAMINHO 2: Do dia 25 em diante, mostra do dia 25 até o fim do mês seguinte
    else:
        # Descobre qual é o próximo mês e ano (cuidando da virada de Dezembro)
        if agora.month == 12:
            mes_que_vem = 1
            ano_que_vem = agora.year + 1
        else:
            mes_que_vem = agora.month + 1
            ano_que_vem = agora.year

        # Pega o dia 25 do mês atual, à meia-noite
        inicio_janela = agora.replace(day=25, hour=0, minute=0, second=0, microsecond=0)

        # A mágica do 'calendar': ele devolve o último dia do mês que pedirmos!
        # O [1] ali no final serve para pegar apenas o número de dias (ex: 30 ou 31)
        ultimo_dia_mes_que_vem = calendar.monthrange(ano_que_vem, mes_que_vem)[1]

        # Monta a data limite exata: último dia do mês que vem, às 23:59:59
        fim_janela = agora.replace(
            year=ano_que_vem,
            month=mes_que_vem,
            day=ultimo_dia_mes_que_vem,
            hour=23,
            minute=59,
            second=59,
        )

        # Filtra como um sanduíche: maior ou igual ao início, e menor ou igual ao fim
        eventos = Evento.objects.filter(data__gte=inicio_janela, data__lte=fim_janela).order_by(
            'data'
        )

    return render(request, 'escala/lista_eventos.html', {'eventos': eventos})


def voluntariar(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)

    if request.method == 'POST':
        form = EscalaForm(request.POST)

        if form.is_valid():
            membro = form.cleaned_data['membro']

            # --- REGRA 1: Impede de se escalar duas vezes no MESMO evento ---
            if Escala.objects.filter(evento=evento, membro=membro).exists():
                messages.error(request, f'Ops! {membro.nome} já está escalado(a) neste evento.')
                return redirect('voluntariar', evento_id=evento.id)

            # --- REGRA 2: Limite máximo escalas no mês ---
            escalas_no_mes = Escala.objects.filter(
                membro=membro,
                evento__data__month=evento.data.month,
                evento__data__year=evento.data.year,
            ).count()

            if escalas_no_mes >= 6:
                messages.error(
                    request, f'{membro.nome} já atingiu o limite de 6 escalas para este mês!'
                )
                return redirect('voluntariar', evento_id=evento.id)

            # --- Se passou pelos dois bloqueios, salva com sucesso ---
            escala = form.save(commit=False)
            escala.evento = evento
            escala.save()

            messages.success(request, 'Presença confirmada com sucesso!')
            return redirect('lista_eventos')

    else:
        form = EscalaForm()

    return render(request, 'escala/voluntariar.html', {'form': form, 'evento': evento})
