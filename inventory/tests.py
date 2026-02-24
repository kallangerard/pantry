from django.test import TestCase
from django.urls import reverse

from .models import SKU


class SKUModelTests(TestCase):
    def test_str(self):
        sku = SKU(name="Baked Beans")
        self.assertEqual(str(sku), "Baked Beans")

    def test_optional_fields_blank(self):
        sku = SKU.objects.create(name="Plain Item")
        self.assertEqual(sku.barcode, "")
        self.assertEqual(sku.unit, "")
        self.assertEqual(sku.category, "")
        self.assertEqual(sku.description, "")


class SKUListViewTests(TestCase):
    def test_empty_list(self):
        response = self.client.get(reverse("inventory:sku-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No items yet")

    def test_list_shows_skus(self):
        SKU.objects.create(name="Pasta", category="Dry Goods")
        response = self.client.get(reverse("inventory:sku-list"))
        self.assertContains(response, "Pasta")
        self.assertContains(response, "Dry Goods")


class SKUCreateViewTests(TestCase):
    def test_get_create_form(self):
        response = self.client.get(reverse("inventory:sku-create"))
        self.assertEqual(response.status_code, 200)

    def test_create_sku(self):
        response = self.client.post(
            reverse("inventory:sku-create"),
            {"name": "Olive Oil", "unit": "ml", "category": "Oils", "description": "", "barcode": ""},
        )
        self.assertRedirects(response, reverse("inventory:sku-list"))
        self.assertTrue(SKU.objects.filter(name="Olive Oil").exists())


class SKUUpdateViewTests(TestCase):
    def setUp(self):
        self.sku = SKU.objects.create(name="Rice", unit="g")

    def test_get_edit_form(self):
        response = self.client.get(reverse("inventory:sku-update", args=[self.sku.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rice")

    def test_update_sku(self):
        response = self.client.post(
            reverse("inventory:sku-update", args=[self.sku.pk]),
            {"name": "Basmati Rice", "unit": "g", "category": "Grains", "description": "", "barcode": ""},
        )
        self.assertRedirects(response, reverse("inventory:sku-list"))
        self.sku.refresh_from_db()
        self.assertEqual(self.sku.name, "Basmati Rice")


class SKUDeleteViewTests(TestCase):
    def setUp(self):
        self.sku = SKU.objects.create(name="Expired Item")

    def test_get_delete_confirm(self):
        response = self.client.get(reverse("inventory:sku-delete", args=[self.sku.pk]))
        self.assertEqual(response.status_code, 200)

    def test_delete_sku(self):
        response = self.client.post(reverse("inventory:sku-delete", args=[self.sku.pk]))
        self.assertRedirects(response, reverse("inventory:sku-list"))
        self.assertFalse(SKU.objects.filter(pk=self.sku.pk).exists())
