# Generated by Django 5.0.6 on 2024-07-14 01:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_brandcategory_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brandcategory',
            name='ordering',
        ),
    ]
