from django.db.models import Q

from helpers.billing import (
    get_customer_active_subscriptions,
    cancel_subscription,
    get_subscription,
)

from customers.models import Customer
from subscriptions.models import Subscription, UserSubscription, SubscriptionStatus


def refresh_active_users_subscriptions(user_ids=None):

    # active_qs = qs.filter(status=SubscriptionStatus.ACTIVE)
    # trailing_qs = qs.filter(status=SubscriptionStatus.TRIALING)
    # qs = qs.filter(active_qs_lookup),filter(user_id__in=user_ids)

    active_qs_lookup = Q(status=SubscriptionStatus.ACTIVE) | Q(
        status=SubscriptionStatus.TRIALING
    )
    qs = UserSubscription.objects.filter(active_qs_lookup)

    if user_ids is not None:
        qs = qs.by_user_ids(user_ids=user_ids)
    complete_count = 0
    qs_count = qs.count()
    for user_subscription_object in qs:
        if user_subscription_object.stripe_id:
            subscription_data = get_subscription(
                user_subscription_object.stripe_id, raw=False
            )
            for k, v in subscription_data.items():
                setattr(user_subscription_object, k, v)
            user_subscription_object.save()
            complete_count += 1
        return complete_count == qs_count


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
