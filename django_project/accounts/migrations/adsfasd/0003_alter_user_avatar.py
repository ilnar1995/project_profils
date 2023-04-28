# Generated by Django 4.1 on 2023-04-28 14:40

import accounts.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_actor_category_genre_ip_addres_movie_quality_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(null=True, upload_to=accounts.utils.get_upload_path, verbose_name='Avatar'),
        ),
    ]
