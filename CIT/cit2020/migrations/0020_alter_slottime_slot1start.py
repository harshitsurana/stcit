# Generated by Django 3.2.9 on 2022-01-02 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cit2020', '0019_alter_slottime_slot1start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slottime',
            name='slot1start',
            field=models.DateTimeField(default=(2022, 1, 1, 4, 40, 0, 701322)),
        ),
    ]