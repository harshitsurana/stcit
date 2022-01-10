from django.db import models
from django.contrib.auth.models import User


class player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    current_question = models.IntegerField(default=1)
    score = models.IntegerField(default=0)
    final_score = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    timestamp = models.DateTimeField()
    slot = models.IntegerField(default=0)
    qualified = models.BooleanField(default=False)

    def __str__(self):
        return self.name



class question(models.Model):
    Q_number = models.IntegerField()
    Question = models.TextField()
    image = models.ImageField(upload_to='images', blank=True)
    option1 = models.CharField(max_length=200, null=True)
    option2 = models.CharField(max_length=200, null=True)
    option3 = models.CharField(max_length=200, null=True)
    option4 = models.CharField(max_length=200, null=True)
    answer = models.CharField(max_length=200)
    correct = models.IntegerField(default=0)
    wrong = models.IntegerField(default=0)
    accuracy = models.FloatField(default=0)

    def __str__(self):
        return str(self.Q_number) + " " + self.Question