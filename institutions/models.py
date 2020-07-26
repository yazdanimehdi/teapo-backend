from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


def upload_location_class_files(instance, filename):
    return f"{instance.related_class.teacher_institute.institute}/{instance.related_class.category.name}/{instance.related_class.name}/{filename}"


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Users(AbstractUser):
    objects = UserManager()
    STUDENT = 1
    TEACHER = 2
    CORRECTOR = 3
    INSTITUTE = 4
    ADMIN = 5

    username = None
    USERNAME_FIELD = 'email'
    email = models.EmailField(_('email address'), unique=True)
    REQUIRED_FIELDS = []
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
        return str(self.email)


class ClassCategory(models.Model):
    name = models.TextField()
    institute = models.ForeignKey(to=Users, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name + ' ------ ' + self.institute.name)


class Class(models.Model):
    name = models.TextField()
    students = models.ManyToManyField(Users, related_name='students')
    category = models.ForeignKey(to=ClassCategory, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(to=Users, on_delete=models.SET_NULL, null=True, blank=True, related_name='teacher')

    def __str__(self):
        return f'{self.teacher} --------- {self.category} --------- {self.name}'


class ClassFiles(models.Model):
    file = models.FileField(upload_to=upload_location_class_files)
    related_class = models.ForeignKey(to=Class, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now=True, auto_created=True)
