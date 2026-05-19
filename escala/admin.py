from django.contrib import admin

from .models import Escala, Evento, Membro


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'data', 'vagas_midia')
    list_filter = ('data',)


@admin.register(Membro)
class MembroAdmin(admin.ModelAdmin):
    list_display = ('nome', 'funcao_principal', 'email')
    search_fields = ('nome',)


@admin.register(Escala)
class EscalaAdmin(admin.ModelAdmin):
    list_display = ('evento', 'membro', 'confirmado')
    list_editable = ('confirmado',)
