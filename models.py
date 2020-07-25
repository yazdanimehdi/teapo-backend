from django.db import models
from django.contrib.auth.models import AbstractUser


class Listening(models.Model):
    listening = models.TextField()
    phase = models.IntegerField(blank=True, null=True)
    listening_image = models.TextField()
    title = models.CharField(max_length=300, blank=True, null=True)
    related = models.CharField(max_length=500, blank=True, null=True)
    type = models.CharField(max_length=30, default='Conversation')
    transcript = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{str(self.related)} {self.type} {self.title}"


class ListeningQuestions(models.Model):
    listening = models.ForeignKey(to='tpo.Listening', on_delete=models.CASCADE)
    question = models.TextField()
    listening_question_audio_file = models.TextField()
    number = models.IntegerField()
    quote = models.BooleanField(default=False)
    quote_audio_file = models.TextField()
    right_answer = models.CharField(max_length=50)


class ListeningAnswers(models.Model):
    question = models.ForeignKey(to='tpo.ListeningQuestions', on_delete=models.CASCADE)
    answer = models.TextField()
    code = models.CharField(max_length=1)


class Reading(models.Model):
    related = models.CharField(max_length=200, default='')
    phase = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=200, default=' ')
    passage = models.TextField()

    def __str__(self):
        return f"{self.related}  {self.title}"


class ReadingQuestions(models.Model):
    reading = models.ForeignKey(to='tpo.Reading', on_delete=models.CASCADE)
    question = models.TextField()
    insertion_sentence = models.TextField(null=True, blank=True)
    number = models.IntegerField()
    related_paragraph = models.IntegerField(null=True, blank=True)
    related_passage = models.TextField(null=True, blank=True)
    related_passage_title = models.CharField(null=True, blank=True, max_length=400)
    question_type = models.CharField(max_length=10)
    right_answer = models.CharField(max_length=50)


class ReadingAnswers(models.Model):
    question = models.ForeignKey(to='tpo.ReadingQuestions', on_delete=models.CASCADE)
    answer = models.TextField()
    code = models.CharField(max_length=1)


class ReadingWords(models.Model):
    related_reading = models.ForeignKey(to='tpo.Reading', on_delete=models.CASCADE)
    word = models.CharField(max_length=400)
    translate = models.CharField(max_length=400, null=True, blank=True)


class CustomUser(AbstractUser):
    phone = models.IntegerField(max_length=11)
    token = models.CharField(max_length=200)
    gender = models.BinaryField(default=0)


class UserTest(models.Model):
    user = models.ForeignKey(to='tpo.CustomUser', on_delete=models.CASCADE)
    test = models.ForeignKey(to='tpo.Test', on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_done = models.BooleanField(default=False)
    section = models.CharField(max_length=200, null=True, blank=True)
    task_number = models.IntegerField(null=True, blank=True)
    question_number = models.IntegerField(null=True, blank=True)
    total_time = models.IntegerField(null=True, blank=True)
    voucher_used = models.CharField(default=0, max_length=30)
    reading_score = models.IntegerField(blank=True, null=True)
    reading_feedback = models.TextField(blank=True, null=True)
    listening_score = models.IntegerField(blank=True, null=True)
    listening_feedback = models.TextField(blank=True, null=True)
    speaking_score = models.IntegerField(blank=True, null=True)
    speaking_feedback = models.TextField(blank=True, null=True)
    writing_score = models.IntegerField(blank=True, null=True)
    writing_feedback = models.TextField(blank=True, null=True)
    writing_feedback_file = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.test)


class UserReadingAnswers(models.Model):
    user_test = models.ForeignKey(to='tpo.UserTest', on_delete=models.CASCADE)
    question = models.ForeignKey(to='tpo.ReadingQuestions', on_delete=models.CASCADE)
    answer = models.CharField(max_length=50, blank=True, null=True)


class UserListeningAnswers(models.Model):
    user_test = models.ForeignKey(to='tpo.UserTest', on_delete=models.CASCADE)
    question = models.ForeignKey(to='tpo.ListeningQuestions', on_delete=models.CASCADE)
    answer = models.CharField(max_length=50, blank=True, null=True)


class UserSpeakingAnswers(models.Model):
    user_test = models.ForeignKey(to='tpo.UserTest', on_delete=models.CASCADE)
    question = models.ForeignKey(to='tpo.Speaking', on_delete=models.CASCADE)
    answer = models.TextField()


class UserWritingAnswers(models.Model):
    user_test = models.ForeignKey(to='tpo.UserTest', on_delete=models.CASCADE)
    question = models.ForeignKey(to='tpo.Writing', on_delete=models.CASCADE)
    answer = models.TextField(blank=True, null=True)


class Speaking(models.Model):
    related = models.CharField(max_length=200, blank=True, null=True)
    speaking_audio_file = models.TextField()
    speaking_reading_title = models.CharField(blank=True, null=True, max_length=400)
    speaking_reading = models.TextField(blank=True, null=True)
    speaking_image = models.TextField()
    speaking_question = models.TextField()
    speaking_reading_time = models.IntegerField(default=45)
    speaking_time = models.IntegerField(default=60)
    speaking_prepare_time = models.IntegerField(default=30)
    speaking_question_audio_file = models.TextField()
    speaking_audio_file_transcript = models.TextField(blank=True, null=True)
    speaking_question_guide_audio_file = models.TextField()
    speaking_question_before_read_audio = models.TextField()
    number = models.IntegerField()
    sections = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.related} {self.number} {self.speaking_question}"


class Test(models.Model):
    title = models.CharField(max_length=30)
    code = models.CharField(max_length=10)
    listening_time = models.IntegerField(blank=True, null=True)
    reading_time = models.IntegerField(blank=True, null=True)
    writing_independent_time = models.IntegerField(blank=True, null=True)
    writing_integrated_time = models.IntegerField(blank=True, null=True)
    writing_reading_time = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title


class TestSpeaking(models.Model):
    test = models.ForeignKey(to='tpo.Test', on_delete=models.CASCADE)
    speaking = models.ForeignKey(to='tpo.Speaking', on_delete=models.CASCADE)


class TestListening(models.Model):
    test = models.ForeignKey(to='tpo.Test', on_delete=models.CASCADE)
    listening = models.ForeignKey(to='tpo.Listening', on_delete=models.CASCADE)
    part = models.IntegerField(default=0)


class TestReading(models.Model):
    test = models.ForeignKey(to='tpo.Test', on_delete=models.CASCADE)
    reading = models.ForeignKey(to='tpo.Reading', on_delete=models.CASCADE)
    part = models.IntegerField(default=0)


class TestWriting(models.Model):
    test = models.ForeignKey(to='tpo.Test', on_delete=models.CASCADE)
    writing = models.ForeignKey(to='tpo.Writing', on_delete=models.CASCADE)


class Writing(models.Model):
    related = models.CharField(max_length=200, blank=True, null=True)
    writing_listening = models.TextField()
    writing_image = models.TextField()
    writing_reading = models.TextField(blank=True, null=True)
    writing_listening_transcript = models.TextField(blank=True, null=True)
    writing_question = models.TextField()
    type = models.CharField(max_length=30, default='Independent')
    section = models.IntegerField(default=1)
    sections = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.related} {self.type}  {self.writing_question}"

