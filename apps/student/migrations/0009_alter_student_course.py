# Generated by Django 4.2 on 2024-10-02 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_student_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.course'),
        ),
    ]
