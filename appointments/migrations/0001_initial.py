# Generated by Django 5.0.7 on 2024-10-14 15:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('patients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeAppointment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('infirmary', models.CharField(max_length=50)),
                ('nurse', models.CharField(max_length=50)),
                ('date', models.DateTimeField()),
                ('reason', models.TextField()),
                ('treatment', models.TextField()),
                ('notes', models.TextField(blank=True, null=True)),
                ('revaluation', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.employee')),
            ],
        ),
        migrations.CreateModel(
            name='StudentAppointment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('infirmary', models.CharField(max_length=50)),
                ('nurse', models.CharField(max_length=50)),
                ('current_class', models.CharField(max_length=50)),
                ('date', models.DateTimeField()),
                ('reason', models.TextField()),
                ('treatment', models.TextField()),
                ('notes', models.TextField(blank=True, null=True)),
                ('revaluation', models.BooleanField(default=False)),
                ('contact_parents', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.student')),
            ],
        ),
        migrations.CreateModel(
            name='VisitorAppointment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('infirmary', models.CharField(max_length=50)),
                ('nurse', models.CharField(max_length=50)),
                ('date', models.DateTimeField()),
                ('reason', models.TextField()),
                ('treatment', models.TextField()),
                ('notes', models.TextField(blank=True, null=True)),
                ('revaluation', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('visitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.visitor')),
            ],
        ),
    ]
