from django.http import JsonResponse
from .models import Set, User, Folder

def fetchSets(request,user):
    sets = Set.objects.filter(author=User.objects.get(username=user))
    return JsonResponse([set.serialize() for set in sets], safe=False)


def fetchFolders(request, user):
    folders = Folder.objects.filter(author=User.objects.get(username=user))
    return JsonResponse([folder.serialize() for folder in folders], safe=False)