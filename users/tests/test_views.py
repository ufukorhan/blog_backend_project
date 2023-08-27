from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class UserViewSetTestCase(APITestCase):
    BASE_URL = "/api/v1/users/"

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


    def tearDown(self):
        User.objects.all().delete()
        self.assertEqual(User.objects.count(), 0)

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
        

    def test_get_users(self):
        header = self._get_jwt_token(username="test_admin", password="dummy_password321")
        response = self.client.get(self.BASE_URL, headers=header).json()

        self.assertEqual(response[0]['username'], "test_admin")
        self.assertEqual(response[1]['username'], "normal_user")     

    def test_get_users_without_token(self):
        response = self.client.get(self.BASE_URL).json()
        self.assertEqual(response['detail'], "Authentication credentials were not provided.")

    def test_get_users_with_normal_user(self):
        header = self._get_jwt_token(username="normal_user", password="dummy_password321")
        response = self.client.get(self.BASE_URL, headers=header).json()

        self.assertEqual(response[0]['username'], "test_admin")
        self.assertEqual(response[1]['username'], "normal_user")

    def test_create_a_user_with_super_user(self):
        header = self._get_jwt_token(username="test_admin", password="dummy_password321")
        data = {
            "username": "new_user",
            "password": "new_dummy_pass"
        }
        response = self.client.post(self.BASE_URL, data= data, headers=header, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get('username'), "new_user")

    def test_create_a_user_with_normal_user(self):
        header = self._get_jwt_token(username="normal_user", password="dummy_password321")
        data = {
            "username": "new_user",
            "password": "new_dummy_pass"
        }
        response = self.client.post(self.BASE_URL, data= data, headers=header, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json().get('detail'), "You do not have permission to perform this action.")

    def test_try_to_update_different_user_information_with_normal_user(self):
        header = self._get_jwt_token(username="normal_user", password="dummy_password321")
        data = {
            "username": "updated_username"
        }
        response = self.client.put(
            f"{self.BASE_URL}{self.super_user.pk}/",
            data= data, 
            headers=header,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json().get('detail'), "You do not have permission to perform this action.")

    def test_try_to_update_different_user_information_with_super_user(self):
        header = self._get_jwt_token(username="test_admin", password="dummy_password321")
        data = {
            "username": "updated_username"
        }
        response = self.client.put(
            f"{self.BASE_URL}{self.normal_user.pk}/",
            data= data, 
            headers=header,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('username'), "updated_username")

    def test_try_to_delete_a_user_with_super_user(self):
        header = self._get_jwt_token(username="test_admin", password="dummy_password321")
        user_pk = self.normal_user.pk
        response = self.client.delete(
            f"{self.BASE_URL}{user_pk}/",
            headers=header,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(username=user_pk).exists())

    def test_try_to_update_own_username(self):
        user_pk = self.normal_user.pk
        header = self._get_jwt_token(username="normal_user", password="dummy_password321")
        data = {
            "username": "new_user"
        }
        response = self.client.patch(
            f"{self.BASE_URL}{user_pk}/",
            data= data, 
            headers=header, 
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('username'), "new_user")
