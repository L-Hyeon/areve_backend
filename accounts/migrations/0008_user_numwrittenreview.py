# Generated by Django 4.0.2 on 2022-03-12 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_user_sigungu'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='numWrittenReview',
            field=models.IntegerField(default=0, verbose_name='작성 리뷰 수'),
        ),
    ]
