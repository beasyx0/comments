# Generated by Django 3.1.5 on 2021-02-17 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0009_auto_20210216_1351'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='commentflags',
            constraint=models.UniqueConstraint(fields=('user', 'comment'), name='limit_flags_by_user'),
        ),
    ]