from django.http import HttpResponse
from django.test import TestCase
from django.utils.html import escape

from lists.models import Item, List


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response: HttpResponse = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response: HttpResponse = self.client.get(f"/lists/{list_.id}/")
        self.assertTemplateUsed(response, "list.html")

    def test_dispalays_all_list_items(self):
        list_ = List.objects.create()
        Item.objects.create(text="item 1", list=list_)
        Item.objects.create(text="item 2", list=list_)

        other_list = List.objects.create()
        Item.objects.create(text="other item 1", list=other_list)
        Item.objects.create(text="other item 2", list=other_list)

        response: HttpResponse = self.client.get(f"/lists/{list_.id}/")

        self.assertContains(response, "item 1")
        self.assertContains(response, "item 2")
        self.assertNotContains(response, "other item 1")
        self.assertNotContains(response, "other item 2")

    def test_passes_correct_list_to_template(self):
        List.objects.create()
        correct_list = List.objects.create()
        response: HttpResponse = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)


class NewListTest(TestCase):
    def test_can_save_post_request(self):
        self.client.post(
            "/lists/new",
            data={"item_text": "A new list item"},
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item: Item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_post(self):
        response: HttpResponse = self.client.post(
            "/lists/new",
            data={"item_text": "A new list item"},
        )
        new_list = List.objects.first()
        self.assertRedirects(response, f"/lists/{new_list.id}/")

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response: HttpResponse = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)


class NewItemTest(TestCase):
    def test_can_save_post_to_existing_list(self):
        List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={"item_text": "A new item for an existing list"},
        )

        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={"item_text": "A new item for an existing list"},
        )
        self.assertRedirects(response, f'/lists/{correct_list.id}/')
