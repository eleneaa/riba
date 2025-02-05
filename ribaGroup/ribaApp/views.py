from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Service


def main(request):
    return render(request, "index.html")


def portfolio(request):
    return render(request, "portfolio.html")


def service(request, service_name):
    this_service = get_object_or_404(Service, name=service_name)
    return render(request, "service.html", {"service_name": service_name})



