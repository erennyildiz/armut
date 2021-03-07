from django.test import TestCase

import json

from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class UserRegistrationAPIViewTestCase(APITestCase):
    url = reverse("register")

    def test_user_registration(self):
        """
        Test to verify that a post call with user valid data
        """
        user_data = {
            "username": "testuser",
            "email": "test@testuser.com",
            "password": "123123"
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(200, response.status_code)
        self.assertTrue("token" in json.loads(response.content))

    def test_unique_username_validation(self):
        """
        Test to verify that a post call with already exists username
        """
        user_data_1 = {
            "username": "testuser",
            "email": "test@testuser.com",
            "password": "123123"
        }
        response = self.client.post(self.url, user_data_1)
        self.assertEqual(200, response.status_code)

        user_data_2 = {
            "username": "testuser",
            "email": "test2@testuser.com",
            "password": "123123"
        }
        response = self.client.post(self.url, user_data_2)
        self.assertEqual(400, response.status_code)


class UserLoginAPIViewTestCase(APITestCase):
    url = reverse("login")

    def setUp(self):
        self.username = "eren"
        self.email = "eren@armut.com"
        self.password = "Pass1234"
        self.user = User.objects.create_user(self.username, self.email, self.password)

    def test_authentication_without_password(self):
        response = self.client.post(self.url, {"username": "eren"})
        self.assertEqual(400, response.status_code)

    def test_authentication_with_wrong_password(self):
        response = self.client.post(self.url, {"username": self.username, "password": "12345"})
        self.assertEqual(400, response.status_code)

    def test_authentication_with_valid_data(self):
        response = self.client.post(self.url, {"username": self.username, "password": self.password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("token" in json.loads(response.content))

class MessageAPIViewTestCase(APITestCase):
    url = reverse("message")

    def setUp(self):
        self.username = "eren"
        self.email = "eren@armut.com"
        self.password = "Pass1234"
        self.user = User.objects.create_user(self.username, self.email, self.password)

        self.username2 = "erenyildiz"
        self.email2 = "erenyildiz@armut.com"
        self.password2 = "12345"
        self.user2 = User.objects.create_user(self.username2, self.email2, self.password2)

        self.username3 = "erenyildizz"
        self.email3 = "erenyildizz@armut.com"
        self.password3 = "123456"
        self.user3 = User.objects.create_user(self.username3, self.email3, self.password3)

        self.client.post(reverse("block"), {"blocker_name":self.username3, "blocked_name":self.username})

    def test_valid_username_message(self):
        response = self.client.post(self.url, {"sender_name": self.username, "receiver_name":self.username2, "message_detail":"Hi"})
        self.assertEqual(201, response.status_code)

    def test_wrong_username_message(self):
        response = self.client.post(self.url, {"sender_name":self.username, "receiver_name":"nobody", "message_detail":"Wrong person"})
        self.assertEqual(400, response.status_code)

    def test_block_user_message(self):
        response = self.client.post(self.url, {"sender_name": self.username, "receiver_name":self.username3, "message_detail":"Hi"})
        print(response)
        self.assertEqual(200, response.status_code)
