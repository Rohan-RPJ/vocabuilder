# Generated by Django 2.0.13 on 2019-03-09 19:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list_type', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('learned', models.BooleanField(default=False)),
                ('correct', models.IntegerField(default=0)),
                ('wrong', models.IntegerField(default=0)),
                ('interval', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WordList',
            fields=[
                ('word', models.CharField(max_length=30)),
                ('definition', models.CharField(max_length=200)),
                ('word_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='progress',
            name='word_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study.WordList'),
        ),
    ]
