from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory, Client
from django.core.exceptions import ValidationError
from django.urls import reverse
from unittest.mock import patch

from ...backend.supplies.supplies import supplies_list
from ...backend.models import Supplies


class SuppliesModelTests(TestCase):
    def test_create_supply_model(self):
        # "Cardboard Box","Storage",5,"units"
        supply = Supplies.objects.create(
            name="Cardboard Box", 
            type="Storage",
            quantity=5,
            unit="units"
            )
        self.assertEqual(Supplies.objects.count(),1)
        self.assertIsNotNone(supply)
        self.assertEqual(supply.name,"Cardboard Box")
        self.assertEqual(supply.type, "Storage")
        self.assertEqual(supply.quantity, 5)
        self.assertEqual(supply.unit,"units")

class SuppliesListClientTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_supplies_list_page(self):
        # could also just use .get(rverse(supplies_list)) but need to import the other views too if so.
        home_response = self.client.get("/supplies/")
        add_response = self.client.get("/supplies/add/")
        edit_response = self.client.get("/supplies/edit/")
        delete_response = self.client.get("/supplies/delete/")

        # Ensure they reach the url without issue.
        self.assertEqual(home_response.request['PATH_INFO'], "/supplies/")
        self.assertEqual(add_response.request['PATH_INFO'], "/supplies/add/")
        self.assertEqual(edit_response.request['PATH_INFO'], "/supplies/edit/")
        self.assertEqual(delete_response.request['PATH_INFO'], "/supplies/delete/")
        self.assertNotEqual(home_response.status_code, 404)
        self.assertNotEqual(add_response.status_code, 404)
        self.assertNotEqual(edit_response.status_code, 404)
        self.assertNotEqual(delete_response.status_code, 404)

class SuppliesListViewMockTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="testuser",password="testpass")

    @patch("app.backend.supplies.supplies.Supplies.objects.all")
    def test_supplies_list_view_with_mocked_queryset(self, mock_all):
        class MockSupply:
            def __init__(self, name, type, quantity, unit):
                self.name = name
                self.type = type
                self.quantity = quantity
                self.unit = unit

        mock_supply1 = MockSupply("Cardboard Box","Storage",5,"units")
        mock_supply2 = MockSupply("Golfgreen Organic Blood Meal Plant Food", "Fertilizer", 1.3, "kg")

        mock_all.return_value = [mock_supply1, mock_supply2]

        request = self.factory.get("/supplies/")
        request.user = self.user
        response = supplies_list(request)

        self.assertEqual(response.status_code, 200)

        # Checking mock_supply1
        self.assertIn(b"Cardboard Box", response.content)
        self.assertIn(b"Storage", response.content)
        self.assertIn(b"units", response.content)

        # Checking mock_supply2
        self.assertIn(b"Golfgreen Organic Blood Meal Plant Food", response.content)
        self.assertIn(b"Fertilizer", response.content)
        self.assertIn(b"kg", response.content)

        mock_all.assert_called_once()
