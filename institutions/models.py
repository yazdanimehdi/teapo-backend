from django.db import models
from django.contrib.auth.models import AbstractUser


def upload_location_class_files(instance, filename):
    return f"{instance.related_class.teacher_institute.institute}/{instance.related_class.category.name}/{instance.related_class.name}/{filename}"


class Users(AbstractUser):
    STUDENT = 1
    TEACHER = 2
    CORRECTOR = 3
    INSTITUTE = 4
    ADMIN = 5

    name = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=11)
    address = models.TextField(null=True, blank=True)
    institute = models.ForeignKey(to='institutions.Users', on_delete=models.SET_NULL, null=True, blank=True)
    ROLE_CHOICES = (
        (STUDENT, 'student'),
        (TEACHER, 'teacher'),
        (CORRECTOR, 'corrector'),
        (INSTITUTE, 'institute'),
        (ADMIN, 'admin'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=5)

    def __str__(self):
        return str(self.username)


class ClassCategory(models.Model):
    name = models.TextField()
    institute = models.ForeignKey(to=Users, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name + ' ------ ' + self.institute.name)


class Class(models.Model):
    name = models.TextField()
    category = models.ForeignKey(to=ClassCategory, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(to=Users, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.teacher} --------- {self.category} --------- {self.name}'


class ClassFiles(models.Model):
    file = models.FileField(upload_to=upload_location_class_files)
    related_class = models.ForeignKey(to=Class, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now=True, auto_created=True)
