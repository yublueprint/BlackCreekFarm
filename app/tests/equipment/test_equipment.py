import pytest
from django.urls import reverse

from app.backend.models import Equipment


pytestmark = pytest.mark.django_db


def test_list_success(client, user, equipment):
    response = client.get(reverse("equipment_list"))
    assert response.status_code == 200
    assert "Tractor" in response.content.decode("utf-8")


def test_add_success_required_only(client, user):
    response = client.post(
        reverse("add_equipment"),
        data={
            "name": "Generator",
            "category": "Power",
            "type": "Portable",
            "purchase_date": "",
            "maintenance_due": "",
            "notes": "",
        },
        follow=True,
    )

    assert response.status_code == 200
    assert Equipment.objects.filter(
        name="Generator",
        category="Power",
        type="Portable"
    ).exists()


def test_add_validation_failure(client, user):
    response = client.post(
        reverse("add_equipment"),
        data={
            "name": "",
            "category": "Power",
            "type": "Portable",
        },
    )

    assert response.status_code == 200
    assert "Name, Category, and Type are required." in response.content.decode("utf-8")


def test_edit_success(client, user, equipment):
    response = client.post(
        reverse("edit_equipment"),
        data={
            "id": equipment.id,
            "name": "Tractor X",
            "category": "Vehicles",
            "type": "Heavy",
            "purchase_date": "",
            "maintenance_due": "",
            "notes": "Updated notes",
        },
        follow=True,
    )

    assert response.status_code == 200

    equipment.refresh_from_db()
    assert equipment.name == "Tractor X"
    assert equipment.notes == "Updated notes"


def test_edit_validation_failure(client, user, equipment):
    response = client.post(
        reverse("edit_equipment"),
        data={
            "id": equipment.id,
            "name": "",
            "category": "Vehicles",
            "type": "Heavy",
        },
    )

    assert response.status_code == 200
    assert "Name, Category, and Type are required." in response.content.decode("utf-8")

    equipment.refresh_from_db()
    assert equipment.name == "Tractor"


def test_delete_success(client, user, equipment):
    response = client.post(
        reverse("delete_equipment"),
        data={"id": equipment.id},
        follow=True,
    )

    assert response.status_code == 200
    assert not Equipment.objects.filter(id=equipment.id).exists()


def test_delete_not_found(client, user):
    response = client.post(
        reverse("delete_equipment"),
        data={"id": 999999},
    )

    assert response.status_code == 200
    assert "Equipment not found." in response.content.decode("utf-8")


def test_add_unexpected_exception_handled(client, user, monkeypatch):
    from app.backend.equipment import equipment as equipment_module

    def boom(*args, **kwargs):
        raise Exception("DB down")

    monkeypatch.setattr(equipment_module.Equipment.objects, "create", boom)

    response = client.post(
        reverse("add_equipment"),
        data={
            "name": "X",
            "category": "Y",
            "type": "Z",
        },
    )

    assert response.status_code == 200
    assert "An unexpected error occurred while adding the equipment." in response.content.decode("utf-8")


def test_edit_unexpected_exception_handled(client, user, equipment, monkeypatch):
    from app.backend.equipment import equipment as equipment_module

    def boom(self):
        raise Exception("Save exploded")

    monkeypatch.setattr(equipment_module.Equipment, "save", boom)

    response = client.post(
        reverse("edit_equipment"),
        data={
            "id": equipment.id,
            "name": "Tractor X", 
            "category": "Vehicles",
            "type": "Heavy",
        },
    )

    assert response.status_code == 200
    assert "An unexpected error occurred while editing the equipment." in response.content.decode("utf-8")