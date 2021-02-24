import datetime as dt

from phonenumber_field.modelfields import PhoneNumberField

from django.db import models
from django.utils.timezone import now
from django.utils import timezone
from django.contrib.postgres.fields import DateRangeField



class Company(models.Model):
    """Company model"""
    name = models.CharField(max_length=200)
    contact = PhoneNumberField()

    class Meta:
        verbose_name_plural = 'companies'


class Installation(models.Model):
    """Installation model"""

    installation_name = models.CharField(max_length=200)
    installation_location = models.CharField(max_length=300)
    #instalation_type
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class Contract(models.Model):
    """Contract model that refers to a specific installation"""
    contract_start = models.DateField()
    contract_end = models.DateField()
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

    # TODO 3 letters 
    ENGINE_3 = '3'
    ENGINE_2 = '2'
    ENGINE_CHOICES = [
        (ENGINE_2, 'Type 2'),
        (ENGINE_3, 'Type 3'),
    ]

    installation = models.OneToOneField(to=Installation, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=100, unique=True)

    # Types
    fuel_type = models.CharField(max_length=1, choices=FUEL_CHOICES)
    type = models.CharField(max_length=1, choices=ENGINE_CHOICES)

    # date when the engine has started
    start_running = models.DateTimeField(null=True)
    stop_running = models.DateTimeField(null=True, blank=True)

    # till when the engine is off
    stopped_till = models.DateTimeField(null=True, blank=True)

    # operating hours so far
    oph = models.FloatField(default=0)

    # expected average oph per month
    oph_per_month = models.FloatField()

    # hours between services
    interval = models.FloatField()
    general_interval = models.FloatField()

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

    class Meta:
        pass


    def oph_now(self, time=None):
        if not self.start_running:
            return self.oph

        if time is None:
            time = now()
        return self.oph + (time - self.start_running).total_seconds() / 3600

    def turn_off(self, time=None):
        """Method that switches off the engine and set date of its happening"""
        if not self.enabled:
            raise ValueError('Engine is already stopped.')
        if time is None:
            time = now()
        self.oph = self.oph_now(time)

        self.start_running = None
        self.stop_running = time

        self.enabled = False

    def oph_after_off(self, time=None):
        """Method that update date of each service related to the object."""
        if not self.stop_running:
            return
        if time is None:
            time = now()

        delta = time - self.stop_running
        print(delta)
        x = Service.objects.filter(engine=self).filter(date__gte=timezone.now().replace(hour=0, minute=0, second=0)).update(
            date=models.F('date')+delta)
        print(Service.objects.get(id=3).date)


    def turn_on(self, time=None):
        """Method that switches on the engine and recalculate dates of services."""
        if self.enabled:
            raise ValueError('Engine is already running.')

        if time is None:
            time = now()

        self.oph_after_off(time)

        self.stop_running = None
        self.start_running = time
        self.enabled = True

    @property
    def state(self):
        if self.enabled and self.start_running < timezone.now():
            return 'Engine is running.'
        else:
            return 'Engine is stopped.'


class Service(models.Model):
    """Model for services"""
    INSPECTION = '1'
    SEMI_GENERAL = '2'
    GENERAL = '3'
    ENGINE_CHOICES = [
        (INSPECTION, 'Inspection'),
        (SEMI_GENERAL, 'Semi general'),
        (GENERAL, 'General')
    ]

    service_type = models.CharField(max_length=1, choices=ENGINE_CHOICES)

    date = models.DateField()

    interval = models.FloatField()

    confirmed = models.BooleanField(default=False)
    engine = models.ForeignKey(Engine, null=True, on_delete=models.SET_NULL)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


