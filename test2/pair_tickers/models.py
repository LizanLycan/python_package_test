from django.db import models
from django.utils import timezone


class Ticker(models.Model):
    pair = models.CharField(max_length=10)
    high = models.DecimalField(decimal_places=18, max_digits=21)
    low = models.DecimalField(decimal_places=18, max_digits=21)
    avg = models.DecimalField(decimal_places=18, max_digits=21)
    vol = models.DecimalField(decimal_places=18, max_digits=28)
    vol_cur = models.DecimalField(decimal_places=18, max_digits=28)
    last = models.DecimalField(decimal_places=18, max_digits=21)
    buy = models.DecimalField(decimal_places=18, max_digits=21)
    sell = models.DecimalField(decimal_places=18, max_digits=21)
    updated = models.BigIntegerField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    def __str__(self):
        return "{}: {}".format(self.pair, self.updated)

    def result_ask_bid(self, input_i):
        return self.sell - self.buy <= input_i
