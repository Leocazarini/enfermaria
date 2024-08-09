# Generated by Django 5.0.7 on 2024-08-08 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nurse',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('badge_number', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='infirmary',
            name='capacity',
        ),
    ]