# Generated by Django 3.0.1 on 2020-01-22 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokus', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userupload',
            name='file',
            field=models.FileField(max_length=500, upload_to='userupload/files/'),
        ),
    ]
