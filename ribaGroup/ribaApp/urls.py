from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import reset_session

urlpatterns = [
    path("", views.main, name="Главная"),
    path("portfolio/", views.portfolio, name="Портфолио"),
    path("service/<str:service_name>/", views.service, name="Услуга"),
    path('reset-session/', reset_session, name='reset_session'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)