from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.paginator import Paginator
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.db import transaction
from django.forms.models import model_to_dict
from .models import Question, LikeQuestion, Answer, LikeAnswer, Tag, Profile
from .forms import LoginForm, RegisterForm, AnswerForm, ProfileForm, AskQuestionForm


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
        popular_tags = Tag.objects.get_popular_tags()
        top_users = Profile.objects.get_top_users_of_week()

        return render(request, template_name='index.html',
                      context={'questions': paginate(request, questions),
                               'popular_tags': popular_tags,
                               'top_users': top_users})
    except Question.DoesNotExist:
        raise Http404("No questions found")


@login_required(login_url='login', redirect_field_name='continue')
def question(request, question_id):
    try:
        item = Question.objects.get(id=question_id)
        answers = item.answers.new()
        popular_tags = Tag.objects.get_popular_tags()
        top_users = Profile.objects.get_top_users_of_week()

        if request.method == 'GET':
            answer_form = AnswerForm()
        if request.method == 'POST':
            answer_form = AnswerForm(request.POST)
            if answer_form.is_valid():
                answer = answer_form.save(question=item, author=request.user.profile)

                try:
                    answers = list(answers)
                    count = answers.index(answer)
                except ValueError:
                    count = 0

                page_number = count // 10 + 1

                anchor = f'#answer-{answer.id}'
                return HttpResponseRedirect(reverse('question', args=[question_id]) + f'?page={page_number}' + anchor)

        return render(request, template_name='question.html',
                      context={'question': item,
                               'questions': paginate(request, answers),
                               'popular_tags': popular_tags,
                               'form': answer_form,
                               'top_users': top_users})
    except Question.DoesNotExist:
        raise Http404("The question was not found")


@login_required(login_url='login', redirect_field_name='continue')
def hot_question(request):
    try:
        best_questions = Question.objects.best()
        popular_tags = Tag.objects.get_popular_tags()
        top_users = Profile.objects.get_top_users_of_week()

        return render(request, template_name='hot-question.html',
                      context={'questions': paginate(request, best_questions),
                               'popular_tags': popular_tags,
                               'top_users': top_users})
    except Question.DoesNotExist:
        raise Http404("No better questions found")


@login_required(login_url='login', redirect_field_name='continue')
def tag(request, tag_name):
    try:
        questions_with_tag = Question.objects.tag(tag_name=tag_name)
        popular_tags = Tag.objects.get_popular_tags()
        top_users = Profile.objects.get_top_users_of_week()

        return render(request, template_name='tag.html',
                      context={'questions': paginate(request, questions_with_tag),
                               'tags': tag_name,
                               'popular_tags': popular_tags,
                               'top_users': top_users})
    except Question.DoesNotExist:
        raise Http404("Questions about the tag were not found")


@csrf_protect
def login(request):
    popular_tags = Tag.objects.get_popular_tags()
    top_users = Profile.objects.get_top_users_of_week()

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

    return render(request, template_name='login.html', context={'form': login_form,
                                                                'popular_tags': popular_tags,
                                                                'top_users': top_users})


@csrf_protect
@login_required(login_url='login', redirect_field_name='continue')
def logout(request):
    auth_logout(request)
    return redirect(reverse('login'))


@csrf_protect
def signup(request):
    popular_tags = Tag.objects.get_popular_tags()
    top_users = Profile.objects.get_top_users_of_week()

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

    return render(request, template_name='signup.html', context={'form': user_form,
                                                                 'popular_tags': popular_tags,
                                                                 'top_users': top_users})


@csrf_protect
@login_required(login_url='login', redirect_field_name='continue')
def ask(request):
    popular_tags = Tag.objects.get_popular_tags()
    top_users = Profile.objects.get_top_users_of_week()

    if request.method == 'GET':
        form = AskQuestionForm()
    if request.method == 'POST':
        form = AskQuestionForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                question = form.save(user=request.user)
                return redirect('question', question_id=question.id)

    return render(request, template_name='ask.html', context={'form': form,
                                                              'popular_tags': popular_tags,
                                                              'top_users': top_users})


@csrf_protect
@login_required(login_url='login', redirect_field_name='continue')
def settings(request):
    popular_tags = Tag.objects.get_popular_tags()
    top_users = Profile.objects.get_top_users_of_week()

    if request.method == 'GET':
        settings_form = ProfileForm(initial=model_to_dict(request.user))
    if request.method == 'POST':
        settings_form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if settings_form.is_valid():
            settings_form.save()
            return redirect('settings')

    return render(request, template_name='settings.html', context={'form': settings_form,
                                                                   'popular_tags': popular_tags,
                                                                   'top_users': top_users})


@csrf_protect
@login_required(login_url='login', redirect_field_name='continue')
def like_question(request):
    id = request.POST.get('question_id')
    #q = Question.objects.filter(id=id).first()
    #if not q:
        #return JsonResponse({'status': 'fail'})
    question = get_object_or_404(Question, id=id)
    LikeQuestion.objects.toggle_like(user=request.user.profile, question=question, positive=True)
    count = Question.objects.rat(question_id=id)

    return JsonResponse({'count': count})


@csrf_protect
@login_required(login_url='login', redirect_field_name='continue')
def dislike_question(request):
    id = request.POST.get('question_id')
    question = get_object_or_404(Question, id=id)
    LikeQuestion.objects.toggle_like(user=request.user.profile, question=question, positive=False)
    count = Question.objects.rat(question_id=id)

    return JsonResponse({'count': count})


@csrf_protect
@login_required(login_url='login', redirect_field_name='continue')
def like_answer(request):
    id = request.POST.get('answer_id')
    answer = get_object_or_404(Answer, id=id)
    LikeAnswer.objects.toggle_like(user=request.user.profile, answer=answer, positive=True)
    count = Answer.objects.rat(question_id=id)

    return JsonResponse({'count': count})


@csrf_protect
@login_required(login_url='login', redirect_field_name='continue')
def dislike_answer(request):
    id = request.POST.get('answer_id')
    answer = get_object_or_404(Answer, id=id)
    LikeAnswer.objects.toggle_like(user=request.user.profile, answer=answer, positive=False)
    count = Answer.objects.rat(question_id=id)

    return JsonResponse({'count': count})


@csrf_protect
@login_required(login_url='login', redirect_field_name='continue')
def correct_answer(request):
    id = request.POST.get('answer_id')
    answer = get_object_or_404(Answer, id=id)
    Answer.objects.set_correct_answer(answer_id=id, user=request.user)
    text_correct = "No correct!" if answer.correct else "Correct!"

    return JsonResponse({'correct': text_correct})
