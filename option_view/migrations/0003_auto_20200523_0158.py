# Generated by Django 2.0 on 2020-05-23 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('option_view', '0002_auto_20200522_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='code',
            field=models.CharField(default='', max_length=20),
        ),
    ]