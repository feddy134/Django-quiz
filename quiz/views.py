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
        for i in data:
            q = int(i[0])
            a = int(i[1])
            correct_id = 0
            question = get_object_or_404(Question,pk = q)
            answers = Answer.objects.filter(question=question)
            for ans in answers.all():
                if ans.correct == True:
                    correct_id = ans.id
        
            #check if answer is correct.
            #if correct create a list with q_id ,correctnswer,result,Explanation  


        return HttpResponse(ans)