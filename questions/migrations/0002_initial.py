# Generated by Django 4.1 on 2022-09-28 22:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('countries', '0001_initial'),
        ('questions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('answers', '0002_initial'),
        ('languages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='author',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='question',
            name='best_answer',
            field=models.OneToOneField(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='best_for_question', to='answers.answer'),
        ),
        migrations.AddField(
            model_name='question',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='countries.country'),
        ),
        migrations.AddField(
            model_name='question',
            name='language',
            field=models.ForeignKey(on_delete=models.SET('en'), to='languages.language'),
        ),
        migrations.AddField(
            model_name='comment',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.question'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together={('question', 'user')},
        ),
    ]
