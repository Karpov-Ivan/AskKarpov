from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer, Tag, LikeQuestion, LikeAnswer
import random


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

        self.stdout.write(self.style.SUCCESS(f'Creating...'))
        questions = Question.objects.all()
        for question in questions:
            positive_likes = LikeQuestion.objects.filter(question=question, positive=True).count()
            negative_likes = LikeQuestion.objects.filter(question=question, positive=False).count()

            question.rating = positive_likes - negative_likes
            question.save()

        self.stdout.write(self.style.SUCCESS(f'Creating...'))
        answers = Answer.objects.all()
        for answer in answers:
            positive_likes = LikeAnswer.objects.filter(answer=answer, positive=True).count()
            negative_likes = LikeAnswer.objects.filter(answer=answer, positive=False).count()

            answer.rating = positive_likes - negative_likes
            answer.save()

        self.stdout.write(self.style.SUCCESS('Database population completed.'))

    """
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
    """

    def create_users(self, ratio):
        users = [
            User(username=f'user{i}', email=f'user{i}@example.com', password=f'password{i}')
            for i in range(ratio)
        ]
        User.objects.bulk_create(users)

        profiles = [Profile(user=user) for user in users]
        Profile.objects.bulk_create(profiles)

    """
    def create_tags(self, ratio):
        for i in range(ratio):
            name = f'tag{i}'
            tag = Tag(name=name)
            tag.save()
    """

    def create_tags(self, ratio):
        tags = [
            Tag(name=f'tag{i}')
            for i in range(ratio)
        ]
        Tag.objects.bulk_create(tags)

    """
    def create_questions(self, ratio):
        tags = list(Tag.objects.all())
        for i in range(ratio * 10):
            title = f'Question {i}'
            text = f'Text of question {i}'
            asker = Profile.objects.get(id=random.randint(1, ratio))
            question = Question(title=title, text=text, asker=asker)
            question.save()
            selected_tags = random.sample(tags, 5)
            question.tags.set(selected_tags)
    """

    def create_questions(self, ratio):
        tags = list(Tag.objects.all())
        questions = [
            Question(
                title=f'Question {i}',
                text=f'Text of question {i}',
                asker=Profile.objects.get(id=random.randint(1, ratio))
            )
            for i in range(ratio * 10)
        ]
        Question.objects.bulk_create(questions)

        for question in questions:
            selected_tags = random.sample(tags, 5)
            question.tags.set(selected_tags)

    """
    def create_answers(self, ratio):
        for i in range(ratio * 100):
            question = Question.objects.get(id=random.randint(1, ratio * 10))
            author = Profile.objects.get(id=random.randint(1, ratio))
            text = f'Text of answer {i}'
            correct = random.choice([True, False])
            answer = Answer(text=text, correct=correct, question=question, author=author)
            answer.save()
    """

    def create_answers(self, ratio):
        answer_count = Answer.objects.count()
        questions = list(Question.objects.all())
        authors = list(Profile.objects.all())

        answers = [
            Answer(
                text=f'Text of answer {i}',
                correct=random.choice([True, False]),
                question=random.choice(questions),
                author=random.choice(authors)
            )
            for i in range(ratio * 100)
        ]
        Answer.objects.bulk_create(answers)

    """
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
    """

    def create_likes(self, ratio):
        answer_count = Answer.objects.count()
        users = list(Profile.objects.all())
        answers = list(Answer.objects.all())
        like_question_objects = []
        like_answer_objects = []

        for i in range(ratio * 200):
            positive = random.choice([True, False])
            user = random.choice(users)
            answer = random.choice(answers)

            like_question_objects.append(LikeQuestion(positive=positive, user=user, question=answer.question))
            like_answer_objects.append(LikeAnswer(positive=positive, user=user, answer=answer))

        LikeQuestion.objects.bulk_create(like_question_objects, ignore_conflicts=True)
        LikeAnswer.objects.bulk_create(like_answer_objects, ignore_conflicts=True)
