# Generated by Django 3.1.3 on 2020-12-04 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cit2020', '0003_auto_20201204_1939'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='current_level',
            new_name='current_question',
        ),
    ]
