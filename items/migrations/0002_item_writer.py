# Generated by Django 4.0.2 on 2022-02-11 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='writer',
            field=models.IntegerField(default=0, verbose_name='작성자'),
        ),
    ]
