from rest_framework import serializers
from .models import Lyb

class LybSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lyb
        fields = '__all__'









