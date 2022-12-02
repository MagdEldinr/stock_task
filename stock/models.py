from django.db import models
from django.core.validators import MinValueValidator

class Stock(models.Model):
    stock_id = models.CharField(max_length=128, unique=True)
    price = models.IntegerField()
    daily_highest_price = models.IntegerField(default=0)
    daily_lowest_price = models.IntegerField(default=0)
    hourly_highest_price = models.IntegerField(default=0)
    hourly_lowest_price = models.IntegerField(default=0)
    name = models.CharField(max_length=32)
    availability = models.IntegerField(validators=[
            MinValueValidator(0)
        ])
    timestamp = models.DateTimeField()

    class Meta:
        app_label = "stock"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        created = self.pk is None
        if created:
            self._reset_daily_prices()
            self.hourly_highest_price = self.hourly_lowest_price = self.price
            return super(Stock, self).save(*args, **kwargs)
        previous_object = self.__class__.objects.get(pk=self.pk)
        if self.timestamp.date() > previous_object.timestamp.date():
            self._reset_daily_prices()
        else:
            self._update_daily_prices(previous_object)
        
        if self.timestamp.hour > previous_object.timestamp.hour:
            self._reset_hourly_prices()
        else:
            self._update_hourly_prices(previous_object)
        return super(Stock, self).save(*args, **kwargs)

    def _update_daily_prices(self, previous_object):
        self._update_daily_highest_price(previous_object)
        self._update_daily_lowest_price(previous_object)

    def _update_hourly_prices(self, previous_object):
        self._update_hourly_highest_price(previous_object)
        self._update_hourly_lowest_price(previous_object)

    def _update_daily_highest_price(self, previous_object):
        if self.price > previous_object.daily_highest_price:
            self.daily_highest_price = self.price
        else:
            self.daily_highest_price = previous_object.daily_highest_price

    def _update_daily_lowest_price(self, previous_object):
        if self.price < previous_object.daily_lowest_price:
            self.daily_lowest_price = self.price
        else:
            self.daily_lowest_price = previous_object.daily_lowest_price

    def _update_hourly_highest_price(self, previous_object):
        if self.price > previous_object.hourly_highest_price:
            self.hourly_highest_price = self.price
        else:
            self.hourly_highest_price = previous_object.hourly_highest_price

    def _update_hourly_lowest_price(self, previous_object):
        if self.price < previous_object.hourly_lowest_price:
            self.hourly_lowest_price = self.price
        else:
            self.hourly_lowest_price = previous_object.hourly_lowest_price
    
    def _reset_daily_prices(self):
        self.daily_highest_price = self.daily_lowest_price = self.price

    def _reset_hourly_prices(self):
        self.hourly_highest_price = self.hourly_lowest_price = self.price
    

class User(models.Model):
    funds = models.IntegerField(default=10000)

    def __str__(self):
        return "User {}".format(self.id)

class Transaction(models.Model):
    ACTION_CHOICES = (
        ("sell", "sell"),
        ("buy", "buy"),
    )

    created_at = models.DateTimeField(auto_now=True)
    stock = models.ForeignKey("Stock", on_delete=models.CASCADE, blank=False, null=False)
    user = models.ForeignKey("User", on_delete=models.CASCADE, blank=False, null=False)
    action_type = models.CharField(choices=ACTION_CHOICES, blank=False, null=False, max_length=32)
