from django.urls import path
from .views import IndexAPIView, SignUpView , QuestionApiView , ResultAPIView, ProgressAPIView,AnswersApiView
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('index/',IndexAPIView.as_view() , name='api_index'),
    path('sign_up/', SignUpView.as_view() ,name='api_sign_up'),
    path('log_in/', obtain_auth_token ,name='api_log_in'),
    path('questions/<slug:cat_id>/',QuestionApiView.as_view(),name='api_questions'),
    path('answers/<slug:question_id>/',AnswersApiView.as_view(),name='api_answers'),
    path('result/',ResultAPIView.as_view(),name='api_result'),
    path('progress/',ProgressAPIView.as_view(),name='api_progress'),
]
