from django.contrib import admin
from .models import *

admin.site.register(Service)
admin.site.register(Work)
admin.site.register(WorkPic)
admin.site.register(Order)


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1  # Количество дополнительных строк по умолчанию


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question_type')
    inlines = [AnswerInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(TestResult)
admin.site.register(OpenAnswer)
