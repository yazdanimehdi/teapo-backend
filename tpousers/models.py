from django.db import models
from django.contrib.auth.models import AbstractUser


def upload_location_user_test_files(instance, filename):
    return f"{instance.test_user.user.username}/{instance.test_user.test.title}/{filename}"


def upload_location_user_order_files(instance, filename):
    return f"{instance.user.username}/{instance.speaking.related}/{filename}"


class UserStudyWords(models.Model):
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


class UserStudyWordsExamples(models.Model):
    word = models.ForeignKey(to=UserStudyWords, on_delete=models.CASCADE)
    example = models.TextField()

    def __str__(self):
        return str(self.word.word + '-----' + self.example)


class TestUser(models.Model):
    test = models.ForeignKey(to='tpo.Test', on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(to='institutions.Users', on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)


class TestUserReading(models.Model):
    test_user = models.ForeignKey(to=TestUser, on_delete=models.CASCADE)
    score = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    related_file = models.FileField(upload_to=upload_location_user_test_files, null=True, blank=True)
    assigned_corrector = models.ForeignKey(to='institutions.Users', on_delete=models.SET_NULL, null=True)


class TestUserListening(models.Model):
    test_user = models.ForeignKey(to=TestUser, on_delete=models.CASCADE)
    score = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    related_file = models.FileField(upload_to=upload_location_user_test_files, null=True, blank=True)
    assigned_corrector = models.ForeignKey(to='institutions.Users', on_delete=models.SET_NULL, null=True)


class TestUserSpeaking(models.Model):
    test_user = models.ForeignKey(to=TestUser, on_delete=models.CASCADE)
    score = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    related_file = models.FileField(upload_to=upload_location_user_test_files, null=True, blank=True)
    assigned_corrector = models.ForeignKey(to='institutions.Users', on_delete=models.SET_NULL, null=True)


class TestUserWriting(models.Model):
    test_user = models.ForeignKey(to=TestUser, on_delete=models.CASCADE)
    score = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    related_file = models.FileField(upload_to=upload_location_user_test_files, null=True, blank=True)
    assigned_corrector = models.ForeignKey(to='institutions.Users', on_delete=models.SET_NULL, null=True)


class UserSpeakingCorrectionOrder(models.Model):
    user = models.ForeignKey(to='institutions.Users', on_delete=models.CASCADE, related_name='speaking_user')
    speaking = models.ForeignKey(to='tpo.speaking', on_delete=models.SET_NULL, null=True)
    assigned_corrector = models.ForeignKey(to='institutions.Users', on_delete=models.SET_NULL, null=True,
                                           related_name='speaking_corrector')

    speaking_answer = models.FileField(upload_to=upload_location_user_order_files, null=True, blank=True)
    score = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    related_file = models.FileField(upload_to=upload_location_user_test_files, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)


class UserWritingCorrectionOrder(models.Model):
    user = models.ForeignKey(to='institutions.Users', on_delete=models.CASCADE, related_name='writing_user')
    writing = models.ForeignKey(to='tpo.writing', on_delete=models.SET_NULL, null=True)
    writing_answer = models.FileField(upload_to=upload_location_user_order_files, null=True, blank=True)
    assigned_corrector = models.ForeignKey(to='institutions.Users', on_delete=models.SET_NULL, null=True,
                                           related_name='writing_corrector')
    score = models.IntegerField()
    comment = models.TextField(null=True, blank=True)
    related_file = models.FileField(upload_to=upload_location_user_test_files, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)


class UserReadingAnswers(models.Model):
    user_test = models.ForeignKey(to=TestUser, on_delete=models.CASCADE)
    question = models.ForeignKey(to='tpo.ReadingQuestions', on_delete=models.CASCADE)


class UserReadingAnswersAnswer(models.Model):
    reading_answer_inst = models.ForeignKey(to=UserReadingAnswers, on_delete=models.CASCADE)
    answer = models.ForeignKey(to='tpo.ReadingAnswers', on_delete=models.CASCADE)


class UserListeningAnswers(models.Model):
    user_test = models.ForeignKey(to=TestUser, on_delete=models.CASCADE)
    question = models.ForeignKey(to='tpo.ListeningQuestions', on_delete=models.CASCADE)
    answer = models.CharField(max_length=50, blank=True, null=True)


class UserListeningAnswersAnswer(models.Model):
    listening_answer_inst = models.ForeignKey(to=UserListeningAnswers, on_delete=models.CASCADE)
    answer = models.ForeignKey(to='tpo.ListeningAnswers', on_delete=models.CASCADE)


class UserSpeakingAnswers(models.Model):
    user_test = models.ForeignKey(to=TestUser, on_delete=models.CASCADE)
    question = models.ForeignKey(to='tpo.Speaking', on_delete=models.CASCADE)
    answer = models.FileField(upload_to=upload_location_user_test_files)


class UserWritingAnswers(models.Model):
    user_test = models.ForeignKey(to=TestUser, on_delete=models.CASCADE)
    question = models.ForeignKey(to='tpo.Writing', on_delete=models.CASCADE)
    answer = models.TextField(blank=True, null=True)
