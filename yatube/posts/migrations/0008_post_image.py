# Generated by Django 2.2.19 on 2022-04-16 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0007_auto_20220410_2017"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="image",
            field=models.ImageField(
                blank=True,
                upload_to="posts/",
                verbose_name="Иллюстрация сообщения",
            ),
        ),
    ]
