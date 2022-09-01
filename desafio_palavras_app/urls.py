from django.urls import path
from desafio_palavras_app import views

urlpatterns = [
    path('', views.getData),
    path('get_data/<str:world_name>', views.getWords),
]
