from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer, Tag, Like
import random


class Command(BaseCommand):
    help = 'Fill the database with users, questions, answers, tags, and likes'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Specify the ratio for data creation')

    def handle(self, *args, **options):
        ratio = options['ratio']

        """
        self.stdout.write(self.style.SUCCESS(f'Creating {ratio} users...'))
        self.create_users(ratio)

        self.stdout.write(self.style.SUCCESS(f'Creating {ratio} tags...'))
        self.create_tags(ratio)

        self.stdout.write(self.style.SUCCESS(f'Creating {ratio * 200} likes...'))
        self.create_likes(ratio)
        """

        self.stdout.write(self.style.SUCCESS(f'Creating {ratio * 10} questions...'))
        self.create_questions(ratio)

        self.stdout.write(self.style.SUCCESS(f'Creating {ratio * 100} answers...'))
        self.create_answers(ratio)

    def create_users(self, ratio):
        for i in range(ratio):
            user = User.objects.create_user(username=f'user{i}', password=f'password{i}')
            profile = Profile.objects.create(user=user, nick_name=f'Nickname{i}', avatar=None)

    def create_likes(self, ratio):
        for i in range(ratio * 200):
            Like.objects.create(count=random.randint(1, 1000))

    def create_tags(self, ratio):
        for i in range(ratio):
            Tag.objects.create(name=f'Tag {i}')

    def create_questions(self, ratio):
        for i in range(63340, ratio * 10):
            user = User.objects.get(username=f'user{i % ratio}')
            tags = Tag.objects.order_by('?')[:random.randint(1, 5)]
            question = Question.objects.create(
                title=f'Question {i}',
                text=f'Question text {i}',
                profile=user.profile,
            )
            question.tags.set(tags)
            like = Like.objects.order_by('?').first()
            question.like = like
            question.save()

    def create_answers(self, ratio):
        for i in range(ratio * 100):
            user = User.objects.get(username=f'user{i % ratio}')
            question = Question.objects.get(title=f'Question {i % (ratio * 10)}')
            like = Like.objects.order_by('?').first()
            answer = Answer.objects.create(
                text=f'Answer {i}',
                profile=user.profile,
                question=question,
            )
            answer.like = like
            answer.save()
