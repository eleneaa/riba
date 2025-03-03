import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from .const import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
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

    # Сбрасываем тест, если услуга изменилась
    previous_service = request.session.get('current_service')
    if previous_service != service_name:
        # Очищаем все данные сессии, связанные с тестом
        keys_to_remove = ['current_question_index', 'selected_answers', 'open_answers', 'submitted_contact']
        for key in keys_to_remove:
            request.session.pop(key, None)
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
            contact_form = ContactForm(request.POST)
            if contact_form.is_valid():
                # Создаем клиента
                name = contact_form.cleaned_data['name']
                phone = contact_form.cleaned_data['phone']
                contact_methods = request.POST.getlist('contact_method')
                customer = Customer.objects.create(name=name, number=phone)

                # Получаем текущие ответы из сессии
                selected_answers = request.session.get('selected_answers', [])
                open_answers = request.session.get('open_answers', [])

                # Создаем результат теста
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

                # Создаем заказ
                order = Order.objects.create(
                    customer=customer,
                    service=this_service,
                    test_result=test_result
                )

                # Отправляем заказ в Telegram
                send_order_to_telegram(order, contact_methods)

                # Очищаем сессию после завершения
                keys_to_remove = ['current_question_index', 'selected_answers', 'open_answers', 'submitted_contact']
                for key in keys_to_remove:
                    request.session.pop(key, None)
                request.session['submitted_contact'] = True

                return render(request, 'service.html', {
                    'service': this_service,
                    'advantages': advantages.get(service_name, {}),
                    'stage': 'completed'
                })

            # Если форма невалидна, показываем ошибки
            return render(request, 'service.html', {
                'service': this_service,
                'advantages': advantages.get(service_name, {}),
                'stage': 'contact',
                'form': contact_form
            })

        # Показываем форму для ввода контактных данных
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
                # Для открытых вопросов обрабатываем данные как строку
                answer_text = form.cleaned_data.get('question', '')
                if isinstance(answer_text, str):  # Проверяем, что это строка
                    answer_text = answer_text.strip()  # Убираем лишние пробелы
                    if answer_text:  # Проверяем, что ответ не пустой
                        open_answers = request.session.get('open_answers', [])
                        open_answers.append({
                            'question': current_question.id,
                            'answer': answer_text
                        })
                        request.session['open_answers'] = open_answers
            else:
                # Для других типов вопросов обрабатываем данные как числа (ID ответов)
                selected_answers = request.session.get('selected_answers', [])
                new_answers = form.cleaned_data.get('question', [])
                if not isinstance(new_answers, list):  # Если ответ не список, делаем его списком
                    new_answers = [new_answers]
                for answer_id in new_answers:
                    if answer_id not in selected_answers:  # Проверяем, что ответ еще не добавлен
                        selected_answers.append(answer_id)
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


def reset_session(request):
    """Сбрасывает сессию и перенаправляет на страницу услуги."""
    keys_to_remove = ['current_question_index', 'selected_answers', 'open_answers', 'submitted_contact']
    for key in keys_to_remove:
        request.session.pop(key, None)
    return redirect('Услуга', service_name=request.session.get('current_service'))


def send_order_to_telegram(order, contact_methods):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    all_answer = {}

    for answer in order.test_result.answers.all():
        all_answer[answer.question] = answer.text

    # Формируем текст сообщения
    message = (
        f"🆕 <b>Новый заказ!</b>\n\n"
        f"📋 Услуга: <i>{order.service.name}</i>\n"
        f"👤 Клиент: <i>{order.customer.name}</i>\n"
        f"📞 Телефон: <i>{order.customer.number}</i>\n"
        f"📞 Способ связи: <i>{contact_methods}</i>\n"
        f"📊 Ответы:\n"
    )

    # Добавляем вопросы и ответы в формате "вопрос: ответ"
    for question, answer_text in all_answer.items():
        message += f"- <i>{question}</i> <strong>{answer_text}</strong>\n"

    # Если в тесте есть открытые ответы, добавляем их
    open_answers = order.test_result.openanswer_set.all()
    if open_answers:
        for answer in open_answers:
            message += f"- <i>{answer.question}:</i> <strong>{answer.text}</strong>"

    # Опции для Telegram API
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"  # Добавляем HTML-разметку
    }

    # Отправляем запрос
    response = requests.post(url, data=payload)

    # Проверяем ответ, чтобы отловить возможные ошибки
    if response.status_code != 200:
        print(f"Ошибка при отправке в Telegram: {response.status_code}, {response.text}")
