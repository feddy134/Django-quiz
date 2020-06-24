from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.index , name='index'),
    path('sign_up/', views.sign_up ,name='sign_up'),
    # path('log_in/', views.log_in ,name='log_in'),
    path('<int:cat_id>/questions/',views.quiz,name='questions'),
    path('result/',views.result,name='result')
]
