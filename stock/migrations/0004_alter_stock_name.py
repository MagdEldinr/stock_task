# Generated by Django 3.2.16 on 2022-12-02 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='name',
            field=models.CharField(max_length=32),
        ),
    ]
