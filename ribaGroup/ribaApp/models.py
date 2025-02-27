from django.conf import settings
from django.db import models


class Service(models.Model):
    url_title = models.CharField(max_length=100, verbose_name='Название услуги для ссылки')
    name = models.CharField(max_length=100, verbose_name='Название услуги')
    description = models.CharField(max_length=500, verbose_name="Краткое описание для карточки рядом с картинкой")
    description_bottom = models.CharField(max_length=500, verbose_name="Краткое описание для карточки внизу")
    main_photo = models.ImageField(verbose_name="Главное фото карточки")

    def __str__(self):
        return self.name


class Work(models.Model):
    date = models.DateTimeField(verbose_name="Дата и время выполнения заказа")
    place = models.CharField(max_length=100, verbose_name='Расположение объекта')
    square = models.FloatField(verbose_name="Площадь")
    cost_of_work = models.FloatField(verbose_name="Стоимость работ")
    cost_of_materials = models.FloatField(verbose_name="Стоимость материалов")

    def __str__(self):
        return f"{self.place} - {self.square} м²"


class Customer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя заказчика")
    number = models.CharField(max_length=15, verbose_name="Номер телефона")

    def __str__(self):
        return self.name


# models.py
class Question(models.Model):
    text = models.CharField(max_length=255, verbose_name="Текст вопроса")

    MULTIPLE_CHOICE = 'MC'
    SINGLE_CHOICE = 'SC'
    OPEN = 'O'
    QUESTION_TYPE_CHOICES = [
        (MULTIPLE_CHOICE, 'Несколько вариантов'),
        (SINGLE_CHOICE, 'Один вариант'),
        (OPEN, 'Открытый ответ')
    ]

    question_type = models.CharField(
        max_length=2,
        choices=QUESTION_TYPE_CHOICES,
        default=SINGLE_CHOICE,
        verbose_name="Тип вопроса"
    )

    # Новое поле для валидации типа открытых ответов
    EXPECTED_TEXT = 'text'
    EXPECTED_NUMBER = 'number'
    EXPECTED_ANSWER_CHOICES = [
        (EXPECTED_TEXT, 'Текст'),
        (EXPECTED_NUMBER, 'Число'),
    ]
    expected_answer_type = models.CharField(
        max_length=10,
        choices=EXPECTED_ANSWER_CHOICES,
        default=EXPECTED_TEXT,
        verbose_name="Ожидаемый тип открытого ответа"
    )

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
    text = models.CharField(max_length=255, verbose_name="Текст ответа")

    def __str__(self):
        return f"{self.text} (Вопрос: {self.question.text})"


class TestResult(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Клиент", null=True, blank=True)
    answers = models.ManyToManyField(Answer, verbose_name="Выбранные ответы")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Результат теста для {self.customer.name if self.customer else 'неизвестного клиента'} номер: {self.customer.number if self.customer else 'x'}"


class OpenAnswer(models.Model):
    test_result = models.ForeignKey(TestResult, on_delete=models.CASCADE, verbose_name="Результат теста")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    text = models.TextField(verbose_name="Ответ пользователя")

    def __str__(self):
        return f"Ответ на '{self.question.text}': {self.text}"


class WorkPic(models.Model):
    work_id = models.ForeignKey(to=Work, on_delete=models.SET_NULL, null=True, related_name='photos')
    photo = models.ImageField(verbose_name="Фото объекта")


class Order(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='orders', default=1)
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='orders', default=1)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    test_result = models.OneToOneField('TestResult', on_delete=models.CASCADE, related_name='order', null=True, blank=True)
    estimate = models.BooleanField(default=False, verbose_name="Сформирована смета?")
    contract = models.BooleanField(default=False, verbose_name="Заключен договор по заказу?")

    def __str__(self):
        return f"Order #{self.id} for {self.customer.name} date: {self.created_at}"
