# Generated by Django 4.1.2 on 2022-10-10 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='Code')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('google_id', models.CharField(help_text='ID for use as an argument for Google.Translate API', max_length=2, verbose_name='Google.Translate id')),
            ],
            options={
                'verbose_name': 'Language',
                'verbose_name_plural': 'Languages',
                'ordering': ('-name',),
            },
        ),
    ]
