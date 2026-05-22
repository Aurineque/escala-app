from django.urls import path

from . import views

urlpatterns = [
    path('', views.lista_eventos, name='lista_eventos'),
    path('deploy/', views.deploy_webhook, name='deploy'),
    path('voluntariar/<int:evento_id>/', views.voluntariar, name='voluntariar'),
]
