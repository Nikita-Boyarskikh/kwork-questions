# Generated by Django 4.1 on 2022-09-15 10:16

import accounts.validators
from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import djmoney.models.fields
import djmoney.models.validators
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Public identifier')),
                ('balance_currency', djmoney.models.fields.CurrencyField(choices=[('USDT', 'USDT crypto currency')], default='USDT', editable=False, max_length=4)),
                ('balance', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), max_digits=14, validators=[djmoney.models.validators.MinMoneyValidator(0)], verbose_name='Balance')),
            ],
            options={
                'verbose_name': 'Account',
                'verbose_name_plural': 'Accounts',
                'ordering': ('-user__date_joined',),
            },
        ),
        migrations.CreateModel(
            name='AccountAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='Public identifier')),
                ('type', models.CharField(choices=[('pay_service_fee', 'Pay Service Fee'), ('get_award', 'Get Award'), ('withdraw', 'Withdraw'), ('deposit', 'Deposit'), ('other', 'Other')], default='other', max_length=100, verbose_name='Type')),
                ('status', models.CharField(choices=[('created', 'Created'), ('approved', 'Approved'), ('declined', 'Declined')], default='created', max_length=100, verbose_name='Status')),
                ('delta_currency', djmoney.models.fields.CurrencyField(choices=[('USDT', 'USDT crypto currency')], default='USDT', editable=False, max_length=4)),
                ('delta', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('0'), max_digits=14, validators=[accounts.validators.not_zero_money_validator], verbose_name='Delta')),
                ('comment', models.TextField(blank=True, verbose_name='Comment')),
                ('object_id', models.IntegerField(blank=True, null=True, verbose_name='Awarded/payed for question/answer id')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.account')),
                ('content_type', models.ForeignKey(blank=True, limit_choices_to=models.Q(models.Q(('app_label', 'questions'), ('model', 'question')), models.Q(('app_label', 'answers'), ('model', 'answer')), _connector='OR'), null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Account Action',
                'verbose_name_plural': 'Account Actions',
                'ordering': ('-created',),
            },
        ),
    ]
