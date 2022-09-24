from multiprocessing import AuthenticationError
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    favoriteSets = models.ManyToManyField('Set')
    favoriteFolders = models.ManyToManyField('Folder')

# model for words


class Word(models.Model):
    term = models.CharField(max_length=255)
    definition = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.term} - {self.definition} "


class Set(models.Model):
    words = models.ManyToManyField(Word, related_name="words")
    label = models.CharField(max_length=255)
    date = models.DateTimeField()
    # if author is null, then author was deleted, but set was saved
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # words that user like to learn more than the others
    chosenWords = models.ManyToManyField(Word, related_name="chosenWords", blank=True)


class Folder(models.Model):
    sets = models.ManyToManyField(Set)
    label = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField()
