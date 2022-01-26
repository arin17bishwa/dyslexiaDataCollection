from django.db import models


# Create your models here.


class Data(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)
    age = models.SmallIntegerField(null=False)
    score1 = models.SmallIntegerField(default=0)
    score2 = models.SmallIntegerField(default=0)
    score3 = models.SmallIntegerField(default=0)
    answer1 = models.JSONField(null=True)
    answer2 = models.JSONField(null=True)
    answer3 = models.JSONField(null=True)
