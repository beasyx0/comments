# Generated by Django 3.1.5 on 2021-02-16 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0008_commentflags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentflags',
            name='reason',
            field=models.CharField(choices=[('AB', 'Abuse'), ('LA', 'Language'), ('OF', 'Offensive'), ('OT', 'Other'), ('SP', 'Spam')], default='OT', max_length=2),
        ),
    ]
