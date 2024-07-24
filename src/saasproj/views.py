from django.shortcuts import render
from django.contrib.auth.decorators import login_required


VALID_CODE = "abc123"


def pw_protected_view(request, *args, **kwargs):
    is_allowed = request.session.get("protected_page_allowed") or 0
    print(
        request.session.get("protected_page_allowed"),
        type(request.session.get("protected_page_allowed")),
    )
    if request.method == "POST":
        # user_pw_sent = request.POST.get("code") or None
        user_pw_sent = request.POST["code"]
        if user_pw_sent == VALID_CODE:
            is_allowed = 1
            request.session["protected_page_allowed"] = is_allowed
    if is_allowed:
        return render(request, "protected/view.html", {})
    return render(request, "protected/entry.html", {})


@login_required
def user_only_view(request, *args, **kwargs):
    return render(request, "protected/user-only.html", {})
