# Generated by Django 2.2 on 2021-03-06 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TaxiService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_id', models.PositiveSmallIntegerField(choices=[(1, 'Creative Mobile Technologies, LLC'), (2, 'VeriFone Inc.')], null=True)),
                ('tpep_pickup_datetime', models.DateTimeField(db_index=True)),
                ('tpep_dropoff_datetime', models.DateTimeField()),
                ('passenger_count', models.IntegerField()),
                ('trip_distance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('rate_code_id', models.PositiveSmallIntegerField(choices=[(1, 'Standard rate'), (2, 'JFK'), (3, 'Newark'), (4, 'Nassau or Westchester'), (5, 'Negotiated fare'), (6, 'Group ride')])),
                ('store_and_fwd_flag', models.CharField(max_length=1)),
                ('pu_location_id', models.IntegerField()),
                ('do_location_id', models.IntegerField()),
                ('payment_type', models.PositiveSmallIntegerField(choices=[(1, 'Credit card'), (2, 'Cash'), (3, 'No charge'), (4, 'Dispute'), (5, 'Unknown'), (6, 'Voided trip')])),
                ('fare_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('extra', models.DecimalField(decimal_places=2, max_digits=10)),
                ('mta_tax', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tip_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tolls_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('improvement_surcharge', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('congestion_surcharge', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]