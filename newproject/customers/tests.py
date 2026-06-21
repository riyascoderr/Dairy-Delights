from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from Seller.models import sellm
from .models import buy, signinm


def create_product(**overrides):
    data = {
        "name": "Fresh Cow Milk",
        "brand": "Dairy Delights",
        "category": "Fresh Milk",
        "sku": "DD-MILK-500",
        "short_description": "Fresh 500 ml bottle",
        "description": "Pure milk delivered fresh.",
        "main_image": "images/Screenshot_2.png",
        "gallery_1": "images/Screenshot_3.png",
        "gallery_2": "images/Screenshot_4.png",
        "gallery_3": "images/Screenshot_5.png",
        "price": "45.00",
        "mrp": "52.00",
        "stock": 20,
        "stock_status": "In stock",
        "badge": "Fresh today",
        "tax_info": "Inclusive of all taxes",
        "size": "500 ml",
        "type": "Cow Milk",
        "ingredients": "Milk",
        "shelf_life": "2 days",
        "packaging": "Glass bottle",
        "allergen": "Contains milk",
        "highlights": "No preservatives",
        "delivery_area": "Srinagar",
        "delivery_slot": "Morning",
        "return_policy": "Replacement available",
        "business_minimum": "10 bottles",
        "slug": "fresh-cow-milk",
    }
    data.update(overrides)
    return sellm.objects.create(**data)


class CustomerFlowTests(TestCase):
    def setUp(self):
        self.product = create_product()
        self.user = User.objects.create_user(
            username="customer@example.com",
            password="pass12345",
        )
        self.customer = signinm.objects.create(
            name="Customer",
            email="customer@example.com",
            phone="9876543210",
            address="Srinagar",
        )

    def test_public_pages_render(self):
        for url_name in ["home", "products", "sell"]:
            response = self.client.get(reverse(url_name))
            self.assertEqual(response.status_code, 200)

    def test_product_detail_renders_and_missing_product_is_404(self):
        response = self.client.get(reverse("product", args=[self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

        response = self.client.get(reverse("product", args=["missing-product"]))
        self.assertEqual(response.status_code, 404)

    def test_customer_signup_creates_account_and_profile(self):
        response = self.client.post(
            reverse("customers:signin"),
            {
                "name": "New Customer",
                "email": "new@example.com",
                "phone": "9876543211",
                "address": "Budgam",
                "password": "pass12345",
            },
        )

        self.assertRedirects(response, reverse("products"))
        self.assertTrue(User.objects.filter(username="new@example.com").exists())
        self.assertTrue(signinm.objects.filter(email="new@example.com").exists())

    def test_cart_requires_login(self):
        response = self.client.get(reverse("customers:cart"))
        self.assertRedirects(response, reverse("home"))

    def test_authenticated_customer_can_add_view_and_delete_cart_item(self):
        self.client.login(username="customer@example.com", password="pass12345")

        response = self.client.post(
            reverse("customers:cart"),
            {"sku": self.product.sku, "next": "products"},
        )
        self.assertRedirects(response, reverse("products"))

        self.customer.refresh_from_db()
        self.assertEqual(self.customer.cart, 1)
        self.assertEqual(self.customer.items, [self.product.sku])

        self.customer.items = [self.product.sku, "STALE-SKU"]
        self.customer.cart = 2
        self.customer.save()

        response = self.client.get(reverse("customers:cart"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

        response = self.client.post(
            reverse("customers:cart"),
            {"sku": self.product.sku, "action": "delete"},
        )
        self.assertRedirects(response, reverse("customers:cart"))

        self.customer.refresh_from_db()
        self.assertEqual(self.customer.items, ["STALE-SKU"])

    def test_buy_form_saves_order(self):
        response = self.client.post(
            reverse("customers:buy"),
            {
                "add": "Srinagar",
                "order": "One-time order",
                "quantity": "1 bottle",
            },
        )

        self.assertRedirects(response, reverse("products"))
        self.assertEqual(buy.objects.count(), 1)
