import pathlib
from django.shortcuts import render
from django.http import HttpResponse

from visits.models import PageVisit

this_dir = pathlib.Path(__file__).resolve().parent


def home_page_view(request, *args, **kwargs):
    PageVisit.objects.create(path=request.path)
    qs = PageVisit.objects.all()
    page_qs = PageVisit.objects.filter(path=request.path)
    path = request.path
    my_title = "My Page"
    my_context = {
        "page_title": my_title,
        "page_visit_count": page_qs.count(),
        "percent": f"{(page_qs.count() * 100.0) / qs.count():.2f}",
        "total_visit_count": qs.count(),
    }
    html_template = "home.html"

    return render(request, html_template, my_context)


def about_page_view(request, *args, **kwargs):
    my_title = "My Page"
    my_context = {
        "page_title": my_title,
    }
    html_ = ""
    return HttpResponse(html_)
