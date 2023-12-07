from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import User, Profile, Answer, Tag, Question
from django.db import transaction


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)
    password_check = forms.CharField(min_length=8, widget=forms.PasswordInput)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']

        if password and password_check and password != password_check:
            self.add_error('password', 'Passwords do not match')
            self.add_error('password_check', 'Passwords do not match')

    def save(self, **kwargs):
        avatar = self.files.get('avatar')
        self.cleaned_data.pop('password_check')
        self.cleaned_data.pop('avatar')

        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        avatar = self.files.get('avatar')
        print(avatar)

        try:
            user = User.objects.get(username=username, email=email)
            self.add_error('username', 'User with this username or email already exists.')
            self.add_error('email', 'User with this username or email already exists.')
            return None
        except User.DoesNotExist:
            user = User.objects.create_user(**self.cleaned_data)
            if avatar is not None:
                Profile.objects.create(user=user, avatar=avatar)
            return user


class AnswerForm(forms.Form):
    answer_text = forms.CharField(widget=forms.Textarea)

    def clean(self):
        answer_text = self.cleaned_data.get('answer_text')

        if not answer_text:
            self.add_error('answer_text', 'Answer text cannot be empty.')

    def save(self, question, author):
        answer_text = self.cleaned_data.get('answer_text')
        answer = Answer.objects.create(text=answer_text, question=question, author=author, correct=False)
        return answer


class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            self.add_error('username', 'This username is already taken.')
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            self.add_error('email', 'This email is already taken.')

        return cleaned_data

    def save(self, **kwargs):
        user = super().save(**kwargs)

        profile = user.profile
        received_avatar = self.cleaned_data.get('avatar')
        if received_avatar:
            profile.avatar = self.cleaned_data.get('avatar')
            profile.save()

        return user


class AskQuestionForm(forms.Form):
    title = forms.CharField(max_length=70)
    text = forms.CharField(widget=forms.Textarea, max_length=1000)
    tags = forms.CharField(max_length=50, required=False, widget=forms.Textarea(attrs={'rows': 3}))

    def clean_tags(self):
        tags_input = self.cleaned_data.get('tags', '')
        tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]

        if len(tags) > 5:
            raise forms.ValidationError("You can't enter more than 5 tags.")

        return tags

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        text = cleaned_data.get('text')
        tags = self.cleaned_data.get('tags', [])

        if not title:
            self.add_error('title', 'Title is required.')

        if not text:
            self.add_error('text', 'Text is required.')

        return cleaned_data

    def save(self, user):
        title = self.cleaned_data['title']
        text = self.cleaned_data['text']
        tags = self.cleaned_data['tags']

        with transaction.atomic():
            question = Question.objects.create(title=title, text=text, asker=user.profile)

            tag_objects = []
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                tag_objects.append(tag)

            question.tags.set(tag_objects)

            return question
