from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('upload/', views.upload_csv, name='upload_csv'),
    path('api/nulos/', views.api_nulos, name='api_nulos'),
    path('api/numericas/', views.api_numericas, name='api_numericas'),
    path('api/fechas/', views.api_fechas, name='api_fechas'),
    path('api/acumulado/', views.api_acumulado, name='api_acumulado'),
    path('api/tipo_dato/', views.api_tipo_dato, name='api_tipo_dato'),
    path('api/no_nulos/', views.api_no_nulos, name='api_no_nulos'),
]