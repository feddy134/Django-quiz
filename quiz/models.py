from django.db import models
from django.contrib.auth.models import User
import uuid

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
# Create your models here.

class Category(models.Model):
    '''
    Category model for question
    Every question comes under a category
    '''
    class Meta:
        verbose_name_plural = "Categories"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)


    def __str__(self):
        return self.title[:30]

class Question(models.Model):
    '''
    Every question is stored in this model
    If there are any explantion , it is also stored 
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    question = models.TextField()
    explanation = models.TextField(blank=True,null=True)
    def __str__(self):
        s = '{} | {}'.format(str(self.category),self.question[:30])
        return s
    

    
class Answer(models.Model):
    '''
    options for each question is stored here
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    answer = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer


class Progress(models.Model):
    '''
    Marks of each category 
    '''
    class Meta:
        verbose_name_plural = "Progress"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    marks = models.IntegerField()
    total = models.IntegerField()

    def __str__(self):
        s = '{} | {}'.format(str(self.user),str(self.category))
        return s 

class Result(models.Model):
    '''
    Marks of each category is stored in this model
    '''
    class Meta:
        verbose_name_plural = 'Results'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    correctness = models.BooleanField(default=False)
    correct_answer = models.ForeignKey(Answer,on_delete=models.CASCADE,related_name='correct_answer')
    selected_answer  = models.ForeignKey(Answer,on_delete=models.CASCADE,related_name='selected_answer')

    def __str__(self):
        s = '{} | {}'.format(str(self.user),str(self.question)) 
        return s 


@receiver(post_save, sender = User)
def create_auth_token(sender,instance = None, created= False,**kwargs):
    if created:
        Token.objects.create(user=instance)