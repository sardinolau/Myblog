# Generated by Django 3.0.6 on 2020-06-09 12:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200607_2213'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='parent_conment',
            new_name='parent_comment',
        ),
    ]
