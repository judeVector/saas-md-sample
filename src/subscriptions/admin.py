from django.contrib import admin
from .models import Subscription, UserSubscription, SubscriptionPrice


# Register your models here.


class SubscriptionPrice(admin.TabularInline):
    model = SubscriptionPrice
    readonly_fields = ["stripe_id"]
    can_delete = False
    extra = 0


class SubscriptionAdmin(admin.ModelAdmin):
    inlines = [SubscriptionPrice]
    readonly_fields = ["stripe_id"]
    list_display = [
        "name",
        "active",
    ]


admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(UserSubscription)
