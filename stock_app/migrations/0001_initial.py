# Generated by Django 2.0 on 2020-06-06 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='stock_vol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='', max_length=20)),
                ('name', models.CharField(default='', max_length=20)),
                ('vol', models.FloatField()),
                ('vol_day_mean', models.FloatField()),
                ('change', models.DateField()),
                ('date', models.DateField()),
            ],
            options={
                'db_table': 'stock_vol',
            },
        ),
    ]
