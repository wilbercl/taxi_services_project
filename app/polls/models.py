from django.db import models
from .constant import *

# Create your models here.
class TaxiService(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    vendorID = models.PositiveSmallIntegerField(null=True, choices=VENDOR_ID_CHOICES)
    tpep_pickup_datetime = models.DateTimeField(db_index=True, blank=False)
    tpep_dropoff_datetime = models.DateTimeField(blank=False)
    passenger_count = models.IntegerField(null=False)
    trip_distance = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    ratecodeID = models.PositiveSmallIntegerField(choices=RATE_CODE_ID_CHOICES, null=False)
    store_and_fwd_flag = models.CharField(max_length=50, null=False)
    PULocationID = models.IntegerField(null=False)
    DOLocationID = models.IntegerField(null=False)
    payment_type = models.PositiveSmallIntegerField(choices=PAYMENT_TYPE_CHOICES, null=False)
    fare_amount =models.DecimalField(null=False, max_digits=10, decimal_places=2)
    extra = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    mta_tax = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    tip_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    tolls_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    improvement_surcharge =models.DecimalField(null=False, max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    congestion_surcharge = models.DecimalField(null=False, max_digits=10, decimal_places=2)