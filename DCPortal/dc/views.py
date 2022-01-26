from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404

from .constants import Quiz1


# Create your views here.

def takeQuizView(request):
    if request.method == 'POST':
        pass
    else:
        context = {}
        quiz1 = Quiz1()
        context = {
            'quiz1': quiz1.serialize()
        }
        return render(request, 'dc/takeQuiz.html', context=context)
