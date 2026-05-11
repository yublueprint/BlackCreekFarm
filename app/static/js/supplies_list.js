function openEditPopup(id, name, category, quantity, unit, last_restocked, minimum_required, cost_per_unit, procurement_date, notes) {
    document.getElementById("editId").value = id;
    document.getElementById("editName").value = name;
    document.getElementById("editCategory").value = category;
    document.getElementById("editQuantity").value = quantity;
    document.getElementById("editUnit").value = unit;
    document.getElementById("editLastRestocked").value = last_restocked;
    document.getElementById("editMinimumRequired").value = minimum_required;
    document.getElementById("editCostPerUnit").value = cost_per_unit;
    document.getElementById("editProcurementDate").value = procurement_date;
    document.getElementById("editNotes").value = notes;
    editPopup.classList.remove("hidden");
}