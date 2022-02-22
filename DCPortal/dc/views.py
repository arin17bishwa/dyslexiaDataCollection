import csv
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from .models import Data, Data2
from .constants import Quiz1, Quiz2, Quiz3, Quiz4, OlderQuiz1, OlderQuiz2, OlderQuiz3, OlderQuiz4
from .forms import UploadForm
from .serializers import DataSerializer


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
        round1 = quiz1.score(res)
        round2 = quiz2.score(res)
        round3 = quiz3.score(res)
        form = UploadForm(request.FILES or None)
        if form.is_valid() or 1:
            obj = Data(
                name=name,
                age=int(age or '0'),
                score1=round1['score'],
                answer1=round1['responses'],
                score2=round2['score'],
                answer2=round2['responses'],
                score3=round3['score'],
                answer3=round3['responses'],
            )
            obj.save()
            if request.FILES.get('image'):
                obj.image = request.FILES['image']
                obj.save()
        return redirect('dc:takeQuiz')
    else:
        context = {}
        quiz1 = Quiz1()
        quiz2 = Quiz2()
        quiz3 = Quiz3()
        quiz4 = Quiz4()
        context = {
            'quiz1': quiz1.serialize(),
            'quiz2': quiz2.serialize(),
            'quiz3': quiz3.serialize(),
            'quiz4': quiz4.serialize(),
        }
        # print(context['quiz3'].keys())
        return render(request, 'dc/takeQuiz.html', context=context)


def takeQuizViewOlder(request):
    if request.method == 'POST':
        quiz1 = OlderQuiz1()
        quiz2 = OlderQuiz2()
        quiz3 = OlderQuiz3()
        quiz4 = OlderQuiz4()
        res = request.POST
        name = res['name']
        age = res['age']
        round1 = quiz1.score(res)
        round2 = quiz2.score(res)
        round3 = quiz3.score(res)
        form = UploadForm(request.FILES or None)
        if form.is_valid() or 1:
            obj = Data2(
                name=name,
                age=int(age or '0'),
                score1=round1['score'],
                answer1=round1['responses'],
                score2=round2['score'],
                answer2=round2['responses'],
                score3=round3['score'],
                answer3=round3['responses'],
            )
            obj.save()
            if request.FILES.get('image'):
                obj.image = request.FILES['image']
                obj.save()
        return redirect('dc:takeQuizOlder')
    else:
        context = {}
        quiz1 = OlderQuiz1()
        quiz2 = OlderQuiz2()
        quiz3 = OlderQuiz3()
        quiz4 = OlderQuiz4()
        print(quiz1.files)
        context = {
            'quiz1': quiz1.serialize(),
            'quiz2': quiz2.serialize(),
            'quiz3': quiz3.serialize(),
            'quiz4': quiz4.serialize(),
        }
        # print(context['quiz3'].keys())
        return render(request, 'dc/takeQuiz.html', context=context)


def home(request):
    return render(request, 'home.html')


@login_required(login_url='/admin/login')
@api_view(['GET', ])
def downloadCSVView(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    serializer = DataSerializer(Data.objects.all(), many=True, context={'request': request})
    cols = [field for field in DataSerializer().fields]
    writer = csv.DictWriter(response, fieldnames=cols)
    writer.writeheader()
    writer.writerows(serializer.data)
    return response
