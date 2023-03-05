from django.shortcuts import render
from rest_framework import viewsets
from .models import Lyb
from .serializers import LybSerializer
# Create your views here.



class LybViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Lyb.objects.all().order_by('-posttime')
    serializer_class = LybSerializer
    # permission_classes = [permissions.IsAuthenticated]



