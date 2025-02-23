# myapp/forms.py
from django import forms
from .models import Test


class WaterSupplySewageForm(forms.Form):
    water_supply_sewage = forms.BooleanField(label='Водоснабжение и канализация?', required=False)


class SquareForm(forms.Form):
    square = forms.FloatField(label="Площадь", min_value=0)


class ProjectForm(forms.Form):
    PROJECT_CHOICES = [
        ('yes', 'Да'),
        ('no', 'Нет')
    ]
    project = forms.ChoiceField(label='Проект', choices=PROJECT_CHOICES)


class FloorsForm(forms.Form):
    FLOORS_CHOICES = [
        (1, '1 этаж'),
        (2, '2 этажа'),
        (3, '3 этажа'),
        ('individual', 'Индивидуальный')
    ]
    floors = forms.ChoiceField(label='Этажность', choices=FLOORS_CHOICES)


class HeatingForm(forms.Form):
    HEATING_CHOICES = [
        ('warm_floor', 'Теплый пол'),
        ('radiators', 'Радиаторы'),
        ('warm_floor_radiators', 'Теплый пол + Радиаторы')
    ]
    heating = forms.ChoiceField(label='Отопление', choices=HEATING_CHOICES)


class BoilerTypeForm(forms.Form):
    BOILER_TYPE_CHOICES = [
        ('gas', 'Газ'),
        ('electric', 'Электро'),
        ('solid_fuel', 'Твердотопливный'),
        ('diesel', 'Дизель')
    ]
    boiler_type = forms.ChoiceField(label='Тип котла', choices=BOILER_TYPE_CHOICES)


class CustomerDataForm(forms.Form):
    customer_name = forms.CharField(label="Имя")
    customer_number = forms.CharField(label="Номер")
