from django.db import models
from django.contrib.postgres.fields import DateRangeField


class Company(models.Model):
    """Company model"""
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'companies'


class Installation(models.Model):
    """Installation model"""

    installation_name = models.CharField(max_length=200)
    installation_location = models.CharField(max_length=300)
    #instalation_type
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company')


class Contract(models.Model):
    """Contract model that refers to a specific installation"""
    period = DateRangeField()
    date_of_signing = models.DateField()
    price_per_hour = models.FloatField()
    oph_yet = models.FloatField(default=0)
    annotation = models.TextField(null=True, blank=True)
    installation = models.ForeignKey(Installation, on_delete=models.DO_NOTHING)



class Parts(models.Model):
    """Parts model"""
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'set of parts'
        verbose_name_plural = 'sets of parts'


class Part(models.Model):
    """Part model"""
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)
    units_in_stock = models.PositiveIntegerField()
    parent_category = models.CharField(max_length=300)
    set_of_parts = models.ForeignKey(Parts, on_delete=models.CASCADE)


class Engine(models.Model):
    """Engine model"""

    # Example choices for fuels
    FUEL_ONE = '1'
    FUEL_TWO = '2'
    FUEL_CHOICES = [
        (FUEL_ONE, 'One'),
        (FUEL_TWO, 'Two'),
    ]

    ENGINE_3 = '3'
    ENGINE_2 = '2'
    ENGINE_CHOICES = [
        (ENGINE_2, 'Type 2'),
        (ENGINE_3, 'Type 3'),
    ]

    serial_number = models.CharField(max_length=100, unique=True)

    # Types
    fuel_type = models.CharField(max_length=1, choices=FUEL_CHOICES)
    type = models.CharField(max_length=1, choices=ENGINE_CHOICES)

    # date when the engine has started
    start_date = models.DateTimeField()

    # operating hours so far
    oph = models.DurationField(default=0)

    # expected average oph per month
    oph_per_month = models.DurationField()

    # hours between small services
    interval = models.DurationField()

    # hours between general renovations
    general_interval = models.DurationField()

    # costs of services
    interval_cost = models.DecimalField(max_digits=6, decimal_places=2)
    general_cost = models.DecimalField(max_digits=11, decimal_places=2)
    half_general_cost = models.DecimalField(max_digits=9, decimal_places=2)

    # only for specific type of engine
    six_k_cost = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    # list of parts
    parts = models.ForeignKey(Parts, on_delete=models.SET_NULL, null=True)

    ##############################3
    # disabled engine
    enabled = models.BooleanField(default=True)
    disabled = models.DateTimeField(null=True, blank=True)

    class Meta:
        pass

    def switch_off(self, date):
        """Method that switches off the engine and set date of its happening"""
        self.enabled = False
        self.disabled = date






