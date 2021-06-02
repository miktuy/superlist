from django.http import HttpResponse
from django.test import TestCase

from lists.models import Item


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response: HttpResponse = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_can_save_post_request(self):
        self.client.post(
            '/',
            data={'item_text': 'A new list item'},
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item: Item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_post(self):
        response: HttpResponse = self.client.post(
            '/',
            data={'item_text': 'A new list item'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_dispalays_all_list_items(self):
        Item.objects.create(text='item 1')
        Item.objects.create(text='item 2')

        response: HttpResponse = self.client.get('/')
        self.assertIn('item 1', response.content.decode())
        self.assertIn('item 2', response.content.decode())


class ItemModelTest(TestCase):
    def test_saving_and_retreiving_items(self):
        first_item: Item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item: Item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')