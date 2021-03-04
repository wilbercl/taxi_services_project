from django.db import models
from polls.constant import *


class TaxiService(models.Model):

    id = models.IntegerField(primary_key=True)
    vendor_id = models.PositiveSmallIntegerField(null=True, choices=VENDOR_ID_CHOICES)
    tpep_pickup_datetime = models.DateTimeField(db_index=True)
    tpep_dropoff_datetime = models.DateTimeField()
    passenger_count = models.IntegerField()
    trip_distance = models.DecimalField(max_digits=10, decimal_places=2)
    rate_code_id = models.PositiveSmallIntegerField(choices=RATE_CODE_ID_CHOICES)
    store_and_fwd_flag = models.CharField(max_length=1)
    pu_location_id = models.IntegerField()
    do_location_id = models.IntegerField()
    payment_type = models.PositiveSmallIntegerField(choices=PAYMENT_TYPE_CHOICES)
    fare_amount = models.DecimalField(max_digits=10, decimal_places=2)
    extra = models.DecimalField(max_digits=10, decimal_places=2)
    mta_tax = models.DecimalField(max_digits=10, decimal_places=2)
    tip_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tolls_amount = models.DecimalField(max_digits=10, decimal_places=2)
    improvement_surcharge = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    congestion_surcharge = models.DecimalField(max_digits=10, decimal_places=2)