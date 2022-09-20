# Generated by Django 4.1 on 2022-09-20 11:56

import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import users.models
import users.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('countries', '0001_initial'),
        ('languages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=users.models._build_avatar_filename, verbose_name='Avatar')),
                ('email', models.EmailField(max_length=254, verbose_name='email address')),
                ('is_approved', models.BooleanField(default=False, help_text='User approved with control question.', verbose_name='Approved')),
                ('is_user_agreement_accepted', models.BooleanField(default=False, help_text='User can create a question only after accept a user agreement.', verbose_name='User agreement accepted')),
                ('pin', models.CharField(max_length=128, verbose_name='Pin')),
                ('sex', models.CharField(blank=True, choices=[(None, 'Prefer not to say / unsure'), ('male', 'Male'), ('female', 'Female')], max_length=10, null=True, verbose_name='Sex')),
                ('education', models.CharField(blank=True, choices=[(None, 'Without education'), ('associate', 'Associate'), ('bachelor', 'Bachelor'), ('master', 'Master'), ('doctor', 'Doctor')], max_length=10, null=True, verbose_name='Education')),
                ('birth_year', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1900), users.validators.max_value_current_year_validator], verbose_name='Birth year')),
                ('country', models.ForeignKey(default='united_states', on_delete=django.db.models.deletion.SET_DEFAULT, to='countries.country')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('preferred_language', models.ForeignKey(default='en', on_delete=django.db.models.deletion.SET_DEFAULT, to='languages.language')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'ordering': ('-date_joined',),
            },
            managers=[
                ('objects', users.models.UserManager()),
            ],
        ),
    ]
