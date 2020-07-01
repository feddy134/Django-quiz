from django.shortcuts import render ,get_object_or_404 ,redirect ,HttpResponse
from .models import Category, Question,Answer,Progress ,Result
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control



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
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def quiz(request,cat_id):
    '''
    Displays the questions of each category
    '''
    user = request.user
    category_object = get_object_or_404(Category,pk = cat_id)
    questions = Question.objects.filter(category = category_object)
    answers = Answer.objects.filter(question__in=questions)
    for question in questions.all():
        try:
            question_in_result = Result.objects.get(user=user,question=question)
            continue
        except Result.DoesNotExist:
            answers = Answer.objects.filter(question=question)
            return render(request,'quiz/quiz.html',{'answers':answers,'question':question})


    return render(request,'quiz/quiz.html',{'Completed':True})



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


@login_required(login_url='/account/login/')
def result(request):
    '''
    Calculates the result 
    '''
    if request.method == 'POST':
        post_data = list(request.POST.items())
        user = request.user
        post_data.pop(0)

        question = get_object_or_404(Question,id=post_data[0][0])
        selected_answer = get_object_or_404(Answer,id=post_data[0][1])
        correct_answer_id = ''
        answers = Answer.objects.filter(question=question)
        for ans in answers.all():
            if ans.correct == True:
                correct_answer_id = ans.id
        correct_answer = get_object_or_404(Answer,id=correct_answer_id)
        
        if str(correct_answer_id) == str(post_data[0][1]):
            result = Result.objects.create(user=user,
                                        question=question,
                                        correctness=True,
                                        correct_answer=correct_answer,
                                        selected_answer=selected_answer)
            update_progress(request,question,True)
            return render(request,'quiz/result.html',{'result':result})
        else :
            result = Result.objects.create(user=user,
                                        question=question,
                                        correctness=False,
                                        correct_answer=correct_answer,
                                        selected_answer=selected_answer)
            update_progress(request,question,False)
            return render(request,'quiz/result.html',{'result':result})
            
    return render(request,'quiz/result.html')