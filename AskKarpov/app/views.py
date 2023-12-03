from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .forms import LoginForm, RegisterForm, AnswerForm
from django.urls import reverse

from .models import Question


def paginate(request, objects, per_page=10):
    page_number = request.GET.get('page')
    paginator = Paginator(objects, per_page)

    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page = paginator.get_page(1)

    return page


@login_required(login_url='login', redirect_field_name='continue')
def index(request):
    try:
        questions = Question.objects.new()
        return render(request, template_name='index.html',
                      context={'questions': paginate(request, questions), 'user': request.user})
    except Question.DoesNotExist:
        raise Http404("Вопросы не найдены")


@login_required(login_url='login', redirect_field_name='continue')
def question(request, question_id):
    try:
        item = Question.objects.get(id=question_id)
        answers = item.answers.new()

        if request.method == 'GET':
            answer_form = AnswerForm()
        if request.method == 'POST':
            answer_form = AnswerForm(request.POST)
            if answer_form.is_valid():
                answer = answer_form.save(question=item, author=request.user.profile)
                return redirect('question', question_id=question_id)
        else:
            form = AnswerForm()

        return render(request, template_name='question.html',
                      context={'question': item, 'questions': paginate(request, answers), 'form': answer_form})
    except Question.DoesNotExist:
        raise Http404("Вопрос не найден")


@login_required(login_url='login', redirect_field_name='continue')
def hot_question(request):
    try:
        best_questions = Question.objects.best()
        return render(request, template_name='hot-question.html',
                      context={'questions': paginate(request, best_questions)})
    except Question.DoesNotExist:
        raise Http404("Лучшие вопросы не найдены")


@login_required(login_url='login', redirect_field_name='continue')
def tag(request, tag_name):
    try:
        questions_with_tag = Question.objects.tag(tag_name=tag_name)
        return render(request, template_name='tag.html',
                      context={'questions': paginate(request, questions_with_tag), 'tags': tag_name})
    except Question.DoesNotExist:
        raise Http404("Вопросы по тэгу не найдены")


@csrf_protect
def login(request):
    if request.method == 'GET':
        login_form = LoginForm(request.POST)
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user is not None:
                auth_login(request, user)
                return redirect(request.GET.get('continue', '/'))
            else:
                login_form.add_error('username', "Wrong password and user does not exist.")
                login_form.add_error('password', "Wrong password and user does not exist.")

    return render(request, template_name='login.html', context={"form": login_form})


def logout(request):
    auth_logout(request)
    return redirect(reverse('login'))


def signup(request):
    if request.method == 'GET':
        user_form = RegisterForm()
    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)
        user_form = RegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user = user_form.save()
            if user:
                auth_login(request, user)
                return redirect(request.GET.get('continue', '/'))
            else:
                user_form.add_error(None, error="User saving error!")

    return render(request, template_name='signup.html', context={"form": user_form})


@login_required(login_url='login', redirect_field_name='continue')
def ask(request):
    return render(request, template_name='ask.html')


@login_required(login_url='login', redirect_field_name='continue')
def settings(request):
    return render(request, template_name='settings.html')
