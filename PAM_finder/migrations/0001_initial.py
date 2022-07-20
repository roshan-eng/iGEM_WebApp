# Generated by Django 4.0.5 on 2022-07-10 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SeqModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('pdf', models.FileField(upload_to='pdf/')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
    ]
