# Generated by Django 4.0 on 2021-12-09 23:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BMIAPP', '0003_bmi_history_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='bmi_history',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='BMIAPP.user'),
        ),
    ]
