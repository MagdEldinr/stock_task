# Generated by Django 3.2.16 on 2022-12-01 03:18

from django.db import migrations, models

def create_initial_users(apps, schema_editor):
    User = apps.get_model("stock", "User")
    User.objects.create(funds=100)
    User.objects.create(funds=1000)
    User.objects.create(funds=10000)

class Migration(migrations.Migration):


    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('funds', models.IntegerField(default=10000)),
            ],
        ),
        migrations.RunPython(create_initial_users)
    ]
