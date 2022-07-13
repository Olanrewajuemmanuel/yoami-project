import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Item

# Create your tests here.

def create_item_model(time):
    """ Helper function to create item for tests """
    price = 8.99
    return Item.objects.create(date_added=time, price=price)


class ItemModelTests(TestCase):
    def test_item_was_added_recently_to_db(self):
        """ Test returns False for date_created greater than when instance was created. """
        time = timezone.now() + datetime.timedelta(days=30)
        future_item = create_item_model(time)

        self.assertIs(future_item.was_added_recently(), False)

class StoreIndexViewTests(TestCase):
    """ Tests to check if Store index View renders correctly  """
    
    def test_view_if_no_item(self):
        """ Checks: status_code, response_content and context. """
        error_msg_if_no_item = "No items to display, please check later."
        response = self.client.get(reverse('store_main:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, error_msg_if_no_item)
        self.assertQuerysetEqual(response.context['items'], [])

class StoreItemDetailViewTest(TestCase):
    """ Tests for the item detail page. """

    def test_view_if_no_item_to_view(self):
        error_msg = "No product to view."
        new_item = create_item_model(timezone.now())

        response = self.client.get(reverse('store_main:item_detail', args=[new_item.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, error_msg)
        self.assertQuerysetEqual(response.context['items'], [])
