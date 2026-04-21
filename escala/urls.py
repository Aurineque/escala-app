from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_eventos, name='lista_eventos'),
    # Nova rota que recebe o ID do evento na URL:
    path('voluntariar/<int:evento_id>/', views.voluntariar, name='voluntariar'), 
]