from django.urls import reverse
# from django.utils import timezone
#
# from .models import Tournament
from ...test.othello_test import OthelloTestCase


class TournamentsTestCase(OthelloTestCase):
    def test_help_view(self):
        response = self.client.get(reverse("tournaments:help"))
        self.assertEqual(200, response.status_code)

    def test_detail(self):
        response = self.client.get(reverse("tournaments:current"))
        self.assertEqual(200, response.status_code)

        # tournament = Tournament.objects.create(start_time=timezone.localtime())

    def test_create(self):
        response = self.client.get(reverse("tournaments:create"))
        self.assertEqual(200, response.status_code)
