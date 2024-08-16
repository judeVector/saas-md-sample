from helpers.billing import get_customer_active_subscriptions, cancel_subscription

from customers.models import Customer
from subscriptions.models import Subscription, UserSubscription


def clear_dangling_subs():
    qs = Customer.objects.filter(stripe_id__isnull=False)
    for customer_obj in qs:
        user = customer_obj.user
        customer_stripe_id = customer_obj.stripe_id
        print(f"Sync {user} - {customer_stripe_id} subs and remove old ones.")
        subs = get_customer_active_subscriptions(customer_stripe_id)
        for sub in subs:
            existing_user_subs_qs = UserSubscription.objects.filter(
                stripe_id__iexact=f"{sub.id}".strip()
            )
            if existing_user_subs_qs.exists():
                continue
            cancel_subscription(
                sub.id,
                reason="Dangling active subscription",
                cancel_at_period_end=True,
            )
            print(sub.id, existing_user_subs_qs.exists())


def sync_subs_group_permissions():
    query_set = Subscription.objects.filter(active=True)
    for obj in query_set:
        # print(obj.groups.all())
        sub_perms = obj.permissions.all()
        for group in obj.groups.all():
            group.permissions.set(sub_perms)
