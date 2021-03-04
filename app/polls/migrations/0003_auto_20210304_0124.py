# Generated by Django 2.2 on 2021-03-04 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20210303_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxiservice',
            name='congestion_surcharge',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='taxiservice',
            name='extra',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='taxiservice',
            name='fare_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='taxiservice',
            name='improvement_surcharge',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='taxiservice',
            name='mta_tax',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='taxiservice',
            name='tip_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='taxiservice',
            name='tolls_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='taxiservice',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='taxiservice',
            name='trip_distance',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
