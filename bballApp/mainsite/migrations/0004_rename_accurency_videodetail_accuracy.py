# Generated by Django 3.2.12 on 2022-06-07 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0003_alter_videodetail_pub_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='videodetail',
            old_name='accurency',
            new_name='accuracy',
        ),
    ]
