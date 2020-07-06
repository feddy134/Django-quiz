from django.shortcuts import render
from django.shortcuts import render ,get_object_or_404 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from quiz.models import Category, Question,Answer,Progress ,Result
from .serializers import SignUpSerializer, CategorySerializer , QuestionSerializer,AnswerSerializer,ProgressSerializer,ResultSerializer

# Create your views here.


class SignUpView(APIView):
    def post(self,request):
        serializer = SignUpSerializer(data = request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'Successfully registered the user'
            data['username'] = user.username
            token = Token.objects.get(user = user).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


class IndexAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        categories = Category.objects.order_by('id')
        serializer = CategorySerializer(categories,many = True)
        return_data = serializer.data
        return Response(serializer.data)

class QuizApiView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,cat_id):
        user = request.user
        category_object = get_object_or_404(Category,pk = cat_id)
        questions = Question.objects.filter(category = category_object)
        
        answers = Answer.objects.filter(question__in=questions)
        return_data = {}
        for question in questions.all():
            try:
                question_in_result = Result.objects.get(user=user,question=question)
                continue
            except Result.DoesNotExist:
                answers = Answer.objects.filter(question=question)
                question_serializer = QuestionSerializer(question)
                answers_serializer = AnswerSerializer(answers,many=True)
                return_data['question'] = question_serializer.data
                return_data['answers'] = answers_serializer.data

                return Response(return_data)
        return_data['message'] : 'All questions of this category has been attended'
        return Response(return_data)