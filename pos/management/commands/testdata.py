from django.core.management.base import BaseCommand
from pos.models import Order, OrderProduct, CustomUser, Product


class Command(BaseCommand):
    help = "Creates test data should not be used in prod."

    def handle(self, *args, **options):
        pass
