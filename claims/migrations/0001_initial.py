# Generated by Django 4.1 on 2022-09-14 12:34

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Claim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('comment', models.TextField(blank=True, verbose_name='Comment')),
                ('object_id', models.IntegerField(blank=True, null=True, verbose_name='Claimed answer id')),
            ],
            options={
                'verbose_name': 'Claim',
                'verbose_name_plural': 'Claims',
                'ordering': ('-created',),
            },
        ),
    ]
