from datetime import UTC, datetime

from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from escala.models import Escala, Evento, Membro


class EventoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.evento = Evento.objects.create(
            nome='Culto de Domingo',
            data=timezone.now(),
            vagas_midia=2,
        )
        cls.membro1 = Membro.objects.create(nome='João', email='joao@email.com')
        cls.membro2 = Membro.objects.create(nome='Maria', email='maria@email.com')
        cls.membro3 = Membro.objects.create(nome='Pedro', email='pedro@email.com')

    def test_vagas_restantes_quando_tem_vaga(self):
        self.assertEqual(self.evento.vagas_restantes, 2)

    def test_vagas_restantes_quando_lotado(self):
        Escala.objects.create(evento=self.evento, membro=self.membro1)
        Escala.objects.create(evento=self.evento, membro=self.membro2)
        self.assertEqual(self.evento.vagas_restantes, 0)

    def test_vagas_restantes_nunca_negativo(self):
        Escala.objects.create(evento=self.evento, membro=self.membro1)
        Escala.objects.create(evento=self.evento, membro=self.membro2)
        Escala.objects.create(evento=self.evento, membro=self.membro3)
        self.assertEqual(self.evento.vagas_restantes, 0)

    def test_evento_str_formato(self):
        data = datetime(2026, 6, 15, 19, 0, 0, tzinfo=UTC)
        evento = Evento.objects.create(nome='Culto de Domingo', data=data)
        self.assertEqual(str(evento), 'Culto de Domingo - 15/06/2026')


class MembroModelTest(TestCase):
    def test_membro_str_retorna_nome(self):
        membro = Membro.objects.create(nome='João Silva', email='joao@email.com')
        self.assertEqual(str(membro), 'João Silva')

    def test_membro_email_unico(self):
        Membro.objects.create(nome='João', email='joao@email.com')
        with self.assertRaises(IntegrityError):
            Membro.objects.create(nome='João 2', email='joao@email.com')


class EscalaModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.evento = Evento.objects.create(nome='Culto', data=timezone.now())
        cls.membro = Membro.objects.create(nome='João', email='joao@email.com')
        cls.escala = Escala.objects.create(evento=cls.evento, membro=cls.membro)

    def test_escala_str_formato(self):
        self.assertEqual(str(self.escala), 'João no(a) Culto')

    def test_escala_unique_together(self):
        with self.assertRaises(IntegrityError):
            Escala.objects.create(evento=self.evento, membro=self.membro)
