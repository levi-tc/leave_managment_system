# Generated by Django 5.1 on 2024-08-22 09:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LeaveRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_type', models.CharField(choices=[('annual', 'Annual Leave'), ('sick', 'Sick Leave'), ('unpaid', 'Unpaid Leave'), ('other', 'Other')], max_length=20)),
                ('other_leave_type', models.CharField(blank=True, max_length=50, null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('return_date', models.DateField()),
                ('total_days', models.IntegerField()),
                ('reason', models.TextField()),
                ('contact_during_leave', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('denied', 'Denied')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
