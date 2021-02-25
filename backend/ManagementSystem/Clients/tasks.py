from celery import task
from celery import shared_task

from django.apps import apps
from django.db.models import F

import datetime as dt

@shared_task
def enable_engines():
    """Task that updates engines that are not running and supposed to be enabled today."""
    Engine = apps.get_model("Clients", "Engine")
    engines_to_be_switched = Engine.objects.filter(start_running__date=dt.date.today(),
                                                  enabled=False).update(enabled=True, stop_running=None)
    print(f"Successfully enabled {engines_to_be_switched} engines.")

@shared_task
def disable_engines():
    """Task that updates engines that are running and supposed to be disabled today."""
    Engine = apps.get_model("Clients", "Engine")
    engines_to_be_switched = Engine.objects.filter(stop_running__date=dt.date.today(),
                                                   enabled=True).update(enabled=False)
    print(f"Successfully disabled {engines_to_be_switched} engines.")

@shared_task
def update_oph():
    """Updating number of operating hours for each running engine."""
    Engine = apps.get_model('Clients', 'Engine')
    Engine.objects.filter(enabled=True).update(oph=F('oph')+1)
    print(Engine.objects.all().values('oph'))