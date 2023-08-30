from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from posts.models import Post
from comments.models import Comment
from comments.serializers import CommentSerializer
from model_bakery import baker



class CommentViewSetTestCase(APITestCase):
    BASE_URL = "/api/v1/comments/"

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
        self.post_1 = baker.make(Post)
        self.post_2 = baker.make(Post)

        self.comment_1 = Comment.objects.create(
            body="This is amazing and well explained!",
            owner=self.normal_user,
            post=self.post_1
        )
        self.comment_2 = Comment.objects.create(
            body="Perfect!!",
            owner=self.super_user,
            post=self.post_2  
        )


    def tearDown(self) -> None:
        Post.objects.all().delete()
        Comment.objects.all().delete()

        self.assertEqual(Comment.objects.count(), 0)
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
    
    def test_get_all_comments(self):
        header = self._get_jwt_token(username="test_admin", password="dummy_password321")
        response = self.client.get(self.BASE_URL, headers=header).json()

        self.assertEqual(len(response), 2)

    def test_update_a_comment(self):
        header = self._get_jwt_token(username="test_admin", password="dummy_password321")
        data={
            "post": self.post_1.pk,
            "body": "Updated this comment."
        }

        post_comment_response_before = self.client.get(
            f"/api/v1/posts/{self.post_1.pk}/",
            headers=header
        ).json().get('comments')[0]

        self.assertEqual(post_comment_response_before.get('id'), self.comment_1.pk)
        self.assertEqual(post_comment_response_before.get('body'), 'This is amazing and well explained!')
        self.assertEqual(post_comment_response_before.get('owner'), self.normal_user.pk)

        response = self.client.patch(
            f"{self.BASE_URL}{self.comment_1.pk}/",
            headers=header,
            data=data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('body'), "Updated this comment.")
        self.assertEqual(Comment.objects.get(pk=self.comment_1.pk).body, "Updated this comment.")


        post_comment_response_after = self.client.get(
            f"/api/v1/posts/{self.post_1.pk}/",
            headers=header
        ).json().get('comments')[0]

        self.assertEqual(post_comment_response_after.get('body'), "Updated this comment.")


    def test_try_to_update_different_users_comment(self):
        header = self._get_jwt_token(username="normal_user", password="dummy_password321")
        data={
            "post": self.post_2.pk,
            "body": "Updated this comment."
        }
        response = self.client.put(
            f"{self.BASE_URL}{self.comment_2.pk}/",
            headers=header,
            data=data,
            format="json"
        ).json()

        self.assertEqual(response.get('detail'), 'You do not have permission to perform this action.')


    def test_try_to_update_different_users_comments_with_admin_role(self):
        header = self._get_jwt_token(username="test_admin", password="dummy_password321")
        data={
            "post": self.post_1.pk,
            "body": "Updated this comment by admin"
        }
        response = self.client.patch(
            f"{self.BASE_URL}{self.comment_1.pk}/",
            headers=header,
            data=data,
            format="json"
        ).json()

        self.assertEqual(response.get('owner'), self.normal_user.pk)
        self.assertEqual(response.get('body'), "Updated this comment by admin")
        self.assertEqual(response.get('post'), self.post_1.pk)

    def test_delete_a_comment(self):
        header = self._get_jwt_token(username="test_admin", password="dummy_password321")
        response = self.client.delete(
            f"{self.BASE_URL}{self.comment_1.pk}/", 
            headers=header
        )
       
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(pk=self.comment_1.pk).exists())

    def test_create_a_comment(self):
        header = self._get_jwt_token(username="normal_user", password="dummy_password321")
        prepared_data = CommentSerializer(
            baker.prepare(
            Comment,
            body="This is a test comment.",
            post=self.post_1
        )).data

        response = self.client.post(self.BASE_URL, data=prepared_data, headers=header, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json().get('body'), 'This is a test comment.')
        self.assertEqual(response.json().get('post'), self.post_1.pk)
        self.assertEqual(response.json().get('owner'), self.normal_user.pk)
