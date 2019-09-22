from django.db import models

# Create your models here.


class Registration(models.Model):

    FName = models.CharField(max_length=30)
    LName = models.CharField(max_length=30)
    Email = models.EmailField(max_length=30, primary_key=True)
    Mobile = models.CharField(max_length=30)
    Password = models.CharField(max_length=30)

    def __str__(self):
        return self.FName+" "+self.LName