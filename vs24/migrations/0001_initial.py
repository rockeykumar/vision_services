# Generated by Django 2.2.6 on 2019-10-06 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('FName', models.CharField(max_length=30)),
                ('LName', models.CharField(max_length=30)),
                ('Email', models.EmailField(max_length=30, primary_key=True, serialize=False)),
                ('Mobile', models.CharField(max_length=30)),
                ('Password', models.CharField(max_length=30)),
            ],
        ),
    ]
