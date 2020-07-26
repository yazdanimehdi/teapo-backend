from django.db import models


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

