from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from posts.models import Post
from categories.models import Category
from model_bakery import baker



class PostViewSetTestCase(APITestCase):
    BASE_URL = "/api/v1/posts/"

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
        for i in range(1, 11):
            baker.make(
                Post, 
                title=f"Django Rest Article {i}",
                owner=self.super_user 
            )
        self.category1 = baker.make(Category, name="Python")
        self.category2 = baker.make(Category, name="Web Development")

    def tearDown(self) -> None:
        Post.objects.all().delete()
        Category.objects.all().delete()

        self.assertEqual(Category.objects.count(), 0)
        self.assertEqual(Post.objects.count(), 0)
        

        
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
    
    def test_get_all_posts(self):
        header = self._get_jwt_token(username="test_admin", password="dummy_password321")
        response = self.client.get(self.BASE_URL, headers=header).json()

        self.assertEqual(len(response), 10)

        for i, item in enumerate(response):
            expected_title = f"Django Rest Article {len(response) - i}"  # Beklenen title
            actual_title = item.get('title')  # Gerçek title

            self.assertEqual(expected_title, actual_title, f"Title mismatch for item {i + 1}")
                
    def test_update_a_post(self):
        header = self._get_jwt_token(username="test_admin", password="dummy_password321")
        post_pk = Post.objects.last().pk
        data = {
            "title": "Updated Title"
        }
        response = self.client.patch(
            f"{self.BASE_URL}{post_pk}/", 
            headers=header,
            data=data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('title'), "Updated Title")

    def test_try_to_update_different_users_post(self):
        header = self._get_jwt_token(username="normal_user", password="dummy_password321")
        post_pk = Post.objects.last().pk
        data = {
            "title": "Updated Title"
        }
        response = self.client.patch(
            f"{self.BASE_URL}{post_pk}/", 
            headers=header,
            data=data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json().get('detail'), 
            "You do not have permission to perform this action."
        )
    
    def test_try_to_update_different_users_post_with_admin_role(self):
        header = self._get_jwt_token(username="test_admin", password="dummy_password321")
        post_pk = Post.objects.create(
            title="Java Compile Time",
            body="Dummy content", 
            owner=self.normal_user
        ).pk

        data = {
            "title": "Updated Title"
        }
        response = self.client.patch(
            f"{self.BASE_URL}{post_pk}/", 
            headers=header,
            data=data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('title'), 'Updated Title')

    def test_try_to_delete_different_users_post_with_admin_role(self):
        header = self._get_jwt_token(username="test_admin", password="dummy_password321")
        post_pk = Post.objects.create(
            title="Java Compile Time",
            body="Dummy content", 
            owner=self.normal_user
        ).pk

        response = self.client.delete(
            f"{self.BASE_URL}{post_pk}/", 
            headers=header
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(title="Java Compile Time").exists())

    def test_create_a_post_with_invalid_credentials(self):
        header = self._get_jwt_token(username="fake_user", password="dummy_password321")

        post_data = {
            "title": "Test Title",
            "body": "This is a test post.",
            "categories": [self.category1.pk]
        }

        response = self.client.post(self.BASE_URL, headers=header, data=post_data, format="json")
        self.assertEqual(
            response.json().get('detail'),
            "Given token not valid for any token type"
        )

    def test_create_a_post_with_valid_credentials(self):
        header = self._get_jwt_token(username="normal_user", password="dummy_password321")

        post_data = {
            "title": "Test Title",
            "body": "This is a test post.",
            "categories": [self.category1.pk]
        }
  
        response = self.client.post(self.BASE_URL, data=post_data, headers=header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get('title'), 'Test Title')
        self.assertEqual(response.json().get('body'), 'This is a test post.')
