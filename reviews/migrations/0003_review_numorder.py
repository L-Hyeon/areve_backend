# Generated by Django 4.0.2 on 2022-03-12 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_review_writername'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='numOrder',
            field=models.IntegerField(default=-1, verbose_name='주문번호'),
        ),
    ]
