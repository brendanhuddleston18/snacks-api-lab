from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Snack

class SnacksTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username="testuser1", password="pass"
        )
        testuser1.save()

        test_snack = Snack.objects.create(
            name="Pretzels",
            owner=testuser1,
            description="Salty and great",
        )
        test_snack.save()

    def test_snack_model(self):
        snack = Snack.objects.get(id=1)
        actual_owner = str(snack.owner)
        actual_name = str(snack.name)
        actual_description = str(snack.description)
        self.assertEqual(actual_owner, "testuser1")
        self.assertEqual(actual_name, "Pretzels")
        self.assertEqual(actual_description, "Salty and great")

    def test_get_snack_list(self):
        url = reverse("snack_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        things = response.data
        self.assertEqual(len(things), 1)
        self.assertEqual(things[0]["name"], "Pretzels")

    def test_get_snack_by_id(self):
        url = reverse("snack_detail", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        thing = response.data
        self.assertEqual(thing["name"], "Pretzels")

    def test_create_thing(self):
        url = reverse("snack_list")
        data = {"owner": 1, "name": "Chips", "description": "Depending on the flavor, I love them"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        snacks = Snack.objects.all()
        self.assertEqual(len(snacks), 2)
        self.assertEqual(Snack.objects.get(id=2).name, "Chips")

    def test_update_snack(self):
        url = reverse("snack_detail", args=(1,))
        data = {
            "owner": 1,
            "name": "Pretzels",
            "description": "Shaped like a bow",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        snack = Snack.objects.get(id=1)
        self.assertEqual(snack.name, data["name"])
        self.assertEqual(snack.owner.id, data["owner"])
        self.assertEqual(snack.description, data["description"])

    def test_delete_thing(self):
        url = reverse("snack_detail", args=(1,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        snacks = Snack.objects.all()
        self.assertEqual(len(snacks), 0)
