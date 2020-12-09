# Generated by Django 3.1.3 on 2020-12-04 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cit2020', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='level',
            old_name='l_number',
            new_name='Q_number',
        ),
        migrations.RenameField(
            model_name='level',
            old_name='text',
            new_name='Question',
        ),
        migrations.RenameField(
            model_name='level',
            old_name='numuser',
            new_name='correct',
        ),
        migrations.AddField(
            model_name='level',
            name='option1',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='level',
            name='option2',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='level',
            name='option3',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='level',
            name='option4',
            field=models.CharField(max_length=200, null=True),
        ),
    ]