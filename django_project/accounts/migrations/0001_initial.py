# Generated by Django 4.1 on 2023-04-27 17:59

import accounts.utils
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('pkid', models.BigAutoField(editable=False, primary_key=True, serialize=False, verbose_name='№')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('email', models.CharField(max_length=50, unique=True, verbose_name='Address')),
                ('first_name', models.CharField(max_length=50, verbose_name='First name')),
                ('last_name', models.CharField(blank=True, max_length=50, verbose_name='Last name')),
                ('phone', models.CharField(blank=True, max_length=15, null=True, verbose_name='Phone')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='Birth date')),
                ('code', models.CharField(blank=True, max_length=6, null=True, verbose_name='Verification code')),
                ('is_verified', models.BooleanField(default=False, verbose_name='Is verified')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('avatar', models.ImageField(null=True, upload_to=accounts.utils.get_upload_path, verbose_name='Avatar')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Staff status')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Superuser status')),
                ('changed_password_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='changed_password_date')),
                ('user_language', models.CharField(choices=[('ru', 'Russian'), ('eng', 'English')], default='ru', max_length=4, verbose_name='User language')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'ordering': ['pkid'],
            },
        ),
    ]
