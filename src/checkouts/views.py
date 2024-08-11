from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings


from subscriptions.models import SubscriptionPrice
from helpers import billing


BASE_URL = settings.BASE_URL


# Create your views here.
def product_price_redirect_view(request, price_id=None, *args, **kwargs):
    request.session["checkout_subscription_price_id"] = price_id
    return redirect("checkouts:stripe-checkout-start")


@login_required
def checkout_redirect_view(request):
    checkout_subscription_price_id = request.session.get(
        "checkout_subscription_price_id"
    )
    try:
        object = SubscriptionPrice.objects.get(id=checkout_subscription_price_id)
    except:
        object = None

    if checkout_subscription_price_id is None or object is None:
        return redirect("subscriptions:pricing")
    customer_stripe_id = request.user.customer.stripe_id

    success_url_path = reverse("checkouts:stripe-checkout-end")
    success_url = f"{BASE_URL}{success_url_path}"

    pricing_url_path = reverse("subscriptions:pricing")
    cancel_url = f"{BASE_URL}{pricing_url_path}"

    price_stripe_id = object.stripe_id

    url = billing.start_checkout_session(
        customer_stripe_id,
        success_url=success_url,
        cancel_url=cancel_url,
        price_stripe_id=price_stripe_id,
        raw=False,
    )
    return redirect(url)


def checkout_finalize_view(request):
    session_id = request.GET.get("session_id")
    checkout_response = billing.get_checkout_session(session_id, raw=True)
    customer_id = checkout_response.customer

    subscription_stripe_id = checkout_response.subscription
    subscription_response = billing.get_subscription(subscription_stripe_id, raw=True)

    subscription_plan = subscription_response.plan
    subscription_plan_price_stripe_id = subscription_plan.id

    price_qs = SubscriptionPrice.objects.filter(
        stripe_id=subscription_plan_price_stripe_id
    )
    print(price_qs)

    context = {
        "checkout": checkout_response,
        "subscription": subscription_response,
    }
    return render(request, "checkout/success.html", context)
