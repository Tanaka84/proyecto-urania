# Generated by Django 3.2.4 on 2021-07-10 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dicval', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='diccionario',
            name='no_de_votos',
            field=models.IntegerField(default=0),
        ),
    ]