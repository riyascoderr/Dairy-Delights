from pathlib import Path

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from Seller.models import sellm, signins
from customers.models import signinm


TEST_MEDIA_ROOT = Path(__file__).resolve().parents[1] / "media"


def test_image(name):
    return SimpleUploadedFile(
        name,
        b"GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;",
        content_type="image/gif",
    )


def product_form_data():
    return {
        "name": "Seller Fresh Milk",
        "brand": "Dairy Delights",
        "category": "Fresh Milk",
        "sku": "SELLER-MILK-500",
        "short_description": "Fresh seller milk",
        "description": "Fresh dairy uploaded by seller.",
        "main_image": test_image("seller-test-main.gif"),
        "gallery_1": test_image("seller-test-gallery-1.gif"),
        "gallery_2": test_image("seller-test-gallery-2.gif"),
        "gallery_3": test_image("seller-test-gallery-3.gif"),
        "video_url": "",
        "price": "50.00",
        "mrp": "60.00",
        "stock": "15",
        "stock_status": "In stock",
        "badge": "Seller pick",
        "tax_info": "Inclusive of all taxes",
        "size": "500 ml",
        "type": "Cow Milk",
        "ingredients": "Milk",
        "shelf_life": "2 days",
        "packaging": "Glass bottle",
        "allergen": "Contains milk",
        "highlights": "Fresh",
        "delivery_area": "Srinagar",
        "delivery_slot": "Morning",
        "return_policy": "Replacement available",
        "business_minimum": "10 bottles",
    }


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class SellerFlowTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        for path in (TEST_MEDIA_ROOT / "images").glob("seller-test-*"):
            path.unlink(missing_ok=True)

    def test_anonymous_product_upload_redirects_to_home(self):
        response = self.client.post(reverse("seller:data"), product_form_data())
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("home"), response["Location"])

    def test_seller_signup_creates_seller_customer_profile_and_logs_in(self):
        response = self.client.post(
            reverse("seller:signin"),
            {
                "seller_name": "Valley Farm",
                "email": "seller@example.com",
                "phone": "9876543210",
                "location": "Srinagar",
                "gst_number": "GST123",
                "password": "pass12345",
            },
        )

        self.assertRedirects(response, reverse("sell"))
        self.assertTrue(User.objects.filter(username="seller@example.com").exists())
        self.assertTrue(signins.objects.filter(email="seller@example.com").exists())
        self.assertTrue(signinm.objects.filter(email="seller@example.com").exists())

    def test_authenticated_seller_can_create_product(self):
        user = User.objects.create_user(
            username="seller@example.com",
            password="pass12345",
        )
        self.client.login(username="seller@example.com", password="pass12345")

        response = self.client.post(reverse("seller:data"), product_form_data())

        self.assertRedirects(response, reverse("products"))
        product = sellm.objects.get(sku="SELLER-MILK-500")
        self.assertEqual(product.seller, user)
        self.assertEqual(product.slug, "seller-fresh-milk")
