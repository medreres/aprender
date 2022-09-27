from email import message
from django.http import JsonResponse
from .models import LearnWay, Set, User, Folder
from django.contrib import messages


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


def fetchNextWord(request, id):
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
    
    return JsonResponse({'word': learnPath.lastWord.term, 'definition':learnPath.lastWord.definition , 'index': indexOfWord}, status=200)