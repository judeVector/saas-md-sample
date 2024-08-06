from typing import Any
from django.core.management.base import BaseCommand

from subscriptions.models import Subscription


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):
        self.stdout.write("Syncing Started")
        query_set = Subscription.objects.filter(active=True)
        for obj in query_set:
            # print(obj.groups.all())
            sub_perms = obj.permissions.all()
            for group in obj.groups.all():
                group.permissions.set(sub_perms)
        self.stdout.write(self.style.SUCCESS("Syncing Successful"))
