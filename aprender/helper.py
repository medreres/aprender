from django.http import JsonResponse
from .models import LearnWay, Set, User, Folder


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
