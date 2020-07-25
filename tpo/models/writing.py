from django.db import models


def upload_location_writing(instance, filename):
    return f"tpo/writing/{instance.type}/{filename}"


class Writing(models.Model):
    related = models.CharField(max_length=200, blank=True, null=True)
    writing_listening = models.FileField(blank=True, null=True, upload_to=upload_location_writing)
    writing_image = models.FileField(blank=True, null=True, upload_to=upload_location_writing)
    writing_reading = models.TextField(blank=True, null=True)
    writing_question = models.TextField()
    type = models.CharField(max_length=30, default='Independent')
    writing_listening_transcript = models.TextField(blank=True, null=True)
    section = models.IntegerField(default=1)
    sections = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.related} {self.type}  {self.writing_question}"



