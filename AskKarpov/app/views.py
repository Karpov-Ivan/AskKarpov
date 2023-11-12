from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import Http404

from .models import Question


def paginate(request, objects, per_page=5):
    page_number = request.GET.get('page')
    paginator = Paginator(objects, per_page)

    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page = paginator.get_page(1)

    return page


def index(request):
    try:
        questions = Question.objects.new()
        return render(request, template_name='index.html', context={'questions': paginate(request, questions)})
    except Question.DoesNotExist:
        raise Http404("Вопросы не найдены")


def question(request, question_id):
    try:
        item = Question.objects.get(id=question_id)
        answers = item.answers.new()
        return render(request, template_name='question.html',
                      context={'question': item, 'questions': paginate(request, answers)})
    except Question.DoesNotExist:
        raise Http404("Вопрос не найден")


def hot_question(request):
    try:
        best_questions = Question.objects.best()
        return render(request, template_name='hot-question.html',
                      context={'questions': paginate(request, best_questions)})
    except Question.DoesNotExist:
        raise Http404("Лучшие вопросы не найдены")


def tag(request, tag_name):
    try:
        questions_with_tag = Question.objects.tag(tag_name=tag_name)
        return render(request, template_name='tag.html',
                      context={'questions': paginate(request, questions_with_tag), 'tags': tag_name})
    except Question.DoesNotExist:
        raise Http404("Вопросы по тэгу не найдены")


def login(request):
    return render(request, template_name='login.html')


def signup(request):
    return render(request, template_name='signup.html')


def ask(request):
    return render(request, template_name='ask.html')


def settings(request):
    return render(request, template_name='settings.html')
