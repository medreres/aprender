from email import message
import json
from multiprocessing.dummy import active_children
from random import random
from django.http import JsonResponse
from .models import LearnWay, Set, User, Folder, Word
from django.contrib import messages
from random import randint, sample, shuffle
from django.views.decorators.csrf import csrf_exempt
WORDSPERSET = 10


# fetch sets via ajax
def fetchSets(request, user):
    sets = Set.objects.filter(author=User.objects.get(username=user))
    return JsonResponse([set.serialize() for set in sets], safe=False)

# fetch folde via ajax


def fetchFolders(request, user):
    folders = Folder.objects.filter(author=User.objects.get(username=user))
    return JsonResponse([folder.serialize() for folder in folders], safe=False)

# create learn path for user


def createLearnPath(request, id):
    # handle wrong id of set to learn
    setToLearn = Set.objects.filter(pk=id)
    if len(setToLearn) == 0:
        return JsonResponse({f"error': 'Set with such id {id} doesnt exist!"})

    newPath = LearnWay.objects.create(
        author=request.user,
        set=setToLearn[0],
        lastWord=setToLearn[0].words.first()
    )

    # add all words to poor known
    # get all words from this set
    newPath.poorKnown.add(*setToLearn[0].words.all())

    return JsonResponse({'success': "Learn Path successfully created!"})


def nextWord(request, id):
    learnPath = LearnWay.objects.filter(author=request.user).filter(set__pk=id)
    # if set doesn't exist but somehow learnway is still available
    if len(learnPath) == 0:
        messages.error(request, 'Internal error. Set is not found')
        return JsonResponse({'error': "Set is not founded"})
    learnPath = learnPath[0]

    # !CRUTCHES
    # ?django manytomany rel doesnt support numeration of elemnt in manytomany,
    # so i created list of all words in many tomany, get index of last word
    # and fetch word with index greater by 1
    allWords = [*Set.objects.filter(pk=id)[0].words.all()]
    print(allWords)
    indexOfWord = (allWords.index(learnPath.lastWord)+1) % len(allWords)
    learnPath.lastWord = allWords[indexOfWord]
    learnPath.save()

    return JsonResponse({'word': learnPath.lastWord.term, 'definition': learnPath.lastWord.definition, 'index': indexOfWord + 1, 'allWordsCount': len(allWords)}, status=200)


def currentWord(request, id):
    learnPath = LearnWay.objects.filter(author=request.user).filter(set__pk=id)
    # if set doesn't exist but somehow learnway is still available
    if len(learnPath) == 0:
        messages.error(request, 'Internal error. Set is not found')
        return JsonResponse({'error': "Set is not founded"})
    learnPath = learnPath[0]
    allWords = [*Set.objects.filter(pk=id)[0].words.all()]
    indexOfWord = (allWords.index(learnPath.lastWord))
    return JsonResponse({'word': learnPath.lastWord.term, 'definition': learnPath.lastWord.definition, 'index': indexOfWord + 1, 'allWordsCount': len(allWords)}, status=200)


def prevWord(request, id):
    learnPath = LearnWay.objects.filter(author=request.user).filter(set__pk=id)
    # if set doesn't exist but somehow learnway is still available
    if len(learnPath) == 0:
        messages.error(request, 'Internal error. Set is not found')
        return JsonResponse({'error': "Set is not founded"})
    learnPath = learnPath[0]

    # !CRUTCHES
    # ?django manytomany rel doesnt support numeration of elemnt in manytomany,
    # so i created list of all words in many tomany, get index of last word
    # and fetch word with index greater by 1
    allWords = [*Set.objects.filter(pk=id)[0].words.all()]
    indexOfWord = (allWords.index(learnPath.lastWord)-1) % len(allWords)
    learnPath.lastWord = allWords[indexOfWord]
    learnPath.save()

    return JsonResponse({'word': learnPath.lastWord.term, 'definition': learnPath.lastWord.definition, 'index': indexOfWord + 1, 'allWordsCount': len(allWords)}, status=200)


