from django.db import models
from django.utils.translation import gettext_lazy as _


class Test(models.Model):
    class ModeChoices(models.TextChoices):
        TPO = 'T', _('TPO')
        MOCK = 'M', _('Mock')
        ASSIGNMENT = 'A', _('Assignment')
        PRACTICE = 'P', _('Practice')

    title = models.CharField(max_length=30)
    code = models.CharField(max_length=10)
    institute = models.ForeignKey(to='institutions.Users', on_delete=models.CASCADE, blank=True, null=True)
    mode = models.CharField(max_length=1, choices=ModeChoices.choices, default=ModeChoices.TPO)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    class_assigned = models.ForeignKey(to='institutions.Class', on_delete=models.CASCADE, blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    reading_time = models.IntegerField(blank=True, null=True)
    is_paid = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class SpeakingTimes(models.Model):
    test = models.ForeignKey(to='tpo.Test', on_delete=models.CASCADE)
    number = models.IntegerField()
    preparation_time = models.IntegerField()
    answering_time = models.IntegerField()
    reading_time = models.IntegerField(blank=True, null=True)


class WritingTimes(models.Model):
    test = models.ForeignKey(to='tpo.Test', on_delete=models.CASCADE)
    number = models.IntegerField()
    time = models.IntegerField()


class ListeningTimes(models.Model):
    test = models.ForeignKey(to='tpo.Test', on_delete=models.CASCADE)
    number = models.IntegerField()
    time = models.IntegerField()


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
