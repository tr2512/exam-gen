# Generated by Django 4.1 on 2023-07-07 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quizz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
                ('qtype', models.TextField(blank=True, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='comment',
            name='course',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='lesson',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='course',
        ),
        migrations.RemoveField(
            model_name='course',
            name='categories',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Lesson',
        ),
        migrations.AddField(
            model_name='quizz',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to='course.course'),
        ),
    ]