from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from subscriptions.models import SubscriptionPrice, UserSubscription
from helpers.billing import get_checkout_session


@login_required
def user_subscription_view(
    request,
):
    user_subscription_object, created = UserSubscription.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        print("Refresh Sub")
    subscription_data = {}
    if user_subscription_object.stripe_id:
        subscription_data = get_checkout_session(user_subscription_object.stripe_id)
    return render(
        request,
        "subscriptions/user_detail_view.html",
        {"subscription": subscription_data},
    )


def subscription_price_view(request, interval="month"):
    # Query the SubscriptionPrice model to get all featured subscription prices.
    qs = SubscriptionPrice.objects.filter(featured=True)

    # Define constants for monthly and yearly intervals.
    interval_monthly = SubscriptionPrice.IntervalChoices.MONTHLY
    interval_yearly = SubscriptionPrice.IntervalChoices.YEARLY

    # Set the default object list to monthly subscriptions.
    object_list = qs.filter(interval=interval_monthly)

    # Name of the URL pattern to reverse, prefixed with the app name.
    url_path_name = "subscriptions:pricing_interval"

    # Generate URLs for switching between monthly and yearly views.
    monthly_url = reverse(url_path_name, kwargs={"interval": interval_monthly})
    yearly_url = reverse(url_path_name, kwargs={"interval": interval_yearly})

    active = interval_monthly

    # If the interval in the request is yearly, update the object list to yearly subscriptions.
    if interval == interval_yearly:
        active = interval_yearly
        object_list = qs.filter(interval=interval_yearly)

    context = {
        "object_list": object_list,
        "monthly_url": monthly_url,
        "yearly_url": yearly_url,
        "active": active,
    }

    return render(request, "subscriptions/pricing.html", context)
