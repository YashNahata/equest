# Generated by Django 4.0.4 on 2022-06-17 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blogcomment_approved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogcomment',
            name='approved',
        ),
    ]
