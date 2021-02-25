from django.core.management.base import BaseCommand, CommandError
import datetime as dt

from Clients.models import Engine

class Command(BaseCommand):
    """Custom command that would be scheduled to switch engines off when the date is at the day."""

    help = 'Switches off engines if they were scheduled to change state in future.'

    def handle(self, *args, **options):
        engines_to_be_switched = Engine.objects.filter(stop_running__date=dt.date.today(),
                                                       enabled=True).update(enabled=False)
        self.stdout.write(self.style.SUCCESS(f"Successfully disabled {engines_to_be_switched} engines."))