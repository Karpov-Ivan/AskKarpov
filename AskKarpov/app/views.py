from django.shortcuts import render
from django.core.paginator import Paginator

QUESTIONS = [
    {
        'id': i,
        'title': f'Question {i}',
        'content': f'Long lorem ipsum {i}'
    } for i in range(20)
]

ANSWERS = [
    {
        'id': i,
        'content': f'Long lorem ipsum {i}'
    } for i in range(15)
]


def paginate(request, objects, per_page=5):
    page_number = request.GET.get('page')
    paginator = Paginator(objects, per_page)

    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page = paginator.get_page(1)

    return page

def index(request):
    return render(request, template_name='index.html', context={'questions': paginate(request, QUESTIONS)})


def question(request, question_id):
    item = QUESTIONS[question_id]
    return render(request, template_name='question.html',
                  context={'question': item, 'questions': paginate(request, ANSWERS)})

def hot_question(request):
    return render(request, template_name='hot-question.html', context={'questions': paginate(request, QUESTIONS)})

def tag(request, tag_name):
    return render(request, template_name='tag.html',
                  context={'questions': paginate(request, QUESTIONS), 'tags': tag_name})

def login(request):
    return render(request, template_name='login.html')

def signup(request):
    return render(request, template_name='signup.html')

def ask(request):
    return render(request, template_name='ask.html')

def settings(request):
    return render(request, template_name='settings.html')