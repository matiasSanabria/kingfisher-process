# Generated by Django 3.0.4 on 2021-02-04 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0010_collection_compilation_started'),
    ]

    operations = [
        migrations.AddField(
            model_name='collectionnote',
            name='code',
            field=models.TextField(blank=True, choices=[('INFO', 'Info'), ('ERROR', 'Error'), ('WARNING', 'Warning')]),
        ),
    ]
