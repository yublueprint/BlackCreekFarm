import pytest
from playwright.sync_api import expect

from app.backend.functions.convertDateString import convertDateString

pytestmark = pytest.mark.django_db(transaction=True)


# @pytest.mark.skip()
def test_supply_flow(
    authed_page,
    live_server,
    valid_supply_1_dict,
    valid_supply_2_dict,
    valid_supply_3_dict,
):
    """
    Test if user can log go from dashboard to supplies succesfully.
    """
    # Start from supplies list.
    authed_page.goto(live_server.url + "/supplies/")

    # Add supply and fill in FULL information.
    authed_page.get_by_role("button", name="Add Supply").click()
    authed_page.locator("#addForm").locator("input[name='name']").fill(
        valid_supply_1_dict["name"]
    )
    authed_page.locator("#addForm").locator("input[name='supply_category']").fill(
        valid_supply_1_dict["supply_category"]
    )
    authed_page.locator("#addForm").locator("input[name='quantity']").fill(
        valid_supply_1_dict["quantity"]
    )
    authed_page.locator("#addForm").locator("input[name='unit']").fill(
        valid_supply_1_dict["unit"]
    )
    authed_page.locator("#addForm").locator("input[name='minimum_required']").fill(
        valid_supply_1_dict["minimum_required"]
    )
    authed_page.locator("#addForm").locator("input[name='cost_per_unit']").fill(
        valid_supply_1_dict["cost_per_unit"]
    )
    authed_page.locator("#addForm").locator("input[name='last_restocked']").fill(
        valid_supply_1_dict["last_restocked"]
    )
    authed_page.locator("#addForm").locator("input[name='procurement_date']").fill(
        valid_supply_1_dict["procurement_date"]
    )
    authed_page.locator("#addForm").locator("textarea[name='notes']").fill(
        valid_supply_1_dict["notes"]
    )
    authed_page.get_by_role("button", name="Save").click()

    # See if its in the list.
    expect(
        authed_page.locator("#stockTable").get_by_text(valid_supply_1_dict["name"])
    ).to_be_visible()
    expect(
        authed_page.locator("#stockTable").get_by_text(
            valid_supply_1_dict["supply_category"]
        )
    ).to_be_visible()
    expect(
        authed_page.locator("#stockTable").get_by_text(valid_supply_1_dict["quantity"])
    ).to_be_visible()
    expect(
        authed_page.locator("#stockTable").get_by_text(valid_supply_1_dict["unit"])
    ).to_be_visible()
    expect(
        authed_page.locator("#stockTable").get_by_text(
            valid_supply_1_dict["minimum_required"]
        )
    ).to_be_visible()
    expect(
        authed_page.locator("#stockTable").get_by_text(
            valid_supply_1_dict["cost_per_unit"]
        )
    ).to_be_visible()
    expect(
        authed_page.locator("#stockTable").get_by_text(
            convertDateString(valid_supply_1_dict["last_restocked"])
        )
    ).to_be_visible()
    expect(
        authed_page.locator("#stockTable").get_by_text(
            convertDateString(valid_supply_1_dict["procurement_date"])
        )
    ).to_be_visible()

    # Add supply again.
    authed_page.get_by_role("button", name="Add Supply").click()
    authed_page.locator("#addForm").locator("input[name='name']").fill(
        valid_supply_2_dict["name"]
    )
    authed_page.locator("#addForm").locator("input[name='supply_category']").fill(
        valid_supply_2_dict["supply_category"]
    )
    authed_page.locator("#addForm").locator("input[name='quantity']").fill(
        valid_supply_2_dict["quantity"]
    )
    authed_page.locator("#addForm").locator("input[name='unit']").fill(
        valid_supply_2_dict["unit"]
    )
    authed_page.locator("#addForm").locator("input[name='minimum_required']").fill(
        valid_supply_2_dict["minimum_required"]
    )
    authed_page.locator("#addForm").locator("input[name='cost_per_unit']").fill(
        valid_supply_2_dict["cost_per_unit"]
    )
    authed_page.locator("#addForm").locator("input[name='last_restocked']").fill(
        valid_supply_2_dict["last_restocked"]
    )
    authed_page.locator("#addForm").locator("input[name='procurement_date']").fill(
        valid_supply_2_dict["procurement_date"]
    )
    authed_page.locator("#addForm").locator("textarea[name='notes']").fill(
        valid_supply_2_dict["notes"]
    )
    authed_page.get_by_role("button", name="Save").click()

    # See if in list.
    expect(
        authed_page.locator("#stockTable").get_by_text(valid_supply_2_dict["name"])
    ).to_be_visible()
    expect(
        authed_page.locator("#stockTable").get_by_text(
            valid_supply_2_dict["supply_category"]
        )
    ).to_be_visible()
    expect(
        authed_page.locator("#stockTable").get_by_text(valid_supply_2_dict["quantity"])
    ).to_be_visible()
    expect(
        authed_page.locator("#stockTable").get_by_text(valid_supply_2_dict["unit"])
    ).to_be_visible()
    expect(
        authed_page.locator("#stockTable").get_by_text(
            valid_supply_2_dict["minimum_required"]
        )
    ).to_be_visible()
    expect(
        authed_page.locator("#stockTable").get_by_text(
            valid_supply_2_dict["cost_per_unit"]
        )
    ).to_be_visible()
    expect(
        authed_page.locator("#stockTable").get_by_text(
            convertDateString(valid_supply_2_dict["last_restocked"])
        )
    ).to_be_visible()
    expect(
        authed_page.locator("#stockTable").get_by_text(
            convertDateString(valid_supply_2_dict["procurement_date"])
        )
    ).to_be_visible()

    # Test Search Filtering.
    authed_page.locator("#searchFilterButton").click()
    # Fill in some inputs and see if clear filters works as intended.
    authed_page.locator("#searchForm").locator("#idSearch").fill("67")
    authed_page.locator("#searchForm").locator("#nameSearch").fill(
        valid_supply_1_dict["name"][:-1]
    )
    authed_page.locator("#searchForm").locator("#categorySearch").fill(
        valid_supply_1_dict["supply_category"][:-1]
    )
    authed_page.locator("#searchForm").locator("#id_qty_mode").select_option(
        value="range"
    )
    authed_page.locator("#searchForm").locator("#qty_inputs_container").is_visible()
    authed_page.locator("#searchForm").locator("#clearAllSearchFiltersButton").click()
    assert authed_page.locator("#searchForm").locator("#idSearch").input_value() == ""
    assert authed_page.locator("#searchForm").locator("#nameSearch").input_value() == ""
    assert (
        authed_page.locator("#searchForm").locator("#categorySearch").input_value()
        == ""
    )
    assert (
        authed_page.locator("#searchForm").locator("#id_qty_mode").input_value()
        == "all"
    )
    # Fill in an input such as name and see if search filter works.
    authed_page.locator("#searchForm").locator("#nameSearch").fill(
        valid_supply_1_dict["name"][:-1]
    )
    authed_page.get_by_role("button", name="Apply Filters").click()
    expect(
        authed_page.locator("#stockTable").get_by_text(valid_supply_1_dict["name"])
    ).to_be_visible()
    expect(
        authed_page.locator("#stockTable").get_by_text(valid_supply_2_dict["name"])
    ).not_to_be_visible()

    # Edit supply.
    authed_page.get_by_role("button", name="Edit").click()
    authed_page.locator("#editForm").locator("input[name='name']").fill(
        valid_supply_3_dict["name"]
    )
    authed_page.locator("#editForm").locator("input[name='supply_category']").fill(
        valid_supply_3_dict["supply_category"]
    )
    authed_page.locator("#editForm").locator("input[name='quantity']").fill(
        valid_supply_3_dict["quantity"]
    )
    authed_page.locator("#editForm").locator("input[name='unit']").fill(
        valid_supply_3_dict["unit"]
    )
    authed_page.locator("#editForm").locator("input[name='minimum_required']").fill(
        valid_supply_3_dict["minimum_required"]
    )
    authed_page.locator("#editForm").locator("input[name='cost_per_unit']").fill(
        valid_supply_3_dict["cost_per_unit"]
    )
    authed_page.locator("#editForm").locator("input[name='last_restocked']").fill(
        valid_supply_3_dict["last_restocked"]
    )
    authed_page.locator("#editForm").locator("input[name='procurement_date']").fill(
        valid_supply_3_dict["procurement_date"]
    )
    authed_page.locator("#editForm").locator("textarea[name='notes']").fill(
        valid_supply_3_dict["notes"]
    )
    authed_page.get_by_role("button", name="Save").click()

    # See if changes are in the list.
    expect(
        authed_page.locator("#stockTable").get_by_text(valid_supply_3_dict["name"])
    ).to_be_visible()
    expect(
        authed_page.locator("#stockTable").get_by_text(
            valid_supply_3_dict["supply_category"]
        )
    ).to_be_visible()
    expect(
        authed_page.locator("#stockTable").get_by_text(valid_supply_3_dict["quantity"])
    ).to_be_visible()
    expect(
        authed_page.locator("#stockTable").get_by_text(
            valid_supply_3_dict["minimum_required"]
        )
    ).to_be_visible()
    expect(
        authed_page.locator("#stockTable").get_by_text(
            valid_supply_3_dict["cost_per_unit"]
        )
    ).to_be_visible()
    expect(
        authed_page.locator("#stockTable").get_by_text(
            convertDateString(valid_supply_3_dict["last_restocked"])
        )
    ).to_be_visible()
    expect(
        authed_page.locator("#stockTable").get_by_text(
            convertDateString(valid_supply_3_dict["procurement_date"])
        )
    ).to_be_visible()

    # Delete supply.
    while (
        authed_page.locator("#stockTable").get_by_role("button", name="Delete").count()
        > 0
    ):
        # print(f"Remaining database objects: {Supplies.objects.count()}")

        authed_page.locator("#stockTable").get_by_role(
            "button", name="Delete"
        ).first.click()

        confirm_btn = authed_page.locator("#deletePopup #deleteObjectForm").get_by_role(
            "button", name="Delete"
        )
        confirm_btn.wait_for(state="visible")
        confirm_btn.click()

        # If animations are added, you can use timeout.
        # authed_page.wait_for_timeout(500)

    # See if it's gone now.
    expect(
        authed_page.locator("#stockTable").get_by_text(valid_supply_1_dict["name"])
    ).not_to_be_visible()
    expect(
        authed_page.locator("#stockTable").get_by_text(valid_supply_2_dict["name"])
    ).not_to_be_visible()
    expect(
        authed_page.locator("#stockTable").get_by_text(valid_supply_3_dict["name"])
    ).not_to_be_visible()
    expect(
        authed_page.locator("#stockTable").get_by_text("No supply records")
    ).to_be_visible()
