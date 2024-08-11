from django.shortcuts import render
from django.urls import reverse

from subscriptions.models import SubscriptionPrice


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
