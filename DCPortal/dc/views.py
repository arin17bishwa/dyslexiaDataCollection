from django.shortcuts import render, redirect, get_object_or_404
from .models import Data
from .constants import Quiz1


# Create your views here.

def takeQuizView(request):
    if request.method == 'POST':
        quiz1 = Quiz1()
        res = request.POST
        name = res['name']
        age = res['age']
        round1 = quiz1.score(res)
        Data.objects.create(
            name=name,
            age=int(age or '0'),
            score1=round1['score'],
            answer1=round1['responses']
        )
        return redirect('dc:takeQuiz')
    else:
        context = {}
        quiz1 = Quiz1()
        context = {
            'quiz1': quiz1.serialize()
        }
        return render(request, 'dc/takeQuiz.html', context=context)

def home(request):
    return render(request, 'home.html')
