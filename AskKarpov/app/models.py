from django.db import models
from django.contrib.auth.models import User


class QuestionManager(models.Manager):
    def new(self):
        questions = self.calculated_rating()
        return questions.order_by('-rating', '-date')

    def tag(self, tag_name):
        questions = self.calculated_rating()
        return questions.filter(tags__name=tag_name).order_by('-rating')

    def best(self):
        questions = self.calculated_rating()
        return questions.order_by('-rating')

    def calculated_rating(self):
        questions = self.all()

        for question in questions:
            positive_likes = LikeQuestion.objects.filter(question=question, positive=True).count()
            negative_likes = LikeQuestion.objects.filter(question=question, positive=False).count()

            question.rating = positive_likes - negative_likes
            # question.save()

        return questions


class AnswerManager(models.Manager):
    def new(self):
        answers = self.calculated_rating()
        return answers.order_by('-rating', '-date')

    def calculated_rating(self):
        answers = self.all()

        for answer in answers:
            positive_likes = LikeAnswer.objects.filter(answer=answer, positive=True).count()
            negative_likes = LikeAnswer.objects.filter(answer=answer, positive=False).count()

            answer.rating = positive_likes - negative_likes
            #answer.save()

        return answers


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(blank=True, upload_to="avatars/")

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

    def __str__(self):
        return f"{self.name}"


class LikeQuestion(models.Model):
    positive = models.BooleanField()  # unique
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)

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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "answer"],
                name="unique_like_answer",
            ),
        ]

    def __str__(self):
        return f"Who = {self.user.id}, what = {self.answer.id}"
