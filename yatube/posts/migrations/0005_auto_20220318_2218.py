# Generated by Django 2.2.19 on 2022-03-18 22:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20220301_0407'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={
                'ordering': ('-pub_date',),
                'verbose_name_plural': 'Посты',
            },
        ),
    ]
