from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
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
    checkout_data = billing.get_checkout_customer_plan(session_id)

    plan_id = checkout_data.pop("plan_id")
    customer_id = checkout_data.pop("customer_id")
    subscription_stripe_id = checkout_data.pop("subscription_stripe_id")
    subscription_data = {**checkout_data}

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

    updated_sub_options = {
        "subscription": subscription_object,
        "stripe_id": subscription_stripe_id,
        "user_cancelled": False,
        **subscription_data,
    }
    try:
        _user_sub_object = UserSubscription.objects.get(user=user_object)
        _user_sub_exists = True
    except UserSubscription.DoesNotExist:
        _user_sub_object = UserSubscription.objects.create(
            user=user_object, **updated_sub_options
        )
    except:
        _user_sub_object = None

    if None in [subscription_object, user_object, _user_sub_object]:
        return HttpResponseBadRequest(
            "There was an error with your account, please contact us"
        )

    if _user_sub_exists:
        # Cancel old subscriptions
        old_stripe_id = _user_sub_object.stripe_id
        same_stripe_id = subscription_stripe_id == old_stripe_id
        if old_stripe_id is not None and not same_stripe_id:
            try:
                billing.cancel_subscription(
                    old_stripe_id,
                    reason="Auto ended, new membership",
                    feedback="other",
                )
            except:
                pass

        # Assign new subscriptions
        for k, v in updated_sub_options.items():
            setattr(_user_sub_object, k, v)
        _user_sub_object.save()
        # messages.success(request, "Success! Thank you for joining")
        # return redirect(_user_sub_object.get_absolute_url())

    context = {}
    return render(request, "checkout/success.html", context)
