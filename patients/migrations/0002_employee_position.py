# Generated by Django 5.0.7 on 2024-08-09 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='position',
            field=models.CharField(max_length=50, null=True),
        ),
    ]