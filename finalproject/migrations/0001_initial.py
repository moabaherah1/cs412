# Generated by Django 5.1.5 on 2025-04-14 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.TextField(blank=True)),
                ('nick_name', models.TextField(blank=True)),
                ('address', models.TextField(blank=True)),
                ('email', models.TextField(blank=True)),
                ('dob', models.DateField()),
                ('image', models.URLField()),
            ],
        ),
    ]
