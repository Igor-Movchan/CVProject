from django.test import TestCase
from django.urls import reverse
from .models import CV

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

