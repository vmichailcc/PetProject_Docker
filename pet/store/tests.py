from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from accounts.models import CustomUser
from .models import Product


class StoreTests(APITestCase):

    def setUp(self):
        test_user = CustomUser.objects.create(
            first_name="Mike",
            last_name="Test",
            city="Zp",
            email="test@test.com",
        )
        test_user.save()
        self.user_data = test_user
        self.user_token = Token.objects.create(user=test_user)
        test_product = Product.objects.create(
            id="8888Qwerty",
            name="Тестова картина",
            category="Тестова категорія",
            vendor_code="99As",
            price="999",
            old_price="1111",
            description="Тестовий опис продукту",
            brand="Козак",
            main_picture="https://image.hubber.pro/ea157ef450c833ef7f3265411c97d670.jpg",
        )
        test_product.save()
        self.product_data = test_product

    def test_store_list_pos(self):
        url = reverse('store_router-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_store_list_search(self):
        response = self.client.get(
            reverse('store_router-list'), {"search": "Тестова"}
        )
        assert len(response.data['results']) == 1

    def test_store_list_search_neg(self):
        response = self.client.get(
            reverse('store_router-list'), {"search": "Козак"}
        )
        assert len(response.data['results']) == 0

    def test_store_list_filter_brand_neg(self):
        response = self.client.get(
            reverse('store_router-list'), {"brand": "brand"}
        )
        assert len(response.data['results']) == 0

    def test_store_list_filter_brand_pos(self):
        response = self.client.get(
            reverse('store_router-list'), {"brand": "Козак"}
        )
        assert len(response.data['results']) == 1

    def test_store_list_filter_price_neg(self):
        response = self.client.get(
            reverse('store_router-list'), {"price": "1000"}
        )
        assert len(response.data['results']) == 0

    def test_store_list_filter_price_pos(self):
        response = self.client.get(
            reverse('store_router-list'), {"price": "999"}
        )
        assert len(response.data['results']) == 1

    def test_store_list_neg(self):
        url = reverse('store_router-list')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_action_add_like(self):
        response = self.client.post(f'/api/product/{self.product_data.pk}/add_like/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_comment_pos(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        url = reverse('comment_router-list')
        data = {
            "text_product": "8888Qwerty",
            "text": "test comment 1"
        }
        response = self.client.post(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_comment_per(self):
        url = reverse('comment_router-list')
        data = {
            "text_product": "8888Qwerty",
            "text": "test comment 1"
        }
        response = self.client.post(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_comment_neg(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        url = reverse('comment_router-list')
        data = {
            "text_product": "error",
            "text": "test comment 1"
        }
        response = self.client.post(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_order_pos(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        url = reverse('order_router-list')
        data = {
            "product": "8888Qwerty",
            "quantity": "1"
        }
        response = self.client.post(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_order_per(self):
        url = reverse('order_router-list')
        data = {
            "product": "8888Qwerty",
            "quantity": "1"
        }
        response = self.client.post(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_order_neg(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        url = reverse('order_router-list')
        data = {
            "product": "8888Qwerty",
            "quantity": "100"
        }
        response = self.client.post(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_view_owner_order_pos(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        url = reverse('order_router-list')
        data = {

        }
        response = self.client.get(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_owner_order_per(self):
        url = reverse('order_router-list')
        data = {

        }
        response = self.client.get(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_view_owner_order_neg(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        url = reverse('order_router-list')
        data = {

        }
        response = self.client.post(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_order_list_filter_status_pos(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        url = reverse('order_router-list')
        data = {
            "product": "8888Qwerty",
            "quantity": "1"
        }
        response1 = self.client.post(url, data, format('json'))

        response = self.client.get(
            reverse('store_router-list'), {"status": "new"}
        )

        assert len(response.data['results']) == 1

    def test_view_product_detail_pos(self):
        url = reverse('product_router-detail', kwargs={"pk": "8888Qwerty"})
        data = {

        }
        response = self.client.get(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_product_detail_neg(self):
        url = reverse('product_router-detail', kwargs={"pk": "1"})
        data = {

        }
        response = self.client.get(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_order_detail_pos(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        url = reverse('order_router-list')
        data = {
            "product": "8888Qwerty",
            "quantity": "1"
        }
        response = self.client.post(url, data, format('json'))
        url = reverse('order_detail_router-detail', kwargs={"pk": "2"})
        data = {

        }
        response = self.client.get(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_detail_per(self):
        url = reverse('order_router-list')
        data = {
            "product": "8888Qwerty",
            "quantity": "1"
        }
        response = self.client.post(url, data, format('json'))
        url = reverse('order_detail_router-detail', kwargs={"pk": "2"})
        data = {

        }
        response = self.client.get(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_order_detail_neg(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)

        url = reverse('order_detail_router-detail', kwargs={"pk": "404"})
        data = {

        }
        response = self.client.get(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_profile_pos(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        url = reverse('custom_user-detail', kwargs={"pk": self.user_data.pk})
        data = {

        }
        response = self.client.get(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_profile_per(self):
        url = reverse('custom_user-detail', kwargs={"pk": self.user_data.pk})
        data = {

        }
        response = self.client.get(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile_neg(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        url = reverse('custom_user-detail', kwargs={"pk": self.user_data.pk})
        data = {

        }
        response = self.client.post(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_profile_pos(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        url = reverse('custom_user-detail', kwargs={"pk": self.user_data.pk})
        data = {
            "first_name": "Boris",
            "last_name": "Jons",
            "city": "Kiev"
        }
        response = self.client.put(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_profile_per(self):
        url = reverse('custom_user-detail', kwargs={"pk": self.user_data.pk})
        data = {
            "first_name": "Boris",
            "last_name": "Jons",
            "city": "Kiev"
        }
        response = self.client.put(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_profile_pos(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        url = reverse('custom_user-detail', kwargs={"pk": self.user_data.pk})
        data = {
            "last_name": "Jons",
        }
        response = self.client.patch(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_profile_per(self):
        url = reverse('custom_user-detail', kwargs={"pk": self.user_data.pk})
        data = {
            "last_name": "Jons",
        }
        response = self.client.patch(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_mark_status_email_per(self):
        response = self.client.post(f'/api/profile/{self.user_data.pk}/mark_status_email/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_mark_status_email_pos(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.post(f'/api/profile/{self.user_data.pk}/mark_status_email/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_asd_email_pos(self):
        url = reverse('mailing_router-list')
        data = {
            "email": "test1@test1.com",
        }
        response = self.client.post(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_asd_email_neg(self):
        url = reverse('mailing_router-list')
        data = {
            "email": "tetest1.com",
        }
        response = self.client.post(url, data, format('json'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
