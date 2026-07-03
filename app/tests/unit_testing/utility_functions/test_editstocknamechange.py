from app.backend.functions.editStockNameChange import editStockNameChange


def nameChangeExample(old_name, new_name, id_to_give):
    name_change_msg = editStockNameChange(old_name, new_name)
    test_str = (
        f"User tester edited supply: {old_name}{name_change_msg} (ID: {id_to_give})."
    )
    return test_str


class TestEditStockNameChangeFunction:
    """
    Purpose is to ensure that the function didn't change and it does what it is supposed to do.
    """

    def test_name_changed_true(self):
        old_name = "Cardboard"
        new_name = "Box"
        id_to_give = 5
        assert editStockNameChange(old_name, new_name) == " to Box"
        assert (
            nameChangeExample(old_name, new_name, id_to_give)
            == f"User tester edited supply: Cardboard to Box (ID: {id_to_give})."
        )

    def test_name_changed_false(self):
        old_name = "Cardboard"
        new_name = "Cardboard"
        id_to_give = 5
        assert editStockNameChange(old_name, new_name) == ""
        assert (
            nameChangeExample(old_name, new_name, id_to_give)
            == f"User tester edited supply: Cardboard (ID: {id_to_give})."
        )
