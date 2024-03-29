# Generated by Django 4.0.2 on 2022-02-16 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('reviewnumber', models.AutoField(primary_key=True, serialize=False)),
                ('score', models.IntegerField(verbose_name='평점')),
                ('content', models.TextField(verbose_name='리뷰내용')),
                ('cntImg', models.IntegerField(verbose_name='이미지 수')),
                ('image1', models.TextField(verbose_name='이미지1')),
                ('image2', models.TextField(verbose_name='이미지2')),
                ('image3', models.TextField(verbose_name='이미지3')),
                ('image4', models.TextField(verbose_name='이미지4')),
                ('image5', models.TextField(verbose_name='이미지5')),
                ('numItem', models.IntegerField(verbose_name='아이템번호')),
                ('numWriter', models.IntegerField(verbose_name='작성자번호')),
            ],
        ),
    ]
