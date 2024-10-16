# Generated by Django 5.0.7 on 2024-10-14 15:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClassGroup',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('segment', models.CharField(blank=True, max_length=50)),
                ('director', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('director', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField(blank=True)),
                ('gender', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('relationship', models.CharField(max_length=50)),
                ('allergies', models.TextField(blank=True, null=True)),
                ('patient_notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField(blank=True)),
                ('gender', models.CharField(max_length=10)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('birth_date', models.DateTimeField(blank=True, null=True)),
                ('position', models.CharField(blank=True, max_length=50, null=True)),
                ('registry', models.CharField(max_length=20, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='patients.department')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allergies', models.TextField(blank=True, null=True)),
                ('patient_notes', models.TextField(blank=True, null=True)),
                ('employee', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='info', to='patients.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField(blank=True)),
                ('gender', models.CharField(max_length=10)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('registry', models.CharField(max_length=20, unique=True)),
                ('birth_date', models.DateTimeField(blank=True, null=True)),
                ('father_name', models.CharField(blank=True, max_length=100, null=True)),
                ('father_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('mother_name', models.CharField(blank=True, max_length=100, null=True)),
                ('mother_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('class_group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='patients.classgroup')),
            ],
        ),
        migrations.CreateModel(
            name='StudentInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allergies', models.TextField(blank=True, null=True)),
                ('patient_notes', models.TextField(blank=True, null=True)),
                ('student', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='info', to='patients.student')),
            ],
        ),
    ]
