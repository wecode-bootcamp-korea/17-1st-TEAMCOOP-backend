# Generated by Django 3.1.6 on 2021-02-22 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_auto_20210219_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='icon',
            field=models.URLField(max_length=2000, null=True),
        ),
    ]
