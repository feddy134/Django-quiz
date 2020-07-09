
from django.urls import path
from .views import api_frontend
 
urlpatterns = [
    path('', api_frontend , name='frontend'),
]