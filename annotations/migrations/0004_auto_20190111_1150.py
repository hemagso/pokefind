# Generated by Django 2.1.5 on 2019-01-11 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotations', '0003_auto_20190109_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
