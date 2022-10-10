# Generated by Django 4.1.2 on 2022-10-10 06:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('languages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Rule text')),
                ('language', models.ForeignKey(default='en', on_delete=django.db.models.deletion.CASCADE, to='languages.language')),
            ],
            options={
                'verbose_name': 'Rule',
                'verbose_name_plural': 'Rules',
            },
        ),
    ]
