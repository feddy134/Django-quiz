from django.shortcuts import render
from django.shortcuts import render ,get_object_or_404 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from quiz.models import Category, Question,Answer,Progress ,Result
from .serializers import SignUpSerializer, CategorySerializer , QuestionSerializer,AnswerSerializer,ProgressSerializer,ResultSerializer
from .serializers import QuizQuestionSerializer,QuizAnswerSerializer
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
                question_serializer = QuizQuestionSerializer(question)
                answers_serializer = QuizAnswerSerializer(answers,many=True)
                return_data['question'] = question_serializer.data
                return_data['answers'] = answers_serializer.data

                return Response(return_data)
        return_data['message'] : 'All questions of this category has been attended'
        return Response(return_data)


def update_progress(request,question,correctness):
    user = request.user
    category = question.category
    increase_mark = 0
    total_questions = Question.objects.filter(category=category).count()
    if correctness:
        increase_mark = 1
    try:
        progress = Progress.objects.get(user=user,category=category)
        progress.marks += increase_mark
        progress.save()
    except Progress.DoesNotExist:
        progress = Progress.objects.create(user=user,category=category,marks=increase_mark,total=total_questions)


class ResultAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user = request.user
        data = request.data
        question = get_object_or_404(Question,id=data['question'])
        selected_answer = get_object_or_404(Answer,id=data['answer'])
        correct_answer_id = ''
        answers = Answer.objects.filter(question=question)
        try:
            attempted_result = Result.objects.get(user=user,question=question)
            return Response({'message':'You have already attempted this question'})
        except Result.DoesNotExist:
            for ans in answers.all():
                if ans.correct == True:
                    correct_answer_id = ans.id
            correct_answer = get_object_or_404(Answer,id=correct_answer_id)
            if str(correct_answer_id) == str(data['answer']):
                result = Result.objects.create(user=user,
                                            question=question,
                                            correctness=True,
                                            correct_answer=correct_answer,
                                            selected_answer=selected_answer)
                update_progress(request,question,True)
                result_serializer = ResultSerializer(result)
                return Response(result_serializer.data)
            else :
                result = Result.objects.create(user=user,
                                            question=question,
                                            correctness=False,
                                            correct_answer=correct_answer,
                                            selected_answer=selected_answer)
                update_progress(request,question,False)
                result_serializer = ResultSerializer(result)
                return Response(result_serializer.data)


class ProgressAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        progresses = Progress.objects.filter(user=user)
        serializer = ProgressSerializer(progresses,many=True)
        return Response(serializer.data) 