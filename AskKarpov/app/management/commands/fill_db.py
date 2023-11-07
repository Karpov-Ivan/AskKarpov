from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer, Tag, LikeQuestion, LikeAnswer
import random
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = 'Fill the database with users, questions, answers, tags, and user ratings.'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Coefficient for data population')

    def handle(self, *args, **options):
        ratio = options['ratio']

        self.stdout.write(self.style.SUCCESS(f'Creating {ratio} users...'))
        self.create_users(ratio)

        self.stdout.write(self.style.SUCCESS(f'Creating {ratio} tags...'))
        self.create_tags(ratio)

        self.stdout.write(self.style.SUCCESS(f'Creating {ratio * 10} questions...'))
        self.create_questions(ratio)

        self.stdout.write(self.style.SUCCESS(f'Creating {ratio * 100} answers...'))
        self.create_answers(ratio)

        self.stdout.write(self.style.SUCCESS(f'Creating {ratio * 200} likes...'))
        self.create_likes(ratio)

        self.stdout.write(self.style.SUCCESS('Database population completed.'))

    def create_users(self, ratio):
        for i in range(ratio):
            username = f'user{i}'
            email = f'user{i}@example.com'
            password = f'password{i}'
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()
            profile = Profile(user=user)
            profile.save()

    def create_tags(self, ratio):
        for i in range(ratio):
            name = f'tag{i}'
            tag = Tag(name=name)
            tag.save()

    def create_questions(self, ratio):
        tags = list(Tag.objects.all())
        for i in range(ratio * 10):
            title = f'Question {i}'
            text = f'Text of question {i}'
            asker = Profile.objects.get(id=random.randint(1, ratio))
            question = Question(title=title, text=text, asker=asker)
            question.save()
            question.tags.set(random.sample(tags, ratio))

    def create_answers(self, ratio):
        for i in range(ratio * 10):
            question = Question.objects.get(id=random.randint(1, ratio * 10))
            author = Profile.objects.get(id=random.randint(1, ratio))
            text = f'Text of answer {i}'
            correct = random.choice([True, False])
            answer = Answer(text=text, correct=correct, question=question, author=author)
            answer.save()

    def create_likes(self, ratio):
        answer_count = Answer.objects.count()

        for i in range(ratio * 200):
            positive = random.choice([True, False])
            user = Profile.objects.get(id=random.randint(1, ratio))

            answer_id = random.randint(1, answer_count)
            answer = Answer.objects.get(id=answer_id)

            try:
                like_question = LikeQuestion.objects.get(user=user, question=answer.question)
                like_question.positive = positive
                like_question.save()
            except LikeQuestion.DoesNotExist:
                like_question = LikeQuestion(positive=positive, user=user, question=answer.question)
                like_question.save()

            try:
                like_answer = LikeAnswer.objects.get(user=user, answer=answer)
                like_answer.positive = positive
                like_answer.save()
            except LikeAnswer.DoesNotExist:
                like_answer = LikeAnswer(positive=positive, user=user, answer=answer)
                like_answer.save()
