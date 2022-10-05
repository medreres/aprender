from email.policy import default
from multiprocessing import AuthenticationError
from re import T
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    favoriteSets = models.ManyToManyField('Set', blank=True)
    favoriteFolders = models.ManyToManyField('Folder', blank=True)
    # recentSets stores id of sets recently visited to be shown on main, stored as JSON
    recentSetsJson = models.CharField(max_length=64, default='[]')
    # ? could be better?
    # implement back end algorithm for learning words via card
    # the main goal is to separe words into 3 categories: well-known, intermediate and poor-known
    # if user gives the right answer for the same words 2 times in a row, the word acquires a higher state
    # Also there is need to implement index  of last word for the carousel in a set's main section to keep track of last word
    # ? maybe creating a model for all those 3 categories and last index will work?



class LearnWay(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    set = models.ForeignKey('Set', on_delete=models.Case, null=True)
    # TODO implement case of deleting last word examined
    
    
    # rank of knowing words
    lastWord = models.ForeignKey('Word', null=True,blank=True, on_delete=models.SET_NULL, related_name='lastKnown')
    poorKnown = models.ManyToManyField('Word', null=True,blank=True, related_name='poorKnown')
    intermediateKnown = models.ManyToManyField('Word', null=True,blank=True, related_name='intermediateKnown')
    wellKnown = models.ManyToManyField('Word', null=True,blank=True, related_name='wellKnown')

    def __str__(self) -> str:
        return f"{self.author.username} learns {self.set.label}"


class Word(models.Model):
    term = models.CharField(max_length=255)
    definition = models.CharField(max_length=500)

    def __str__(self):
        return f"({self.id}) {self.term} - {self.definition} "

    def serialize(self):
        return {
            'id': self.id,
            'term': self.term,
            'definition': self.definition
        }


class Set(models.Model):
    words = models.ManyToManyField(Word, related_name="words")
    label = models.CharField(max_length=255)
    description = models.CharField(max_length=512, null=True, blank=True)
    date = models.DateTimeField()
    # if author is null, then author was deleted, but set was saved
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # words that user like to learn more than the others
    chosenWords = models.ManyToManyField(Word, related_name="chosenWords", blank=True)

    def __str__(self) -> str:
        return f"{self.label} {self.id}"

    def serialize(self):
        return {
            'id': self.id,
            'label': self.label,
            'wordsNumber': self.words.count(),
            'author': self.author.username
        }

    def get_all_words(self):
        return self.words


class Folder(models.Model):
    sets = models.ManyToManyField(Set)
    label = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField()

    def serialize(self):
        return {
            'id': self.id,
            'label': self.label,
            'setsNumber': self.sets.count(),
            'author': self.author.username,
            'sets': [set.serialize() for set in self.sets.all()]
        }
