from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


class QuestionManager(models.Manager):
    def new(self):
        return self.order_by('-like__count', '-created_at')

    def tag(self, tag_name):
        return self.filter(tags__name=tag_name).order_by('-like__count')

    def best(self):
        return self.order_by('-like__count')

class AnswerManager(models.Manager):
    def new(self):
        return self.order_by('-like__count', '-created_at')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick_name = models.CharField(max_length=15)
    avatar = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.nick_name}"


class Question(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    like = models.ForeignKey('Like', null=True, blank=True, on_delete=models.CASCADE, related_name='question_likes')
    tags = models.ManyToManyField('Tag', related_name='questions', blank=True)

    objects = QuestionManager()

    def __str__(self):
        return f"{self.title}"


class Answer(models.Model):
    text = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    like = models.ForeignKey('Like', null=True, blank=True, on_delete=models.CASCADE, related_name='answer_likes')
    correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    objects = AnswerManager()

    def __str__(self):
        return f"{self.text}"


class Tag(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name}"


class Like(models.Model):
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.count}"