# Generated by Django 4.0.2 on 2022-03-02 04:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0009_item_enddate_item_startdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='endDate',
            field=models.DateField(default=datetime.datetime.now, verbose_name='종료시간'),
        ),
        migrations.AlterField(
            model_name='item',
            name='startDate',
            field=models.DateField(default=datetime.datetime.now, verbose_name='시간시간'),
        ),
    ]