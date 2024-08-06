# Generated by Django 5.0.7 on 2024-08-06 18:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('patients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Infirmary',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('capacity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeAppointment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('reason', models.TextField()),
                ('treatment', models.TextField()),
                ('notes', models.TextField(blank=True, null=True)),
                ('revaluation', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.employee')),
                ('infirmary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appointments.infirmary')),
            ],
        ),
        migrations.CreateModel(
            name='StudentAppointment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('reason', models.TextField()),
                ('treatment', models.TextField()),
                ('notes', models.TextField(blank=True, null=True)),
                ('revaluation', models.BooleanField(default=False)),
                ('contact_parents', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('infirmary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appointments.infirmary')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.student')),
            ],
        ),
        migrations.CreateModel(
            name='VisitorAppointment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('reason', models.TextField()),
                ('treatment', models.TextField()),
                ('notes', models.TextField(blank=True, null=True)),
                ('revaluation', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('infirmary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appointments.infirmary')),
                ('visitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.visitor')),
            ],
        ),
    ]
