# Generated by Django 4.1.1 on 2022-09-30 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0002_alter_university_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='related',
            name='value',
            field=models.DecimalField(decimal_places=8, default=0.0, max_digits=10),
        ),
    ]
