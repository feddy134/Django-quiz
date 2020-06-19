from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"
    title = models.CharField(max_length=200)


    def __str__(self):
        return self.title[:30]

class Question(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    question = models.TextField()
    explanation = models.TextField(blank=True,null=True)
    def __str__(self):
        s = str(self.category) + ' | ' + self.question[:30]
        return s
    

    
class Answer(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer


class Progress(models.Model):
    class Meta:
        verbose_name_plural = "Progress"
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    marks = models.IntegerField()
    total = models.IntegerField()

