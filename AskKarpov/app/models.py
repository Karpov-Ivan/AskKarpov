from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.utils import timezone


class QuestionManager(models.Manager):
    def new(self):
        return self.all().order_by('-rating', '-date')

    def tag(self, tag_name):
        return self.filter(tags__name=tag_name).order_by('-rating')

    def best(self):
        return self.all().order_by('-rating')

    def rat(self, question_id):
        question = self.get(id=question_id)

        positive_likes = LikeQuestion.objects.filter(question=question, positive=True).count()
        negative_likes = LikeQuestion.objects.filter(question=question, positive=False).count()

        question.rating = positive_likes - negative_likes
        question.save()

        return positive_likes - negative_likes


class AnswerManager(models.Manager):
    def new(self):
        return self.order_by('-rating', '-date')

    def rat(self, question_id):
        answer = self.get(id=question_id)

        positive_likes = LikeAnswer.objects.filter(answer=answer, positive=True).count()
        negative_likes = LikeAnswer.objects.filter(answer=answer, positive=False).count()

        answer.rating = positive_likes - negative_likes
        answer.save()

        return positive_likes - negative_likes

    def set_correct_answer(self, answer_id, user):
        answer = self.get(id=answer_id)

        if user == answer.question.asker.user:
            answer.correct = not answer.correct
            answer.save()


class QuestionLikeManager(models.Manager):
    def toggle_like(self, user, question, positive):
        if self.filter(user=user, question=question, positive=positive).exists():
            self.filter(user=user, question=question, positive=positive).delete()
        else:
            self.create(user=user, question=question, positive=positive)


class AnswerLikeManager(models.Manager):
    def toggle_like(self, user, answer, positive):
        if self.filter(user=user, answer=answer, positive=positive).exists():
            self.filter(user=user, answer=answer, positive=positive).delete()
        else:
            self.create(user=user, answer=answer, positive=positive)


class TagManager(models.Manager):
    def get_popular_tags(self, count=10):
        popular_tags = (
            self.filter(question__isnull=False)
                .values('id', 'name')
                .annotate(question_count=Count('question'))
                .order_by('-question_count')[:count]
        )

        return popular_tags


class ProfileManager(models.Manager):
    def get_top_users_of_week(self, count=10):
        now = timezone.now()
        start_date = now - timezone.timedelta(days=7)

        top_users = (
            self.filter(answer__date__gte=start_date)
                .annotate(total_rating=Sum('answer__rating'))
                .values('user__id', 'user__username', 'avatar')
                .annotate(total_questions=Count('question'))
                .order_by('-total_rating')[:count]
        )

        return top_users


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(blank=True, upload_to="avatars/")

    objects = ProfileManager()

    def __str__(self):
        return f"id = {self.id}, {self.user.get_username()}"


class Question(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    statusChangeDate = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField(auto_now_add=True)
    asker = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name="questions",
                              related_query_name="question")
    tags = models.ManyToManyField('Tag', related_name="questions", related_query_name="question")
    likes = models.ManyToManyField('Profile', through="LikeQuestion", related_name="question_likes",
                                   related_query_name="question_like")

    objects = QuestionManager()

    def __str__(self):
        return f"id = {self.id}, {self.title}"


class Answer(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    correct = models.BooleanField()
    rating = models.IntegerField(default=0)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name="answers",
                                 related_query_name="answer")
    author = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name="answers",
                               related_query_name="answer")
    likes = models.ManyToManyField('Profile', through="LikeAnswer", related_name="answer_likes",
                                   related_query_name="answer_like")

    objects = AnswerManager()

    def __str__(self):
        return f"id = {self.id}, {self.text[0:5]}"


class Tag(models.Model):
    name = models.CharField(max_length=50)

    objects = TagManager()

    def __str__(self):
        return f"{self.name}"


class LikeQuestion(models.Model):
    positive = models.BooleanField()  # unique
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)

    objects = QuestionLikeManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "question"],
                name="unique_like_question",
            ),
        ]

    def __str__(self):
        return f"Who = {self.user.id}, what = {self.question.id}"


class LikeAnswer(models.Model):  # unique
    positive = models.BooleanField()
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)

    objects = AnswerLikeManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "answer"],
                name="unique_like_answer",
            ),
        ]

    def __str__(self):
        return f"Who = {self.user.id}, what = {self.answer.id}"
