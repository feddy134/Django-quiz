from django.shortcuts import render
from rest_framework import generics
from rest_framework import mixins
from django.shortcuts import render ,get_object_or_404 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from quiz.models import Category, Question,Answer,Progress ,Result
from .serializers import SignUpSerializer, CategorySerializer , QuestionSerializer,AnswerSerializer,ProgressSerializer,ResultSerializer,UserSerializer
# from .serializers import QuizQuestionSerializer,QuizAnswerSerializer
# Create your views here.


class SignUpView(APIView):
    permission_classes = []
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


class IndexAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.order_by('id')
    serializer_class = CategorySerializer

class AnswersApiView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AnswerSerializer
    def get_queryset(self):
        question_id = self.kwargs['question_id']
        query = Answer.objects.filter(question__id = question_id)
        return query

class QuestionApiView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuestionSerializer
    def get_queryset(self):
        cat_id = self.kwargs['cat_id']
        user = self.request.user
        question_in_result = Result.objects.filter(user=user,question__category__id = cat_id)
        query = Question.objects.filter(category__id = cat_id).exclude(id__in=[o.question.id for o in question_in_result])
        return query



class ResultAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResultSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Result.objects.filter(user = user)
        return qs
        
    def create(self,request):
        user = self.request.user
        data = self.request.data
        question = get_object_or_404(Question,id = data['question'])
        correct_answer = get_object_or_404(Answer,id = data['correct_answer'])
        selected_answer = get_object_or_404(Answer,id = data['selected_answer'])
        correctness = False
        if data['correctness'] == 'true':
            correctness = True
        else:
            correctness = False
        result = Result.objects.create(user=user,
                            question=question,
                            correctness=correctness,
                            correct_answer=correct_answer,
                            selected_answer=selected_answer)

        serializer = ResultSerializer(result)
        return Response(serializer.data)
        

class ProgressAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProgressSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Progress.objects.filter(user = user)
        return qs

    def create(self,request):
        user = self.request.user
        data = self.request.data
        category_id = data['category'] 
        category = get_object_or_404(Category,id=category_id)
        total_questions = Question.objects.filter(category=category).count()
        try:
            progress = Progress.objects.get(user=user,category=category)
            progress.marks += int(data['marks'])
            progress.save()
            serializer= ProgressSerializer(progress)
            return Response(serializer.data)
        except Progress.DoesNotExist:
            progress = Progress.objects.create(user=user,category=category,marks=data['marks'],total=total_questions)
            serializer= ProgressSerializer(progress)
            return Response(serializer.data)