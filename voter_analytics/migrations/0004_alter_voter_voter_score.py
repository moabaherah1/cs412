# Generated by Django 5.1.5 on 2025-04-01 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voter_analytics', '0003_alter_voter_precinct_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voter',
            name='Voter_Score',
            field=models.TextField(),
        ),
    ]
