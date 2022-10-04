from datetime import datetime
from doctest import debug_script
from operator import is_
from random import randint, sample, shuffle
from secrets import randbelow
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import LoginForm, RegisterForm, CreateSet, CreateFolder, TestForm
from .models import Folder, User, Word, Set, LearnWay
from django.contrib.auth import authenticate, login, logout
# from django.shortcuts import redirect
from django.contrib import messages  # import messages
from django.contrib.auth.decorators import login_required
# from django.utils.http import is_safe_url
from django.utils.http import url_has_allowed_host_and_scheme
from .helper import fetchSets, fetchFolders, createLearnPath, nextWord, currentWord, prevWord, getWords, check, restartLearnWay

# Create your views here.


def index(request):
    # messages.success(request, "Success message")
    return render(request, 'aprender/index.html', {
        'LoginForm': LoginForm,
        'CreateFolder': CreateFolder()
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
    if next_url is not None:
        return redirect(next_url)

    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.user:
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
    })


@login_required
def sets(request, user):
    return render(request, 'aprender/sets.html',
                  {
                      'CreateFolder': CreateFolder(),
                      'LoginForm': LoginForm(),
                  })


def set(request, id):
    # find out if user has already started learning way
    print('SET')
    learnStarted = LearnWay.objects.filter(author=request.user).filter(
        set__pk=id).count() > 0 if request.user.is_authenticated else False

    return render(request, 'aprender/set.html', {
        'set': Set.objects.get(pk=id).serialize(),
        'learnStarted': learnStarted,
        'id': id,
        'LoginForm': LoginForm(),
        'TestForm': TestForm(),
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

    return HttpResponseRedirect(reverse('folders', args=(request.user,)))


@login_required
def folders(request, user):
    return render(request, 'aprender/folders.html', {
        'username': user,
    })


@login_required
def folder(request, id):
    return HttpResponse("TODO")


@login_required
def profile(request, user):
    return render(request, 'aprender/profile.html')


@login_required
def flashcards(request, id):
    return render(request, 'aprender/flashcards.html')


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

    return render(request, 'aprender/test.html', {
        'questions': createTest(request, id, form.cleaned_data),
        'numberOfWordsGeneral': form.cleaned_data['questionLimit'],
        'id': id,
    })


def testCheck(request, id):
    written = request.POST.getlist('written')
    return HttpResponseRedirect(reverse('index'))


def createTest(request, id, testForm) -> list:

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
    allWords = [*(learnPath.poorKnown.all()), *
                (learnPath.intermediateKnown.all()), *(learnPath.wellKnown.all())]

    if testForm['questionLimit'] > len(allWords):
        # TODO
        messages.warning(request, 'Too few words in dictionary')
        print("EROR\n\n")
    # print('ALL WORDS')
    # print('----------------------------------')
    # print(allWords)
    # print('----------------------------------')
    for key in questions.keys():
        # numberOfQuestionTypes[key]
        for i in range(numberOfQuestionTypes[key]):
            # chose random word in accordace to question type
            if key == 'multiple':
                questions[key].append(getMultipleWord(allWords))
            elif key == 'written':
                questions[key].append(getWrittenWord(allWords))
            elif key == 'true':
                questions[key].append(getTrueWord(allWords))
    return questions


def getRandWord(words: list) -> Word:
    # get rand word
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


def getMultipleWord(words: list):
    randWord = getRandWord(words)
    # add definition of the word, rest chose randomly

    # !!! TODO
    definition = [randWord.definition, *
                  ([word.definition for word in sample(words, 3)])]
    shuffle(definition)
    return {'word': randWord.term, 'definition': definition, 'id': randWord.id}


def getTrueWord(words: list):
    randWord = getRandWord(words)
    # chose definition for true/false statemnt on random
    faultyDef = sample([*words, randWord], 1)[0].definition
    return {'word': randWord.term, 'definitionRandom': faultyDef, 'definitionTrue': randWord.definition, 'id': randWord.id}
