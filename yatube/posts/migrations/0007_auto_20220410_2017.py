# Generated by Django 2.2.19 on 2022-04-10 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20220408_0950'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ('title',), 'verbose_name_plural': 'Группы'},
        ),
    ]
