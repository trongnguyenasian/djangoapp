# Generated by Django 2.1.4 on 2018-12-16 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='traning_img',
        ),
        migrations.AlterField(
            model_name='image',
            name='test_img',
            field=models.FileField(upload_to='data/test/021'),
        ),
    ]
