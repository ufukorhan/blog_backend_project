from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from categories.models import Category
from categories.views import CategoryViewSet
from model_bakery import baker
from utils.mixins import required_test_methods


@required_test_methods(http_methods='all', class_view_set=CategoryViewSet)
class CategoryViewSetTestCase(APITestCase):
    BASE_URL = "/api/v1/categories/"

    def setUp(self) -> None:
        self.super_user = User.objects.create_superuser(
        username="test_admin",
        email="test_admin@gmail.com",
        password="dummy_password321"
    )
        self.normal_user = User.objects.create_user(
        username="normal_user",
        email="dummy@gmail.com",
        password="dummy_password321"
    )

        self.category1 = baker.make(Category, name="Python")
        self.category2 = baker.make(Category, name="Web Development")
        self.category3 = baker.make(Category, name="Django Rest Framework")

    def tearDown(self) -> None:
        Category.objects.all().delete()
        self.assertEqual(Category.objects.count(), 0)

    
    def _get_jwt_token(self, username, password) -> dict[str, str]:
        data = {
            "username": username,
            "password": password
        }
        access_token = self.client.post("/token/", data=data).json().get('access')
        header = {
            "Authorization": f"Bearer {access_token}"
        }

        return header

    def test_get_queryset(self):
        header = self._get_jwt_token(username="test_admin", password="dummy_password321")
        response = self.client.get(self.BASE_URL, headers=header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)
        expected_names = ['Python', 'Web Development', 'Django Rest Framework']

        for index, item in enumerate(response.json()):
            self.assertEqual(item.get('name'), expected_names[index])

    def test_perform_update(self):
        header = self._get_jwt_token(username="test_admin", password="dummy_password321")
        data = {
            'name': "Updated Category"
        }
        response = self.client.put(f"{self.BASE_URL}{self.category1.pk}/", data=data, headers=header)
        self.assertEqual(response.json().get('name'), 'Updated Category')
        self.category1.refresh_from_db()
        self.assertNotEqual(self.category1.name, "Python")


    def test_partial_update(self):
        header = self._get_jwt_token(username="test_admin", password="dummy_password321")
        data = {
            'name': "Updated Category"
        }
        response = self.client.patch(f"{self.BASE_URL}{self.category2.pk}/", data=data, headers=header)
        self.assertEqual(response.json().get('name'), 'Updated Category')
        self.category2.refresh_from_db()
        self.assertNotEqual(self.category2.name, "Web Development")

    def test_perform_destroy(self):
        header = self._get_jwt_token(username="test_admin", password="dummy_password321")
        response = self.client.delete(f"{self.BASE_URL}{self.category3.pk}/", headers=header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_perform_create(self):
        header = self._get_jwt_token(username="test_admin", password="dummy_password321")
        data = {
            'name': "New Category"
        }
        response = self.client.post(self.BASE_URL, data=data, headers=header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get('name'), 'New Category')
        self.assertTrue(Category.objects.filter(name='New Category').exists())

    def test_create_a_category_with_normal_user(self):
        header = self._get_jwt_token(username="normal_user", password="dummy_password321")
        data = {
            'name': "New Category"
        }
        response = self.client.post(self.BASE_URL, data=data, headers=header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Category.objects.filter(name='New Category').exists())

    def test_update_a_category_with_normal_user(self):
        header = self._get_jwt_token(username="normal_user", password="dummy_password321")
        data = {
            'name': "Updated Category"
        }
        response = self.client.put(f"{self.BASE_URL}{self.category1.pk}/", data=data, headers=header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Category.objects.filter(name='Updated Category').exists())


    def test_partial_update_with_normal_user(self):
        header = self._get_jwt_token(username="normal_user", password="dummy_password321")
        data = {
            'name': "Updated Category"
        }
        response = self.client.patch(f"{self.BASE_URL}{self.category2.pk}/", data=data, headers=header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_perform_destroy_with_normal_user(self):
        header = self._get_jwt_token(username="normal_user", password="dummy_password321")
        response = self.client.delete(f"{self.BASE_URL}{self.category3.pk}/", headers=header)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
