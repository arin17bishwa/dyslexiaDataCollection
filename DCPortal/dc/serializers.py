from rest_framework import serializers
from .models import Data


class DataSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj: Data):
        req = self.context['request']
        return req.build_absolute_uri(obj.image.url)

    class Meta:
        model = Data
        fields = ['id', 'name', 'age', 'score1', 'score2', 'score3', 'score4', 'answer1', 'answer2', 'answer3',
                  'image_url', 'submitted']
