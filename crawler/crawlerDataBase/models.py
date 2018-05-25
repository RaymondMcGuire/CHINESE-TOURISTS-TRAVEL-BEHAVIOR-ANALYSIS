from django.db import models

class Article(models.Model):
    articleName = models.CharField(max_length=100)
    authorPos = models.CharField(max_length=20)
    authorSex = models.CharField(max_length=20)
    startTime = models.CharField(max_length=50)
    people = models.CharField(max_length=50)
    duringDay = models.CharField(max_length=50)
    cost = models.CharField(max_length=20)
    articleInfo = models.TextField()
    keyWords = models.TextField()
    href = models.TextField(null=True)