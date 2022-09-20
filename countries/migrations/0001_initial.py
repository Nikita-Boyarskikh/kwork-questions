# Generated by Django 4.1 on 2022-09-20 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('languages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='Code')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('population', models.IntegerField(blank=True, null=True, verbose_name='Population')),
                ('live_quality_index', models.IntegerField(blank=True, help_text='From https://ru.wikipedia.org/wiki/Список_стран_по_индексу_человеческого_развития', null=True, verbose_name='Live quality index')),
                ('language', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='languages.language')),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
                'ordering': ('name',),
            },
        ),
    ]
