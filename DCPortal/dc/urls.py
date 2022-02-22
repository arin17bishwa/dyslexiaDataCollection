from django.urls import path
from .views import (
    takeQuizView,
    takeQuizViewOlder,
)

app_name = 'dc'

urlpatterns = [
    path('1/', takeQuizView, name='takeQuiz'),
    path('2/', takeQuizViewOlder, name='takeQuizOlder'),
]
