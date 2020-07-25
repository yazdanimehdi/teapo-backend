from django.db import models


def upload_location_listening(instance, filename):
    return f"tpo/listening/{instance.type}/{instance.title}/{filename}"


def upload_location_listening_questions(instance, filename):
    return f"tpo/listening/{instance.listening.type}/{instance.listening.title}/questions/{filename}"


class Listening(models.Model):
    listening = models.FileField(upload_to=upload_location_listening)
    listening_image = models.FileField(upload_to=upload_location_listening)
    title = models.CharField(max_length=300, blank=True, null=True)
    type = models.CharField(max_length=30, default='Conversation')
    phase = models.IntegerField(blank=True, null=True)
    related = models.CharField(max_length=500, blank=True, null=True)
    transcript = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{str(self.related)} {self.type} {self.title}"


class ListeningQuestions(models.Model):
    listening = models.ForeignKey(to='tpo.Listening', on_delete=models.CASCADE)
    question = models.TextField()
    listening_question_audio_file = models.FileField(upload_to=upload_location_listening_questions)
    number = models.IntegerField()
    quote = models.BooleanField(default=False)
    quote_audio_file = models.FileField(upload_to=upload_location_listening_questions, null=True, blank=True)


class ListeningAnswers(models.Model):
    question = models.ForeignKey(to='tpo.ListeningQuestions', on_delete=models.CASCADE)
    answer = models.TextField()
    code = models.CharField(max_length=1)
    is_correct = models.BooleanField(default=False)
