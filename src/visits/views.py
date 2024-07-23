from django.shortcuts import render

from .models import PageVisit


def home_view(request, *args, **kwargs):
    return about_view(request, *args, **kwargs)


def about_view(request, *args, **kwargs):
    PageVisit.objects.create(path=request.path)
    queryset = PageVisit.objects.all()
    page_queryset = PageVisit.objects.filter(path=request.path)
    try:
        percent = (page_queryset.count() * 100.0) / queryset.count()
    except:
        percent = 0
    my_context = {
        "page_title": "My Page",
        "page_visit_count": page_queryset.count(),
        "percent": f"{percent:.2f}",
        "total_visit_count": queryset.count(),
    }

    return render(request, "home.html", my_context)
