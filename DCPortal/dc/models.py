from django.db import models


# Create your models here.
def upload_location(instance, filename, **kwargs):
    file_path = 'r4/{_id:05d}_{filename}'.format(
        _id=instance.id,
        filename=filename
    )
    return file_path


class Data(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)
    age = models.SmallIntegerField(null=False)
    score1 = models.SmallIntegerField(default=0)
    score2 = models.SmallIntegerField(default=0)
    score3 = models.SmallIntegerField(default=0)
    score4 = models.SmallIntegerField(default=0)
    answer1 = models.JSONField(null=True)
    answer2 = models.JSONField(null=True)
    answer3 = models.JSONField(null=True)
    image = models.FileField(
        upload_to=upload_location,
        blank=True,
        null=True
    )
    submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Name:{} Age:{} ({},{},{})".format(
            self.name,
            self.age,
            self.score1, self.score2, self.score3
        )

    def __repr__(self):
        return self.__str__()
