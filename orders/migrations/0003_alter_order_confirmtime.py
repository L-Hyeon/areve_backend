# Generated by Django 4.0.2 on 2022-03-11 06:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_endtime_alter_order_starttime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='confirmTime',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='확정시간'),
        ),
    ]