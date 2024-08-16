from typing import Any
from django.core.management.base import BaseCommand

from subscriptions.utils import sync_subs_group_permissions


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):
        self.stdout.write("Syncing Started")
        sync_subs_group_permissions()
        self.stdout.write(self.style.SUCCESS("Syncing Successful"))
