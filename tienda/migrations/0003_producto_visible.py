# Generated by Django 3.2.25 on 2025-06-15 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0002_auto_20250611_1008'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='visible',
            field=models.BooleanField(default=True),
        ),
    ]
