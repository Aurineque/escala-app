from django import forms
from .models import Escala

class EscalaForm(forms.ModelForm):
    class Meta:
        model = Escala

        fields = ['membro','funcao']
        labels = {
            'funcao': 'Função',
            'membro': 'Selecione o Voluntário', 
        }