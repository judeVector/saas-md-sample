from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model

User = get_user_model()


# Create your views here.
@login_required
def profile_view(request, username=None, *args, **kwargs):
    profile_user_obj = User.objects.get(username=username)
    return HttpResponse("Hello World")


@login_required
def profile_detail_view(request, username=None, *args, **kwargs):
    user = request.user
    print(user.has_perm("subscriptions.basic"))
    print(user.has_perm("subscriptions.pro"))
    print(user.has_perm("subscriptions.advanced"))
    print(user.has_perm("subscriptions.basic_ai"))
    user_groups = user.groups.all()
    print("user_groups", user_groups)
    if user_groups.filter(name__icontains="basic").exists():
        return HttpResponse("Congrats! You have successfully registered")

    return render(request, "profiles/detail.html", {})
