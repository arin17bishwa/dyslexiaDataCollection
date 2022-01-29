from django.urls import path
from .views import (
    takeQuizView
)

app_name = 'dc'

urlpatterns = [
    path('', takeQuizView, name='takeQuiz'),
]
