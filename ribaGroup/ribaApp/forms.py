from django import forms
from django.core.validators import RegexValidator

from .models import Question


class TestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions', [])
        super().__init__(*args, **kwargs)

        if len(questions) != 1:
            raise ValueError("Форма поддерживает только один вопрос за раз.")

        question = questions[0]
        self.question = question

        if question.question_type == Question.OPEN:
            # Открытый вопрос: выбираем CharField или IntegerField
            if question.expected_answer_type == Question.EXPECTED_NUMBER:
                self.fields['question'] = forms.IntegerField(
                    label=question.text,
                    required=True,
                    widget=forms.NumberInput(attrs={'placeholder': 'Введите число'}),
                    error_messages={
                        'invalid': 'Вы должны ввести число.',
                    }
                )
            else:
                self.fields['question'] = forms.CharField(
                    label=question.text,
                    required=True,
                    widget=forms.TextInput(attrs={'placeholder': 'Введите текст'}),
                )
        else:
            # Вопрос с несколькими или одним выбором
            choices = [(answer.id, answer.text) for answer in question.answers.all()]

            if question.question_type == Question.MULTIPLE_CHOICE:
                # Поле с несколькими вариантами ответа
                self.fields['question'] = forms.MultipleChoiceField(
                    label=question.text,
                    required=True,
                    widget=forms.CheckboxSelectMultiple,  # Виджет: чекбоксы
                    choices=choices
                )
            else:
                # Поле с одним вариантом ответа
                self.fields['question'] = forms.ChoiceField(
                    label=question.text,
                    required=True,
                    widget=forms.RadioSelect,  # Виджет: радиокнопки
                    choices=choices
                )


class ContactForm(forms.Form):
    name = forms.CharField(
        label="Ваше имя",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Введите ваше имя"})
    )

    phone = forms.CharField(
        label="Ваш номер телефона",
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Введите ваш номер телефона"}),
        validators=[
            RegexValidator(
                regex=r'^\+?\d{10,15}$',
                message="Введите корректный номер телефона (например, +79991234567)"
            )
        ]
    )