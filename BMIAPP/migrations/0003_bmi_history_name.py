# Generated by Django 4.0 on 2021-12-09 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BMIAPP', '0002_bmi_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='bmi_history',
            name='name',
            field=models.CharField(max_length=25, null=True),
        ),
    ]
