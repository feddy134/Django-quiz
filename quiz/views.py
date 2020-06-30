from django.shortcuts import render ,get_object_or_404 ,redirect ,HttpResponse
from .models import Category, Question,Answer,Progress ,Result
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/account/login/')
def index(request):
    '''
    Home page view
    All the categories are displayed
    '''
    categories = Category.objects.order_by('id')
    user = request.user
    prog_dict = {}
    prog = Progress.objects.filter(user=user)

    if prog is not None:
        for p in prog.all():
            category_id = p.category.id
            prog_dict[category_id] = [p.marks,p.total]
        return render(request,'quiz/index.html',{'categories':categories,'prog_dict':prog_dict})
    else:
        return render(request,'quiz/index.html',{'categories':categories})

def sign_up(request):
    '''
    To create new user
    '''
    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,'Account was created successfully for '+user)
            return redirect('/account/login/')

    context = {'form':form}
    return render(request,'quiz/signup.html', context)



@login_required(login_url='/account/login/')
def quiz(request,cat_id):
    '''
    Displays the questions of each category
    '''
    cat_object = get_object_or_404(Category,pk = cat_id)
    questions = Question.objects.filter(category = cat_object)
    answers = Answer.objects.filter(question__in=questions)
    return render(request,'quiz/quiz.html',{'answers':answers,'questions':questions})

@login_required(login_url='/account/login/')
def result(request):
    '''
    Calculates the result 
    '''
    if request.method == 'POST':
        # request.user
        # [('1', '4'), ('2', '6'), ('3', '11'), ('4', '15'), ('5', '18')]
        user = request.user
        rec_data = request.POST.items()
        data = list(rec_data)
        rem = data.pop(0)
        rtndata = {}
        marks = {}
        correct_ones = 0
        category = None
        # total_quest = 0
        for i in data:
            q = i[0]
            a = i[1]
            correct_id = 0
            question = get_object_or_404(Question,pk = q)
            category = question.category
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
                #update Result model
                try:
                    res = Result.objects.get(user = user,question=question)
                    res.correctness = True
                    res.save()
                except Result.DoesNotExist:
                    res = Result.objects.create(user=user,question=question,correctness=True,correct_answer=c_answer,selected_answer=s_answer)
        
            else:
                s_answer = get_object_or_404(Answer,pk=a)
                selected_answer = s_answer.answer
                c_answer = get_object_or_404(Answer,pk=correct_id)
                correct_answer = c_answer.answer
                explanation = question.explanation
                rtndata[question] = [ 'INCORRECT', selected_answer,correct_answer, explanation]
                #update Result model
                try:
                    res = Result.objects.get(user = user,question=question)
                    res.correctness = False
                    res.save()
                except Result.DoesNotExist:
                    res = Result.objects.create(user=user,question=question,correctness=False,correct_answer=c_answer,selected_answer=s_answer)

        total_quest = Question.objects.filter(category=category).count()
        marks['correct'] = correct_ones
        marks['total'] = total_quest
        
        
        #Update progress Model
        try:
            prog = Progress.objects.get(user=user,category=category)
            prog.marks = correct_ones
            prog.total = total_quest
            prog.save()
        except Progress.DoesNotExist:
            progress = Progress.objects.create(user=user,category=category,marks=correct_ones,total=total_quest)
        return render(request,'quiz/result.html',{'rtndata':rtndata, 'marks':marks})