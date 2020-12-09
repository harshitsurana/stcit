# Generated by Django 3.1.3 on 2020-12-04 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cit2020', '0005_save_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='audio',
            field=models.FileField(blank=True, upload_to='audios'),
        ),
        migrations.AlterField(
            model_name='question',
            name='image',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
    ]