from django import forms

from .models import Escala


class EscalaForm(forms.ModelForm):
    class Meta:
        model = Escala

        fields = ['membro', 'funcao']
        labels = {
            'funcao': 'Função',
            'membro': 'Selecione o Voluntário',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['membro'].queryset = self.fields['membro'].queryset.order_by('nome')
