def editStockNameChange(old_name, new_name) -> str:
    """
    Meant for logging of stock edit.
    Detects if there was a name change with a stock. 
    If so, it would indicate it.

    User {request.user} edited supply: {old_name} {name_change_msg} (ID: {supply.id}).
    >> editStockNameChange("Cardboard", "Box")
        returns "to Box"
        User {request.user} edited supply: Cardboard to Box (ID: {supply.id}).
    >> editStockNameChange("Cardboard", "Cardboard")
        returns ""
        User {request.user} edited supply: "Cardboard" (ID: {supply.id}). 
    """
    if old_name != new_name:
        return f" to {new_name}"
    else:
        return ""