# Generated by Django 3.2.8 on 2021-10-23 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0005_messagemodel_threadmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='Gender',
            field=models.CharField(choices=[('male', 'Male'), ('Female', 'Female')], max_length=10, null=True),
        ),
    ]