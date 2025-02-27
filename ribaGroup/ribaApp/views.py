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
    # Получаем услугу
    this_service = get_object_or_404(Service, url_title=service_name)

    # Сбрасывать тест, если услуга изменилась
    previous_service = request.session.get('current_service')
    if previous_service != service_name:
        # Очистить сессию теста полностью
        request.session.pop('current_question_index', None)
        request.session.pop('selected_answers', None)
        request.session.pop('open_answers', None)
        request.session.pop('submitted_contact', None)
        request.session['current_service'] = service_name  # Устанавливаем новую услугу

    # Преимущества услуги
    advantages = {
        "montazh_kotelnogo_oborudovaniya": {
            "Энергоэффективность": "Современные котлы помогут снизить расходы на отопление",
            "Надежность": "Установка качественного оборудования гарантирует долгую и безопасную эксплуатацию",
            "Индивидуальный подход": "Подбор котла в зависимости от площади и потребностей вашего дома",
        },
        "radiatornoe_otoplenie": {
            "Эффективность": "Быстрый прогрев помещений",
            "Комфорт": "Регулируемая температура в каждом помещении",
            "Надежность": "Долговечность системы и низкие затраты на обслуживание",
        },
        "vodyanoy_teplyy_pol": {
            "Комфорт": "Обеспечивает приятное тепло от пола",
            "Экономия": "Уменьшает затраты на отопление",
            "Эстетика": "Не занимает место и скрыт под покрытием",
        },
        "vnutrennee_vodosnabzhenie": {
            "Качество": "Используем только сертифицированные материалы для долговечности системы",
            "Эффективность": "Оптимальное распределение воды и высокая производительность",
            "Индивидуальный подход": "Проектирование системы с учетом особенностей вашего дома",
        }
    }

    # Получаем список всех вопросов и текущий прогресс
    questions = Question.objects.all().order_by('id')
    total_questions = len(questions)
    current_question_index = request.session.get('current_question_index', 0)

    # Если пользователь завершил все вопросы
    if current_question_index >= total_questions:
        # Если контактные данные уже отправлены, показываем сообщение о завершении
        if request.session.get('submitted_contact'):
            return render(request, 'service.html', {
                'service': this_service,
                'advantages': advantages.get(service_name, {}),
                'stage': 'completed'
            })

        # Этап сбора контактных данных
        if request.method == 'POST':
            contact_form = ContactForm(request.POST)  # Используем ContactForm для проверки данных
            if contact_form.is_valid():
                # Создаём клиента
                name = contact_form.cleaned_data['name']
                phone = contact_form.cleaned_data['phone']
                customer = Customer.objects.create(name=name, number=phone)

                # Получаем текущие ответы из сессии
                selected_answers = request.session.get('selected_answers', [])
                open_answers = request.session.get('open_answers', [])

                # Создаём результат теста
                test_result = TestResult.objects.create(customer=customer)
                if selected_answers:
                    test_result.answers.set(Answer.objects.filter(id__in=selected_answers))

                # Сохраняем открытые ответы
                for item in open_answers:
                    OpenAnswer.objects.create(
                        test_result=test_result,
                        question=Question.objects.get(id=item['question']),
                        text=item['answer']
                    )

                # Создание заказа после теста
                Order.objects.create(
                    customer=customer,
                    service=this_service,
                    test_result=test_result
                )

                # Очистка сессии после завершения
                request.session.pop('current_question_index', None)
                request.session.pop('selected_answers', None)
                request.session.pop('open_answers', None)
                request.session['submitted_contact'] = True

                return render(request, 'service.html', {
                    'service': this_service,
                    'advantages': advantages.get(service_name, {}),
                    'stage': 'completed'
                })

            # Если ввод был некорректным
            return render(request, 'service.html', {
                'service': this_service,
                'advantages': advantages.get(service_name, {}),
                'stage': 'contact',
                'form': contact_form
            })

        # Показ пустой формы контактов
        contact_form = ContactForm()
        return render(request, 'service.html', {
            'service': this_service,
            'advantages': advantages.get(service_name, {}),
            'stage': 'contact',
            'form': contact_form
        })

    # Этап вопросов
    current_question = questions[current_question_index]
    if request.method == 'POST':
        form = TestForm(request.POST, questions=[current_question])
        if form.is_valid():
            if current_question.question_type == Question.OPEN:
                # Сохраняем открытые ответы
                open_answers = request.session.get('open_answers', [])
                open_answers.append({
                    'question': current_question.id,
                    'answer': form.cleaned_data['question']  # Данные очищены формой
                })
                request.session['open_answers'] = open_answers
            else:
                # Сохраняем выбор пользователя
                selected_answers = request.session.get('selected_answers', [])
                selected_answers.extend(form.cleaned_data['question'])
                request.session['selected_answers'] = selected_answers

            # Переходим к следующему вопросу
            request.session['current_question_index'] = current_question_index + 1
            return redirect('Услуга', service_name=service_name)
    else:
        form = TestForm(questions=[current_question])

    return render(request, 'service.html', {
        'service': this_service,
        'advantages': advantages.get(service_name, {}),
        'form': form,
        'current_question': current_question,
        'stage': 'questions'
    })


