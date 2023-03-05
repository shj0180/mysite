from django.db import models

# Create your models here.



class Lyb(models.Model):
    title = models.CharField(max_length=100, null=False)
    author = models.CharField(max_length=50)
    content = models.TextField(max_length=1000)
    posttime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'd_lyb'
        