# Generated by Django 4.0.6 on 2022-07-12 10:37

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
                ('yandex_id', models.CharField(help_text='ID for use as an argument for Yandex.Translate API', max_length=2, verbose_name='Yandex.Translate id')),
            ],
            options={
                'verbose_name': 'Language',
                'verbose_name_plural': 'Languages',
            },
        ),
    ]
