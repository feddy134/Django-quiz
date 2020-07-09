  
from rest_framework import serializers
from quiz.models import Category, Question,Answer,Progress ,Result
from django.contrib.auth.models import User


class SignUpSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type':'password'})
    class Meta:
        model = User
        fields = ['username','password','password2']
        extra_kwargs = {
            'password' : {'write_only':True}
        }

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'Passwords must match'})

        user = User(username = self.validated_data['username'])
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'




class ProgressSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Progress
        fields = ['id','marks','total','user','category']


class ResultSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    question = QuestionSerializer(read_only=True)
    correct_answer = AnswerSerializer(read_only=True)
    selected_answer = AnswerSerializer(read_only=True)
    class Meta:
        model = Result
        fields = ['id','correctness','user','question','correctness','correct_answer','selected_answer']

# class QuizQuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Question
#         fields = ['id','question']


# class QuizAnswerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Answer
#         fields = ['id','answer']