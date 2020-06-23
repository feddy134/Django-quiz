from django.shortcuts import render ,get_object_or_404 ,redirect ,HttpResponse
from .models import Category, Question,Answer,Progress
from django.urls import reverse
# Create your views here.
def index(request):
    categories = Category.objects.order_by('id')
    return render(request,'quiz/index.html',{'categories':categories})

def sign_up(request):
    return render(request,'quiz/signup.html')

def log_in(request):
    return render(request,'quiz/login.html')

def quiz(request,cat_id):

    cat_object = get_object_or_404(Category,pk = cat_id)
    questions = Question.objects.filter(category = cat_object)
    answers = Answer.objects.filter(question__in=questions)
    return render(request,'quiz/quiz.html',{'answers':answers,'questions':questions})


def result(request):
    if request.method == 'POST':
        # for key, value in request.POST.items():
        #     print('Key: %s' % (key) ) 
        #     print('Value %s' % (value) )
        # [('1', '4'), ('2', '6'), ('3', '11'), ('4', '15'), ('5', '18')]
        rec_data = request.POST.items()
        data = list(rec_data)
        rem = data.pop(0)
        rtndata = {}
        marks = {}
        correct_ones = 0
        total_quest = 0
        for i in data:
            total_quest = total_quest + 1
            q = int(i[0])
            a = int(i[1])
            correct_id = 0
            question = get_object_or_404(Question,pk = q)
            answers = Answer.objects.filter(question=question)
            for ans in answers.all():
                if ans.correct == True:
                    correct_id = ans.id
        
            #check if answer is correct.
            # {qestion_object : [result,selected_answer,correct_answer,explanation]}  
            if a == correct_id:
                s_answer = get_object_or_404(Answer,pk=a)
                selected_answer = s_answer.answer
                explanation = question.explanation
                correct_ones = correct_ones + 1
                rtndata[question] = [ 'CORRECT', selected_answer,selected_answer, explanation]
            else:
                s_answer = get_object_or_404(Answer,pk=a)
                selected_answer = s_answer.answer
                c_answer = get_object_or_404(Answer,pk=correct_id)
                correct_answer = c_answer.answer
                explanation = question.explanation
                rtndata[question] = [ 'INCORRECT', selected_answer,correct_answer, explanation]

        marks['correct'] = correct_ones
        marks['total'] = total_quest
        return render(request,'quiz/result.html',{'rtndata':rtndata, 'marks':marks})