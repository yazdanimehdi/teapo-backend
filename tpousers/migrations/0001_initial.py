# Generated by Django 3.0.7 on 2020-07-24 02:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tpousers.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tpo', '0002_auto_20200724_0146'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_paid', models.BooleanField(default=False)),
                ('is_done', models.BooleanField(default=False)),
                ('test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tpo.Test')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserListeningAnswers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(blank=True, max_length=50, null=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tpo.ListeningQuestions')),
                ('user_test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tpousers.TestUser')),
            ],
        ),
        migrations.CreateModel(
            name='UserReadingAnswers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tpo.ReadingQuestions')),
                ('user_test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tpousers.TestUser')),
            ],
        ),
        migrations.CreateModel(
            name='UserStudyWords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('definition', models.TextField()),
                ('correct_times', models.IntegerField()),
                ('uncorrect_times', models.IntegerField()),
                ('word', models.TextField()),
                ('label', models.TextField()),
                ('state', models.IntegerField()),
                ('last_time', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserWritingCorrectionOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('writing_answer', models.FileField(blank=True, null=True, upload_to=tpousers.models.upload_location_user_order_files)),
                ('score', models.IntegerField()),
                ('comment', models.TextField(blank=True, null=True)),
                ('related_file', models.FileField(blank=True, null=True, upload_to=tpousers.models.upload_location_user_test_files)),
                ('is_paid', models.BooleanField(default=False)),
                ('is_done', models.BooleanField(default=False)),
                ('assigned_corrector', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='writing_corrector', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='writing_user', to=settings.AUTH_USER_MODEL)),
                ('writing', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tpo.Writing')),
            ],
        ),
        migrations.CreateModel(
            name='UserWritingAnswers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(blank=True, null=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tpo.Writing')),
                ('user_test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tpousers.TestUser')),
            ],
        ),
        migrations.CreateModel(
            name='UserStudyWordsExamples',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('example', models.TextField()),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tpousers.UserStudyWords')),
            ],
        ),
        migrations.CreateModel(
            name='UserSpeakingCorrectionOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('speaking_answer', models.FileField(blank=True, null=True, upload_to=tpousers.models.upload_location_user_order_files)),
                ('score', models.IntegerField()),
                ('comment', models.TextField(blank=True, null=True)),
                ('related_file', models.FileField(blank=True, null=True, upload_to=tpousers.models.upload_location_user_test_files)),
                ('is_paid', models.BooleanField(default=False)),
                ('is_done', models.BooleanField(default=False)),
                ('assigned_corrector', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='speaking_corrector', to=settings.AUTH_USER_MODEL)),
                ('speaking', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tpo.Speaking')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='speaking_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserSpeakingAnswers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.FileField(upload_to=tpousers.models.upload_location_user_test_files)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tpo.Speaking')),
                ('user_test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tpousers.TestUser')),
            ],
        ),
        migrations.CreateModel(
            name='UserReadingAnswersAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tpo.ReadingAnswers')),
                ('reading_answer_inst', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tpousers.UserReadingAnswers')),
            ],
        ),
        migrations.CreateModel(
            name='UserListeningAnswersAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tpo.ListeningAnswers')),
                ('listening_answer_inst', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tpousers.UserListeningAnswers')),
            ],
        ),
        migrations.CreateModel(
            name='TestUserWriting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('comment', models.TextField(blank=True, null=True)),
                ('related_file', models.FileField(blank=True, null=True, upload_to=tpousers.models.upload_location_user_test_files)),
                ('assigned_corrector', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('test_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tpousers.TestUser')),
            ],
        ),
        migrations.CreateModel(
            name='TestUserSpeaking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('comment', models.TextField(blank=True, null=True)),
                ('related_file', models.FileField(blank=True, null=True, upload_to=tpousers.models.upload_location_user_test_files)),
                ('assigned_corrector', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('test_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tpousers.TestUser')),
            ],
        ),
        migrations.CreateModel(
            name='TestUserReading',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('comment', models.TextField(blank=True, null=True)),
                ('related_file', models.FileField(blank=True, null=True, upload_to=tpousers.models.upload_location_user_test_files)),
                ('assigned_corrector', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('test_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tpousers.TestUser')),
            ],
        ),
        migrations.CreateModel(
            name='TestUserListening',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('comment', models.TextField(blank=True, null=True)),
                ('related_file', models.FileField(blank=True, null=True, upload_to=tpousers.models.upload_location_user_test_files)),
                ('assigned_corrector', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('test_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tpousers.TestUser')),
            ],
        ),
    ]
