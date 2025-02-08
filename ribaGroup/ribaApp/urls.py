from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("", views.main, name="Главная"),
    path("portfolio/", views.portfolio, name="Портфолио"),
    path("service/<str:service_name>/", views.service, name="Услуга")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)