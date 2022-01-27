from django.shortcuts import render, redirect, get_object_or_404
from .models import Data
from .constants import Quiz1, Quiz2, Quiz3, Quiz4


# Create your views here.

def takeQuizView(request):
    if request.method == 'POST':
        quiz1 = Quiz1()
        quiz2 = Quiz2()
        res = request.POST
        name = res['name']
        age = res['age']
        # round1 = quiz1.score(res)
        round2 = quiz2.score(res)

        Data.objects.create(
            name=name,
            age=int(age or '0'),
            score2=round2['score'],
            answer2=round2['responses']
        )
        return redirect('dc:takeQuiz')
    else:
        context = {}
        quiz1 = Quiz1()
        quiz2 = Quiz2()
        context = {
            # 'quiz1': quiz1.serialize(),
            'quiz2': quiz2.serialize(),
        }
        return render(request, 'dc/takeQuiz.html', context=context)


def home(request):
    return render(request, 'home.html')
