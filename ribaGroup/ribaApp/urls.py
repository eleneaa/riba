from django.urls import path
from . import views

urlpatterns = [
    path("", views.main, name="Главная"),
    path("portfolio/", views.portfolio, name="Портфолио"),
    path("service/<str:service_name>/", views.service, name="Услуга")
]