def getWords(request, id):
    """getWord() sends a list of 10 words, if availble, or all the words left in one of the sets(poorKnown or intermediateKnown)"""

    # find the learnpath in database
    learnPath = LearnWay.objects.filter(author=request.user).get(set__pk=id)

    # if there are any words, show menu to restart the learnPath
    if learnPath.set.words.count() == learnPath.wellKnown.count():
        return JsonResponse({'finish': 'The learn way is finished'}, status=200)


    # if poorknown set is empty, take word from intermediate
    if learnPath.poorKnown.count() > 0:
        studySet = learnPath.poorKnown
    else:
        studySet = learnPath.intermediateKnown

    # get a list of words from the set available
    numberOfWordsToStudy = 10 if studySet.count() > 10 else studySet.count()

    # list of words to be studied
    wordsToStudy = []

    # all words from the set
    allWords = ([*studySet.all()])
    for i in range(numberOfWordsToStudy):
        # get index of random word
        randIndex = randint(0, len(allWords) - 1)
        randWord = allWords[randIndex]

        # remove that word from all words to avoid repetition
        allWords.remove(randWord)

        # get random answer, including the right one
        possibleAnswers = [randWord.definition]

        # if overall number of words less than 4, then select only words available
        if learnPath.set.words.count() < 4:
            possibleAnswers.extend(sample([word.definition for word in learnPath.set.words.all(
            ) if word.definition != randWord.definition], learnPath.set.words.count() - 1))
        else:
            possibleAnswers.extend(sample([word.definition for word in learnPath.set.words.all(
            ) if word.definition != randWord.definition], 3))

        # shuffle all words to prevent pattern
        shuffle(possibleAnswers)

        # add the word to the list
        wordToStudy = {'word': randWord.serialize(
        ), 'definitions': possibleAnswers}
        wordsToStudy.append(wordToStudy)
    return JsonResponse({'words': wordsToStudy, 'numberOfWordsToStudy': numberOfWordsToStudy, }, status=200)


# list to remember all words learned to show them at the end of the round
@csrf_exempt
def check(request, id):
    # compare two words, if their definitions are equal , then answer is right
    givenWord = json.loads(request.body)
    actualWord = Word.objects.get(pk=givenWord['id'])

    learnPath = LearnWay.objects.filter(
        author=request.user).filter(set__pk=id)[0]
    # if answer is right remove this word from poor known and add to intermediate known

    if actualWord.definition == givenWord['definition']:
        moveToUpperRank(learnPath, actualWord)
        answer = True
    else:
        moveToLowerRank(learnPath, actualWord)
        answer = False

    return JsonResponse({'answer': answer}, status=200)


def moveToUpperRank(learnPath: LearnWay, word: Word):
    # if word in learnPath.poor, rise it to intermediate
    if word in learnPath.poorKnown.all():
        learnPath.poorKnown.remove(word)
        learnPath.intermediateKnown.add(word)
    elif word in learnPath.intermediateKnown.all():
        learnPath.intermediateKnown.remove(word)
        learnPath.wellKnown.add(word)


def moveToLowerRank(learnPath: LearnWay, word: Word):
    # if word in wellknown, downgrade it to intermediate
    if word in learnPath.wellKnown.all():
        learnPath.wellKnown.remove(word)
        learnPath.intermediateKnown.add(word)
    elif word in learnPath.intermediateKnown.all():
        learnPath.intermediateKnown.remove(word)
        learnPath.poorKnown.add(word)


# if learning is finihsed, propose restart learning
def resetLearnWay(learnPath: LearnWay):
    learnPath.intermediateKnown.remove(learnPath.intermediateKnown.all())
    learnPath.wellKnown.remove(learnPath.wellKnown.all())
    learnPath.poorKnown.add(*learnPath.set.words.all())
    return JsonResponse({'success': 'Learn Way successfully restarted!'})
