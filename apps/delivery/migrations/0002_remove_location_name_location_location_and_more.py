# Generated by Django 4.2 on 2024-08-12 18:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='name',
        ),
        migrations.AddField(
            model_name='location',
            name='location',
            field=models.CharField(default='Lagos', max_length=225),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='streets', to='delivery.location'),
        ),
    ]
