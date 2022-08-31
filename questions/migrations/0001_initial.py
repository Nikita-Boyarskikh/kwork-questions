# Generated by Django 4.1 on 2022-08-31 04:51

from decimal import Decimal
from django.db import migrations, models
import django.utils.timezone
import djmoney.models.fields
import djmoney.models.validators
import model_utils.fields
import utils.generic_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', models.CharField(choices=[('draft', 'In progress'), ('pending', 'Moderation'), ('approved', 'Ready for publication'), ('rejected', 'Refused'), ('published', 'Open'), ('answered', 'Voting'), ('closed', 'Closed')], default='draft', max_length=100, verbose_name='Status')),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='status')),
                ('reason', models.TextField(blank=True, verbose_name='Rejected reason')),
                ('original_text', models.TextField(verbose_name='Original text')),
                ('en_text', models.TextField(verbose_name='Translated to english text')),
                ('price_currency', djmoney.models.fields.CurrencyField(choices=[('USDT', 'USDT crypto currency')], default='USDT', editable=False, max_length=4)),
                ('price', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), max_digits=14, validators=[djmoney.models.validators.MinMoneyValidator(Decimal('0'))], verbose_name='Price')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
                'ordering': ('-price',),
            },
            bases=(models.Model, utils.generic_fields.WithSelfContentTypeMixin),
        ),
    ]
