# Generated by Django 4.0.3 on 2022-06-01 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nodedevice', '0002_alter_nodedevice_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nodedevice',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
