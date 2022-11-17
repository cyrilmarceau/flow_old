# Generated by Django 4.1.3 on 2022-11-17 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='firstname',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Prénom'),
        ),
        migrations.AddField(
            model_name='user',
            name='lastname',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Nom'),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Numéro de téléphone'),
        ),
    ]