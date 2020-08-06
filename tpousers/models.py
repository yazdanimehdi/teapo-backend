from django.db import models
from django.contrib.auth.models import AbstractUser


def upload_location_user_test_files(instance, filename):
    return f"{instance.test_user.user.username}/{instance.test_user.test.title}/{filename}"


def upload_location_user_order_files(instance, filename):
    return f"{instance.user.username}/{instance.speaking.related}/{filename}"


class StudyWords(models.Model):
    user = models.ForeignKey(to='institutions.Users', on_delete=models.CASCADE)
    definition = models.TextField()
    correct_times = models.IntegerField()
    uncorrect_times = models.IntegerField()
    word = models.TextField()
    label = models.TextField()
    state = models.IntegerField()
    last_time = models.DateTimeField()

    def __str__(self):
        return str(self.word)


class StudyWordsExamples(models.Model):
    word = models.ForeignKey(to=StudyWords, on_delete=models.CASCADE)
    example = models.TextField()

    def __str__(self):
        return str(self.word.word + '-----' + self.example)


class TestUser(models.Model):
    test = models.ForeignKey(to='tpo.Test', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(to='institutions.Users', on_delete=models.CASCADE)
    date_time = models.DateTimeField(null=True, blank=True)
    reading_score = models.IntegerField(null=True, blank=True)
    listening_score = models.IntegerField(null=True, blank=True)
    speaking_score = models.IntegerField(null=True, blank=True)
    writing_score = models.IntegerField(null=True, blank=True)
    is_paid = models.BooleanField(null=True, blank=True)
    is_done = models.BooleanField(default=False)
    exam_section = models.CharField(null=True, blank=True, max_length=10)
    task_number = models.IntegerField(null=True, blank=True)
    state_number = models.IntegerField(null=True, blank=True)
    remaining_time = models.IntegerField(null=True, blank=True)


class UserReadingAnswers(models.Model):
    user_test = models.ForeignKey(to=TestUser, on_delete=models.CASCADE)
    question = models.ForeignKey(to='tpo.ReadingQuestions', on_delete=models.CASCADE)
    answer = models.CharField(max_length=50, blank=True, null=True)


class UserListeningAnswers(models.Model):
    user_test = models.ForeignKey(to=TestUser, on_delete=models.CASCADE)
    question = models.ForeignKey(to='tpo.ListeningQuestions', on_delete=models.CASCADE)
    answer = models.CharField(max_length=50, blank=True, null=True)


class UserSpeakingAnswers(models.Model):
    user_test = models.ForeignKey(to=TestUser, on_delete=models.CASCADE)
    question = models.ForeignKey(to='tpo.Speaking', on_delete=models.CASCADE)
    answer = models.FileField(upload_to=upload_location_user_test_files)


class UserWritingAnswers(models.Model):
    user_test = models.ForeignKey(to=TestUser, on_delete=models.CASCADE)
    question = models.ForeignKey(to='tpo.Writing', on_delete=models.CASCADE)
    answer = models.TextField(blank=True, null=True)


class UserSpeakingCorrectionOrder(models.Model):
    user = models.ForeignKey(to='institutions.Users', on_delete=models.CASCADE, related_name='speaking_user')
    assigned_corrector = models.ForeignKey(to='institutions.Users', on_delete=models.SET_NULL, null=True, blank=True,
                                           related_name='speaking_corrector')

    speaking_answers = models.ManyToManyField(UserSpeakingAnswers)
    score = models.IntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    related_file = models.FileField(upload_to=upload_location_user_test_files, null=True, blank=True)
    state = models.IntegerField(default=0)
    is_paid = models.BooleanField(default=False)


class UserWritingCorrectionOrder(models.Model):
    user = models.ForeignKey(to='institutions.Users', on_delete=models.CASCADE, related_name='writing_user')
    writing_answer = models.ManyToManyField(UserWritingAnswers)
    assigned_corrector = models.ForeignKey(to='institutions.Users', on_delete=models.SET_NULL, null=True,
                                           related_name='writing_corrector')
    score = models.IntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    related_file = models.FileField(upload_to=upload_location_user_test_files, null=True, blank=True)
    state = models.IntegerField(default=0)
    is_paid = models.BooleanField(default=False)


class UserTestOwnership(models.Model):
    test = models.ForeignKey(to='tpo.Test', on_delete=models.CASCADE)
    user = models.ForeignKey(to='institutions.Users', on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)


class UserTestOwnershipPendingPayment(models.Model):
    ownership = models.ForeignKey(to=UserTestOwnership, on_delete=models.CASCADE)
    token = models.CharField(max_length=20)
    fee = models.FloatField()


class SpeakingOrderPendingPayment(models.Model):
    order = models.ForeignKey(to=UserSpeakingCorrectionOrder, on_delete=models.CASCADE)
    token = models.CharField(max_length=20)
    fee = models.FloatField()


class WritingOrderPendingPayment(models.Model):
    order = models.ForeignKey(to=UserWritingCorrectionOrder, on_delete=models.CASCADE)
    token = models.CharField(max_length=20)
    fee = models.FloatField()


class GlobalVariables(models.Model):
    key = models.CharField(max_length=100)
    value = models.TextField()
