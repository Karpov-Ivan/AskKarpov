from django import forms
from .models import User
from .models import Profile, Answer


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
