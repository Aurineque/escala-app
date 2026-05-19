from django.test import TestCase

from escala.forms import EscalaForm
from escala.models import Membro


class EscalaFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.membro = Membro.objects.create(nome='João', email='joao@email.com')

    def test_form_campos_esperados(self):
        form = EscalaForm()
        self.assertIn('membro', form.fields)
        self.assertIn('funcao', form.fields)
        self.assertEqual(len(form.fields), 2)

    def test_form_labels_personalizados(self):
        form = EscalaForm()
        self.assertEqual(form.fields['membro'].label, 'Selecione o Voluntário')
        self.assertEqual(form.fields['funcao'].label, 'Função')

    def test_form_valido_com_dados(self):
        form = EscalaForm(
            data={
                'membro': self.membro.id,
                'funcao': 'geral',
            }
        )
        self.assertTrue(form.is_valid())

    def test_form_invalido_sem_dados(self):
        form = EscalaForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('membro', form.errors)
        self.assertIn('funcao', form.errors)
