from django.shortcuts import render, redirect, get_object_or_404
from .models import Data
from .constants import Quiz1, Quiz2, Quiz3, Quiz4


# Create your views here.

def takeQuizView(request):
    if request.method == 'POST':
        quiz1 = Quiz1()
        quiz2 = Quiz2()
        quiz3 = Quiz3()
        quiz4 = Quiz4()
        res = request.POST
        name = res['name']
        age = res['age']
        # round1 = quiz1.score(res)
        # round2 = quiz2.score(res),
        round3 = quiz3.score(res)
        # print(round3)
        Data.objects.create(
            name=name,
            age=int(age or '0'),
            score3=round3['score'],
            answer3=round3['responses']
        )
        return redirect('dc:takeQuiz')
    else:
        context = {}
        quiz1 = Quiz1()
        quiz2 = Quiz2()
        quiz3 = Quiz3()
        context = {
            # 'quiz1': quiz1.serialize(),
            # 'quiz2': quiz2.serialize(),
            'quiz3': quiz3.serialize(),
        }
        print(context['quiz3'].keys())
        return render(request, 'dc/takeQuiz.html', context=context)


def home(request):
    return render(request, 'home.html')
