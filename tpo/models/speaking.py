from django.db import models


def upload_location_speaking(instance, filename):
    return f"tpo/speaking/{instance.number}/{filename}"


class Speaking(models.Model):
    related = models.CharField(max_length=200, blank=True, null=True)
    speaking_audio_file = models.FileField(blank=True, null=True, upload_to=upload_location_speaking)
    speaking_reading_title = models.CharField(blank=True, null=True, max_length=400)
    speaking_reading = models.TextField(blank=True, null=True)
    speaking_image = models.FileField(blank=True, null=True, upload_to=upload_location_speaking)
    speaking_question = models.TextField()
    speaking_question_audio_file = models.FileField(blank=True, null=True, upload_to=upload_location_speaking)
    speaking_question_guide_audio_file = models.FileField(blank=True, null=True, upload_to=upload_location_speaking)
    speaking_question_before_read_audio = models.FileField(blank=True, null=True, upload_to=upload_location_speaking)
    number = models.IntegerField()
    speaking_audio_file_transcript = models.TextField(blank=True, null=True)
    sections = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.related} {self.number} {self.speaking_question}"

