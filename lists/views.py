from typing import List as TList

from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from lists.models import Item, List


def home_page(request: HttpRequest):
    return render(request, "home.html")


def view_list(request: HttpRequest, list_id: str):
    list_: List = List.objects.get(id=list_id)
    Item.objects.filter(list=list_)
    return render(request, "list.html", {"list": list_})


def new_list(request: HttpRequest):
    list_ = List.objects.create()
    item = Item.objects.create(text=request.POST["item_text"], list=list_)
    try:
        item.full_clean()
    except ValidationError:
        error = "You can't have an empty list item"
        return render(request, 'home.html', {"error": error})
    return redirect(f"/lists/{list_.id}/")


def add_item(request: HttpRequest, list_id: str):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(
        text=request.POST['item_text'],
        list=list_,
    )
    return redirect(f'/lists/{list_.id}/')
