from django.urls import reverse

from ...test.othello_test import OthelloTestCase


class GamesTestCase(OthelloTestCase):
    def test_help_view(self):
        response = self.client.get(reverse("games:help"))
        self.assertEqual(200, response.status_code)

        self.login()
        response = self.client.get(reverse("games:help"))
        self.assertEqual(200, response.status_code)

    def test_watch(self):
        response = self.client.get(reverse("games:watch"))
        self.assertEqual(200, response.status_code)
        self.assertEqual([], list(response.context["games"]))

    def test_play(self):
        response = self.client.get(reverse("games:play"))
        self.assertEqual(200, response.status_code)
