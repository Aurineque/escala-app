from datetime import UTC, datetime, timedelta
from unittest.mock import patch

from django.contrib.messages import get_messages
from django.test import TestCase

from escala.forms import EscalaForm
from escala.models import Escala, Evento, Membro


class ListaEventosViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.membro = Membro.objects.create(nome='João', email='joao@email.com')

    def test_lista_eventos_template_usado(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'escala/lista_eventos.html')

    def test_lista_eventos_sem_eventos(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['eventos']), 0)

    @patch('django.utils.timezone.now')
    def test_lista_eventos_ordenados_por_data(self, mock_now):
        mock_now.return_value = datetime(2026, 6, 15, 10, 0, 0, tzinfo=UTC)
        Evento.objects.create(
            nome='Segundo', data=datetime(2026, 6, 15, 19, 0, 0, tzinfo=UTC),
        )
        Evento.objects.create(
            nome='Primeiro', data=datetime(2026, 6, 10, 19, 0, 0, tzinfo=UTC),
        )
        response = self.client.get('/')
        eventos = response.context['eventos']
        self.assertEqual(eventos[0].nome, 'Primeiro')
        self.assertEqual(eventos[1].nome, 'Segundo')

    @patch('django.utils.timezone.now')
    def test_lista_eventos_filtra_mes_atual(self, mock_now):
        mock_now.return_value = datetime(2026, 6, 10, 10, 0, 0, tzinfo=UTC)

        Evento.objects.create(
            nome='Evento Junho',
            data=datetime(2026, 6, 20, 19, 0, 0, tzinfo=UTC),
        )
        Evento.objects.create(
            nome='Evento Julho',
            data=datetime(2026, 7, 5, 19, 0, 0, tzinfo=UTC),
        )

        response = self.client.get('/')
        self.assertContains(response, 'Evento Junho')
        self.assertNotContains(response, 'Evento Julho')

    @patch('django.utils.timezone.now')
    def test_lista_eventos_janela_estendida(self, mock_now):
        mock_now.return_value = datetime(2026, 6, 25, 10, 0, 0, tzinfo=UTC)

        Evento.objects.create(
            nome='Dentro Janela',
            data=datetime(2026, 6, 28, 19, 0, 0, tzinfo=UTC),
        )
        Evento.objects.create(
            nome='Fora Janela',
            data=datetime(2026, 6, 10, 19, 0, 0, tzinfo=UTC),
        )

        response = self.client.get('/')
        self.assertContains(response, 'Dentro Janela')
        self.assertNotContains(response, 'Fora Janela')

    @patch('django.utils.timezone.now')
    def test_lista_eventos_virada_ano(self, mock_now):
        mock_now.return_value = datetime(2026, 12, 25, 10, 0, 0, tzinfo=UTC)

        Evento.objects.create(
            nome='Evento Dezembro',
            data=datetime(2026, 12, 28, 19, 0, 0, tzinfo=UTC),
        )
        Evento.objects.create(
            nome='Evento Janeiro',
            data=datetime(2027, 1, 10, 19, 0, 0, tzinfo=UTC),
        )

        response = self.client.get('/')
        self.assertContains(response, 'Evento Dezembro')
        self.assertContains(response, 'Evento Janeiro')


class VoluntariarViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.membro = Membro.objects.create(nome='João', email='joao@email.com')
        cls.evento = Evento.objects.create(
            nome='Culto de Domingo',
            data=datetime(2026, 6, 15, 19, 0, 0, tzinfo=UTC),
            vagas_midia=5,
        )

    def test_voluntariar_get_formulario(self):
        response = self.client.get(f'/voluntariar/{self.evento.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], EscalaForm)
        self.assertTemplateUsed(response, 'escala/voluntariar.html')

    def test_voluntariar_evento_inexistente_retorna_404(self):
        response = self.client.get('/voluntariar/99999/')
        self.assertEqual(response.status_code, 404)

    def test_voluntariar_post_cria_escala_com_sucesso(self):
        response = self.client.post(
            f'/voluntariar/{self.evento.id}/',
            {
                'membro': self.membro.id,
                'funcao': 'geral',
            },
        )

        self.assertRedirects(response, '/')
        self.assertEqual(Escala.objects.count(), 1)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Presença confirmada com sucesso!')

    def test_voluntariar_post_duplicata_no_evento(self):
        Escala.objects.create(evento=self.evento, membro=self.membro)

        response = self.client.post(
            f'/voluntariar/{self.evento.id}/',
            {
                'membro': self.membro.id,
                'funcao': 'geral',
            },
        )

        self.assertRedirects(response, f'/voluntariar/{self.evento.id}/')
        self.assertEqual(Escala.objects.count(), 1)

        messages = list(get_messages(response.wsgi_request))
        self.assertIn('já está escalado', str(messages[0]))

    def test_voluntariar_post_excede_limite_mensal(self):
        for i in range(6):
            e = Evento.objects.create(
                nome=f'Evento {i}',
                data=datetime(2026, 6, 1, tzinfo=UTC) + timedelta(days=i),
            )
            Escala.objects.create(evento=e, membro=self.membro)

        response = self.client.post(
            f'/voluntariar/{self.evento.id}/',
            {
                'membro': self.membro.id,
                'funcao': 'geral',
            },
        )

        self.assertRedirects(response, f'/voluntariar/{self.evento.id}/')
        self.assertEqual(Escala.objects.count(), 6)

        messages = list(get_messages(response.wsgi_request))
        self.assertIn('limite de 6', str(messages[0]))

    def test_voluntariar_post_dados_invalidos(self):
        response = self.client.post(f'/voluntariar/{self.evento.id}/', {})

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())
