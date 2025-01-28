from django.test import TestCase, Client
from django.urls import reverse
from .models import AmountType, Item, ShoppingList
import json

class APITestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.amount_type = AmountType.objects.create(name="Kilograms")
        self.item = Item.objects.create(name="Apples", amount=5, amount_type=self.amount_type)
        self.shopping_list = ShoppingList.objects.create(name="Default Shopping List")
        self.shopping_list.items.add(self.item)

    def test_add_item(self):
        response = self.client.put(
            reverse('add_item'),
            data=json.dumps({
                "itemType": "Bananas",
                "expirationDate": "2025-01-01",
                "amount": 3
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Item.objects.filter(name="Bananas").exists())
        

    def test_remove_item(self):
        response = self.client.delete(
            reverse('remove_item'),
            data=json.dumps({"ID": self.item.id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Item.objects.filter(id=self.item.id).exists())

    def test_new_type(self):
        response = self.client.put(
            reverse('new_type'),
            data=json.dumps({
                "unique barcode": "12345",
                "name": "Cans",
                "amount type": "Liters"
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(AmountType.objects.filter(name="Cans").exists())

    def test_add_to_shopping_list(self):
        response = self.client.put(
            reverse('add_to_shopping_list'),
            data=json.dumps({
                "item type": "Apples",
                "amount": 2
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        updated_item = Item.objects.get(name="Apples")
        self.assertEqual(updated_item.amount, 7)

    def test_remove_from_shopping_list(self):
        response = self.client.delete(
            reverse('remove_from_shopping_list'),
            data=json.dumps({
                "itemType": "Apples",
                "amount": 5
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.shopping_list.items.filter(name="Apples").exists())

    def test_purchase_item(self):
        response = self.client.patch(
            reverse('purchase_item'),
            data=json.dumps({
                "item type": "Apples",
                "amount": 3,
                "expiration date": "2025-02-01"
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Item.objects.filter(name="Apples", amount=2).exists())
        self.assertTrue(Item.objects.filter(name="Apples", amount=3, expiration_date="2025-02-01").exists())
