from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from .forms import *
from .models import *


def main(request):
    images = WorkPic.objects.select_related('work_id').all()
    return render(request, "index.html", {"images": images})


def portfolio(request):
    works = Work.objects.all().order_by('-date').prefetch_related('photos')
    return render(request, "portfolio.html", {"works": works})


def service(request, service_name):
    this_service = get_object_or_404(Service, url_title=service_name)

    advantages = {
        "montazh_kotelnogo_oborudovaniya": {
            "Энергоэффективность": "Современные котлы помогут снизить расходы на отопление",
            "Надежность": "Установка качественного оборудования гарантирует долгую и безопасную эксплуатацию",
            "Индивидуальный подход": "Подбор котла в зависимости от площади и потребностей вашего дома"
        },
        "radiatornoe_otoplenie": {
            "Эффективность": "Быстрый прогрев помещений",
            "Комфорт": "Регулируемая температура в каждом помещении",
            "Надежность": "Долговечность системы и низкие затраты на обслуживание"
        },
        "vodyanoy_teplyy_pol": {
            "Комфорт": "Обеспечивает приятное тепло от пола",
            "Экономия": "Уменьшает затраты на отопление",
            "Эстетика": "Не занимает место и скрыт под покрытием"
        },
        "vnutrennee_vodosnabzhenie": {
            "Качество": "Используем только сертифицированные материалы для долговечности системы",
            "Эффективность": "Оптимальное распределение воды и высокая производительность",
            "Индивидуальный подход": "Проектирование системы с учетом особенностей вашего дома"
        }
    }

    step = int(request.GET.get('step', 1))

    form = None
    form_completed = False

    # Механизм отображения шагов
    if request.method == 'POST':
        if step == 1:
            form = WaterSupplySewageForm(request.POST)
            if form.is_valid():
                request.session['water_supply_sewage'] = form.cleaned_data['water_supply_sewage']
                return redirect(f'/service/{service_name}/?step=2')
        elif step == 2:
            form = SquareForm(request.POST)
            if form.is_valid():
                request.session['square'] = form.cleaned_data['square']
                return redirect(f'/service/{service_name}/?step=3')
        elif step == 3:
            form = ProjectForm(request.POST)
            if form.is_valid():
                request.session['project'] = form.cleaned_data['project']
                return redirect(f'/service/{service_name}/?step=4')
        elif step == 4:
            form = FloorsForm(request.POST)
            if form.is_valid():
                request.session['floors'] = form.cleaned_data['floors']
                return redirect(f'/service/{service_name}/?step=5')
        elif step == 5:
            form = HeatingForm(request.POST)
            if form.is_valid():
                request.session['heating'] = form.cleaned_data['heating']
                return redirect(f'/service/{service_name}/?step=6')
        elif step == 6:
            form = BoilerTypeForm(request.POST)
            if form.is_valid():
                request.session['boiler_type'] = form.cleaned_data['boiler_type']
                return redirect(f'/service/{service_name}/?step=7')
        elif step == 7:
            form = CustomerDataForm(request.POST)
            if form.is_valid():
                request.session['customer_name'] = form.cleaned_data['customer_name']
                request.session['customer_number'] = form.cleaned_data['customer_number']
                new_test = Test(
                    water_supply_sewage=request.session.get('water_supply_sewage'),
                    square=request.session.get('square'),
                    project=request.session.get('project'),
                    floors=request.session.get('floors'),
                    heating=request.session.get('heating'),
                    boiler_type=request.session.get('boiler_type'),
                    customer_name=request.session.get('customer_name'),
                    customer_number=request.session.get('customer_number')
                )

                new_customer = Customer(
                    name=request.session.get('customer_name'),
                    number=request.session.get('customer_number')
                )

                new_order = Order(
                    customer=new_customer,
                    estimate=False,
                    contract=False,
                    test=new_test
                )

                new_test.save()
                new_customer.save()
                new_order.save()

                form_completed = True

    else:
        if step == 1:
            form = WaterSupplySewageForm()
        elif step == 2:
            form = SquareForm()
        elif step == 3:
            form = ProjectForm()
        elif step == 4:
            form = FloorsForm()
        elif step == 5:
            form = HeatingForm()
        elif step == 6:
            form = BoilerTypeForm()
        elif step == 7:
            form = CustomerDataForm()
        else:
            return redirect(f'/service/{service_name}/?step=1')

    # Упаковка формы со списком её полей
    form_fields = [
        {
            "field": field,
            "widget_type": type(field.field.widget).__name__  # Тип виджета
        }
        for field in form
    ]

    return render(request, "service.html", {
        "service": this_service,
        "advantages": advantages[service_name],
        "form_fields": form_fields,
        "step": step,
        "form_completed": form_completed
    })


