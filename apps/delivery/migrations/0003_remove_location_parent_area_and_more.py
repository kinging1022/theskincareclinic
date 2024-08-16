# Generated by Django 4.2 on 2024-08-12 20:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0002_remove_location_name_location_location_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='parent',
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.CharField(max_length=225)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='areas', to='delivery.location')),
            ],
        ),
        migrations.AlterField(
            model_name='deliveryprice',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='delivery.area'),
        ),
    ]
