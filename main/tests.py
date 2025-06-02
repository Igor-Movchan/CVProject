from django.test import TestCase
from django.urls import reverse
from .models import CV
from rest_framework.test import APITestCase
from rest_framework import status

class CVViewTests(TestCase):
    def setUp(self):
        CV.objects.create(
          firstname="Test",
          lastname="User",
          skills="Django, Testing",
          projects="Test Project",
          bio="Testing bio",
          contacts="test@example.com"
        )

    def test_cv_list_status_code(self):
        response = self.client.get(reverse("cv_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test User")

    def test_cv_detail_status_code(self):
        cv = CV.objects.first()
        url = reverse("cv_detail", args=[cv.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Testing bio")


class CVAPITest(APITestCase):
    def setUp(self):
        self.cv_data = {
            "firstname": "Bob",
            "lastname": "Brown",
            "skills": "Django, API",
            "projects": "Portfolio API",
            "bio": "Bio for Bob",
            "contacts": "bob@example.com"
        }
        self.cv = CV.objects.create(**self.cv_data)
        self.list_url = reverse("cv-list")
        self.detail_url = reverse("cv-detail", args=[self.cv.id])

    def test_list_cvs(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_cv(self):
        new_data = {
            "firstname": "Carol",
            "lastname": "Green",
            "skills": "Rest, Testing",
            "projects": "New Project",
            "bio": "Carol’s bio",
            "contacts": "carol@example.com"
        }
        response = self.client.post(self.list_url, new_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CV.objects.count(), 2)
        created = CV.objects.get(firstname="Carol")
        self.assertEqual(created.lastname, "Green")

    def test_retrieve_cv(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["firstname"], "Bob")

    def test_update_cv(self):
        patch_data = {"firstname": "Bobby"}
        response = self.client.patch(self.detail_url, patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cv.refresh_from_db()
        self.assertEqual(self.cv.firstname, "Bobby")

    def test_delete_cv(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CV.objects.filter(id=self.cv.id).exists())