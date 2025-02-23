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


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания заказа")
    customer = models.ForeignKey(to=Customer, on_delete=models.SET_NULL, null=True, related_name='orders')
    estimate = models.BooleanField(verbose_name="Сформирована смета?")
    contract = models.BooleanField(verbose_name="Заключен договор по заказу?")
    test = models.ForeignKey(to='Test', on_delete=models.SET_NULL, null=True, related_name='orders')

    def __str__(self):
        return f"Заказ от {self.customer.name} - Дата создания: {self.created_at}"


class Test(models.Model):
    PROJECT_CHOICES = [
        ('yes', 'Да'),
        ('no', 'Нет')
    ]

    FLOORS_CHOICES = [
        (1, '1 этаж'),
        (2, '2 этажа'),
        (3, '3 этажа'),
        ('individual', 'Индивидуальный')
    ]

    HEATING_CHOICES = [
        ('warm_floor', 'Теплый пол'),
        ('radiators', 'Радиаторы'),
        ('warm_floor_radiators', 'Теплый пол + Радиаторы')
    ]

    BOILER_TYPE_CHOICES = [
        ('gas', 'Газ'),
        ('electric', 'Электро'),
        ('solid_fuel', 'Твердотопливный'),
        ('diesel', 'Дизельный')
    ]

    water_supply_sewage = models.BooleanField(default=False)
    square = models.FloatField(verbose_name="Площадь")
    project = models.CharField(max_length=3, choices=PROJECT_CHOICES)
    floors = models.IntegerField(choices=FLOORS_CHOICES)
    heating = models.CharField(max_length=50, choices=HEATING_CHOICES)
    boiler_type = models.CharField(max_length=50, choices=BOILER_TYPE_CHOICES)

    customer_name = models.CharField(max_length=100, verbose_name="Имя заказчика")
    customer_number = models.CharField(max_length=15, verbose_name="Номер телефона")

    def __str__(self):
        return f"Тест для {self.customer_name} - Площадь: {self.square} м²"

    def is_complete(self):
        return all([self.water_supply_sewage, self.square, self.project, self.floors, self.heating, self.boiler_type])


class WorkPic(models.Model):
    work_id = models.ForeignKey(to=Work, on_delete=models.SET_NULL, null=True, related_name='photos')
    photo = models.ImageField(verbose_name="Фото объекта")
