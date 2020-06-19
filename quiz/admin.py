from django.contrib import admin
from . models import Category,Question,Answer,Progress
# Register your models here.

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Category)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Progress)
