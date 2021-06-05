from typing import List

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from lists.models import Item


def home_page(request: HttpRequest):
    if request.method == "POST":
        Item.objects.create(text=request.POST["item_text"])
        return redirect("/lists/unique-list")
    return render(request, "home.html")


def view_list(request: HttpRequest):
    items: List[Item] = Item.objects.all()
    return render(request, "list.html", {"items": items})
