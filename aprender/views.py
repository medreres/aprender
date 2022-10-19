from datetime import datetime
import json
import copy
from random import randint, sample, shuffle
from secrets import randbelow
from xmlrpc.client import Boolean
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from .forms import LoginForm, RegisterForm, CreateSet, CreateFolder, TestForm, EditUser
from .models import Folder, User, Word, Set, LearnWay
from django.contrib.auth import authenticate, login, logout
# from django.shortcuts import redirect
from django.contrib import messages  # import messages
from django.contrib.auth.decorators import login_required
# from django.utils.http import is_safe_url
from django.utils.http import url_has_allowed_host_and_scheme
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404

from .helper import fetchSets, fetchFolders, createLearnPath, nextWord, currentWord, prevWord, getWords, check, restartLearnWay, getWordsToEdit, getNumberOfPages, saveChanges, deleteWord, addSet, getSetsId, folderEdit, favorite

# Create your views here.


class PassowrdsChangeView(SuccessMessageMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('settings')
    success_message = "Your password was changed successfully!"


def index(request):

    allSets = Set.objects.all()
    if request.user.is_authenticated:
        # get list of recent items in json
        recentSetsId = request.user.recentSetsJson
        # parse it into list
        try:
            recentSetsId = json.loads(recentSetsId)
            recentSets = Set.objects.filter(pk__in=recentSetsId)
        except:
            recentSets = None

    # print(recentSets)
    return render(request, 'aprender/index.html', {
        'LoginForm': LoginForm,
        'CreateFolder': CreateFolder,
        'recentSets':  recentSets if request.user.is_authenticated else None,
        'allSets': allSets
    })


def changePassword(request):
    user = User.objects.get(pk=request.user.id)
    # passwordOld = request.POST['passwordOld']
    # passwordNew = request.POST['passwordNew']
    # print(passwordOld, passwordNew)
    print(request.POST)
    return HttpResponseRedirect(reverse('settings'))


def settings(request):

    if not request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = EditUser(request.POST, request.FILES)
        if not form.is_valid():
            # TODO throw error
            pass

        user = User.objects.get(pk=request.user.id)
        if form.cleaned_data['profile_image'] is None:
            form.cleaned_data['profile_image'] = user.profile_image
        elif form.cleaned_data['profile_image'] == False:
            user.profile_image.delete()
        user.__dict__.update(form.cleaned_data)
        # user.profile_image = form.cleaned_data['profile_image']
        user.save()
        messages.success(request, 'Changed successfully!')
        return HttpResponseRedirect(reverse('settings'))
    user = User.objects.get(pk=request.user.id)
    return render(request, 'aprender/settings.html', {
        'user': user,
        'EditUser': EditUser(initial=model_to_dict(user))
    })


def loginUser(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method!'})
    form = LoginForm(request.POST)

    # check form for validity, else show error
    if not form.is_valid():
        messages.error(request, "Error. Invalid form")
        return JsonResponse({'error': 'Invalid form!'})

    user = authenticate(
        request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
    if user is not None:
        logUser(request, user)
    else:
        messages.warning(
            request, "User with such password/username doesnt exist")
        return JsonResponse({'error': 'User doesnt exist!'})

    # get page from which user logged
    next_url = request.GET.get('next', None)
    if next_url is not None:
        return redirect(next_url)

    return HttpResponseRedirect(reverse('index'))


def logoutUser(request):
    # log out and reverse back to main page
    logout(request)
    next_url = request.GET.get('next', None)
    print(next_url)
    if next_url is not None:
        try:
            return redirect(next_url)
        except:
            return HttpResponseRedirect(reverse('index'))

    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged!')
        return HttpResponseRedirect(reverse('index'))

    if request.method == 'POST':
        # TODO throw warning
        pass

        form = RegisterForm(request.POST)
        if not form.is_valid():
            messages.error(request, "Error. Invalid form")

        password = form.cleaned_data['password']
        password2 = form.cleaned_data['password2']
        if password != password2:
            # TODO throw an error
            # ? OR better to do it on frontend?
            pass

        # ? Check on front whether username is taken
        username = form.cleaned_data['username']

        # ? Check on front whether email is taken
        email = form.cleaned_data['email']

        # * register new user and sign in
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.warning(
                request, "User with such username already exists!")
            return HttpResponseRedirect(reverse('register'))

        logUser(request, user)
        # print(user)
        # redirect to main page
        return HttpResponseRedirect(reverse('index'))

    else:
        return render(request, 'aprender/register.html', {
            'RegisterForm': RegisterForm(),
            'LoginForm': LoginForm()
        })


def logUser(request, user):
    login(request, user)
    messages.success(request, f'You are now logged in as {user.username}')


@login_required
def createset(request):
    if request.method == 'POST':
        form = CreateSet(request.POST)

        if not form.is_valid():
            messages.error(request, 'Form is not valid')
            return HttpResponseRedirect(reverse('createset'))

        # ! CRUTCHES
        formFields = request.POST
        # didn't manage to implement correctly, so all terms and their definitions
        # will be fetched via request.POST than it would be better to do via django form

        # iterate through all terms and create corresponding object Word
        wordsObjectList = []
        for (word, definition) in zip(formFields.getlist('words'), formFields.getlist('definitions')):
            # create Word model for every word-definition
            wordModel = Word.objects.create(term=word, definition=definition)
            wordsObjectList.append(wordModel)

        studySet = Set.objects.create(
            label=form.cleaned_data['label'],
            date=datetime.now(),
            author=request.user,
            description=form.cleaned_data['description']
        )
        studySet.words.add(*[w.id for w in wordsObjectList])

        return HttpResponseRedirect(reverse('createset'))

    return render(request, 'aprender/createset.html', {
        'CreateSet': CreateSet(),
        'CreateFolder': CreateFolder()
    })


def search(request):
    body = request.GET

    return render(request, 'aprender/search.html', {
        'result': Set.objects.filter(label__contains=body['search'])
    })


@login_required
def sets(request, user):
    return render(request, 'aprender/sets.html',
                  {
                      'CreateFolder': CreateFolder(),
                      'LoginForm': LoginForm(),
                  })


@csrf_exempt
def toggleFavorite(request, id):
    set = Set.objects.get(pk=id)
    user = User.objects.get(pk=request.user.id)
    favoriteSets = user.favoriteSets
    isFavorite = favoriteSets.contains(set)

    if not isFavorite:
        user.favoriteSets.add(set)
        user.save()
        return JsonResponse({'add': 'liked successfully!'}, status=200)
    else:
        user.favoriteSets.remove(set)
        user.save()
        return JsonResponse({'delete': 'disliked successfully!'}, status=200)


def set(request, id):

    set = Set.objects.get(pk=id)

    if request.user.is_authenticated:
        isFavorite = User.objects.get(
            pk=request.user.id).favoriteSets.contains(set)
    else:
        isFavorite = False

    # find out if user has already started learning way
    learnStarted = LearnWay.objects.filter(author=request.user).filter(
        set__pk=id).count() > 0 if request.user.is_authenticated else False

    # set = set

    # recentSets = request.user.recentSets
    # print(json.loads(recentSets))

    # print(json.dumps([1,3,], separators=(',',';')))

    # get recentSets from user, parse it, add or move, parse back to json and save
    if request.user.is_authenticated:

        recentSetsid = json.loads(request.user.recentSetsJson)

        if id in recentSetsid:
            recentSetsid.insert(0, recentSetsid.pop(recentSetsid.index(id)))
        else:
            recentSetsid.insert(0, id)
        recentSetsid = json.dumps(recentSetsid)
        user = User.objects.get(pk=request.user.id)
        user.recentSetsJson = recentSetsid
        user.save()

    # recentSets.append(set)

    return render(request, 'aprender/set.html', {
        'set': set,
        'learnStarted': learnStarted,
        'id': id,
        'LoginForm': LoginForm(),
        'TestForm': TestForm(),
        'isFavorite': isFavorite
    })


@login_required
def createfolder(request):
    if request.method != "POST":
        messages.error(request, 'Error. Wrong request method')
        return HttpResponseRedirect(reverse('index'))

    form = CreateFolder(request.POST)
    if not form.is_valid():
        messages.error(request, 'Error. Form is not valid')

    folder = Folder.objects.create(
        label=form.cleaned_data['label'],
        description=form.cleaned_data['description'],
        author=request.user,
        date=datetime.now()
    )

    return redirect('folder', folder.id)
    return HttpResponseRedirect(reverse('folders', args=(request.user,)))


@login_required
def folders(request, user):
    return render(request, 'aprender/folders.html', {
        'username': user,
    })


@login_required
def deleteFolder(request, id):
    Folder.objects.get(pk=id).delete()
    messages.success(request, 'Folder deleted successfully!')
    return HttpResponseRedirect(reverse('index'))


@login_required
def folder(request, id):
    try:
        folder = Folder.objects.get(pk=id)
    except:
        # TODO folder is not found
        return HttpResponseRedirect(reverse('index'))

    return render(request, 'aprender/folder.html', {
        'folder': folder.serialize(),
        'CreateFolder': CreateFolder(),
        'folderId': id
    })


def profile(request, user):

    return render(request, 'aprender/profile.html', {
        'LoginForm': LoginForm,
        'user': User.objects.get(username=user)
    })


@login_required
def flashcards(request, id):
    return render(request, 'aprender/flashcards.html', {
        'id': id
    })


def learn(request, id):
    return render(request, 'aprender/learn.html', {
        'id': id
    })


def test(request, id):
    form = TestForm(request.GET)
    # TODO
    if form.is_valid():
        pass
        # messages.warning(request, 'Form is not valid')

    # {'questionTypes': ['written', 'matching', 'multiple', 'true'], 'questionLimit': 10, 'starredTerms': 'starred', 'showImages': False}

    test = createTest(request, id, form.cleaned_data)
    print(test)
    if test == -1:
        return HttpResponseRedirect(reverse('set', kwargs={'id': id}))
    return render(request, 'aprender/test.html', {
        'questions': test,
        'numberOfWordsGeneral': form.cleaned_data['questionLimit'],
        'id': id,
    })


def testCheck(request, id):
    written = request.POST.getlist('written')
    return HttpResponseRedirect(reverse('index'))


def getAllWords(request, learnPath: LearnWay, questionLimit: int, starred):
    """Get all possible words from learnway"""
    allWords = []
    # if not only starred then get all words
    if starred == 'all':
        return [*(learnPath.set.words.all())]
    
    # if only starred then fetch poor known first
    allWords = [*(learnPath.poorKnown.all())]


    # if not enough, append from intermedate
    if questionLimit > len(allWords) and learnPath.intermediateKnown.count():
        allWords.extend(*(learnPath.intermediateKnown.all()))

    # if thats not enough, then add from wellknown
    if questionLimit > len(allWords) and learnPath.wellKnown.count():
        allWords.extend(*(learnPath.wellKnown.all()))

    # if not enough throw an error
    if questionLimit > len(allWords):
        return -1
    
    else:
        return allWords

def createTest(request, id, testForm) -> list:

    # TODO not starred choice

    # keys for accessing dictionary
    numberOfQuestionTypes = {'written': 0,
                             'matching': 0, 'multiple': 0, 'true': 0}
    # generate number of question of each type as even as possible
    for i in range(testForm['questionLimit']):
        # select questio type from form and spread number evenly
        questionType = testForm['questionTypes'][i %
                                                 len(testForm['questionTypes'])]
        numberOfQuestionTypes[questionType] += 1

    # for each question create list where words will be saved
    questions = {}
    for questionType in testForm['questionTypes']:
        questions[questionType] = []

    # fetch all words from all sets(poorKnown, intermediate and well) and randomly
    # choose for each question type(all are ought to be different)
    # TODO replace all instances of seraching user's path with one function
    learnPath = LearnWay.objects.filter(author=request.user).get(set__pk=id)
    allWords = getAllWords(request, learnPath, testForm['questionLimit'], testForm['starredTerms'])

    if allWords == -1:
        # TODO
        messages.warning(request, 'Too few words in dictionary')
        # return error
        return -1

    possibleAnswers = copy.deepcopy(allWords)
   

    
    

    # print('ALL WORDS')
    # print(allWords)

    # print('ALL WORDS')
    # print('----------------------------------')
    # print(allWords)
    # print('----------------------------------')
    for key in questions.keys():
        # numberOfQuestionTypes[key]
        for i in range(numberOfQuestionTypes[key]):
            # chose random word in accordace to question type
            if key == 'multiple':
                questions[key].append(getMultipleWord(allWords, possibleAnswers))
            elif key == 'written':
                questions[key].append(getWrittenWord(allWords))
            elif key == 'true':
                questions[key].append(getTrueWord(allWords, possibleAnswers))
    return questions


def getRandWord(words: list) -> Word:
    # get rand word
    # print('LEN\n')
    # print(len(words)-1)
    randInd = randint(0, len(words)-1)
    randWord = words[randInd]

    # delete this word from all words lst
    words.remove(randWord)
    return randWord


def getWrittenWord(words: list):
    """Choses random word to write, deletes it from array of all words"""

    randWord = getRandWord(words)

    # print({'word': randWord.term, 'definition': randWord.definition, 'id': randWord.id})
    return {'word': randWord.term, 'definition': randWord.definition, 'id': randWord.id}


def getMultipleWord(words: list, answers: list):
    randWord = getRandWord(words)

    possibleAnswers = answers[:]
    possibleAnswers.remove(randWord)
    # add definition of the word, rest chose randomly

    # TODO
    definition = [randWord.definition, *
                  ([word.definition for word  in sample(possibleAnswers, 3)])]
    shuffle(definition)
    return {'word': randWord.term, 'definition': definition, 'id': randWord.id}


def getTrueWord(words: list, answers: list):
    randWord = getRandWord(words)

    possibleAnswers = answers[:]
    possibleAnswers.remove(randWord)
    # chose definition for true/false statemnt on random
    faultyDef = sample([*possibleAnswers, randWord], 1)[0].definition
    return {'word': randWord.term, 'definitionRandom': faultyDef, 'definitionTrue': randWord.definition, 'id': randWord.id}

# TODO maybe


def match(request, id):
    return render(request, 'aprender/match.html', {
        'id': id
    })


def edit(request, id):

    set = Set.objects.get(pk=id)
    if not request.user.is_authenticated or set.author.id != request.user.id:
        messages.error(request, 'Permission denied')
        return HttpResponseRedirect(reverse('set', kwargs={'id': id}))

    return render(request, 'aprender/edit.html', {
        'id': id
    })
