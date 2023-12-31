# Generated by Django 4.1 on 2023-07-08 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='chapter_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='quiz', to='courses.chapter'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='course_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='quiz', to='courses.course'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Chapterquiz',
        ),
    ]
