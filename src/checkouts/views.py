from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponseBadRequest


from subscriptions.models import SubscriptionPrice, Subscription, UserSubscription
from helpers import billing


BASE_URL = settings.BASE_URL
User = get_user_model()


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
    customer_id, plan_id = billing.get_checkout_customer_plan(session_id)

    price_qs = SubscriptionPrice.objects.filter(stripe_id=plan_id)
    print(price_qs)

    try:
        subscription_object = Subscription.objects.get(
            subscriptionprice__stripe_id=plan_id
        )
    except:
        subscription_object = None

    try:
        user_object = User.objects.get(customer__stripe_id=customer_id)
    except:
        user_object = None

    _user_sub_exists = False
    try:
        _user_sub_object = UserSubscription.objects.get(user=user_object)
        _user_sub_exists = True
    except UserSubscription.DoesNotExist:
        _user_sub_object = UserSubscription.objects.create(
            user=user_object, subcription=subscription_object
        )
    except:
        _user_sub_object = None

    if None in [subscription_object, user_object, _user_sub_object]:
        return HttpResponseBadRequest(
            "There was an error with your account, please contact us"
        )

    if _user_sub_exists:
        # Cancel old subscriptions

        # Assign new subscriptions
        _user_sub_object.subscription = subscription_object
        _user_sub_object.save()

    context = {}
    return render(request, "checkout/success.html", context)
