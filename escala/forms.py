from django import forms
from .models import Escala

class EscalaForm(forms.ModelForm):
    class Meta:
        model = Escala
        # O formulário vai pedir apenas o nome do membro.
        # O evento nós vamos pegar automaticamente pela URL!
        fields = ['membro']