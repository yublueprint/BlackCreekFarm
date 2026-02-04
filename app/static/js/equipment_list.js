const addButton = document.getElementById("addButton");
const popupForm = document.getElementById("popupForm");
const closeButton = document.getElementById("closeButton");


addButton.addEventListener("click", () => {
    popupForm.classList.remove("hidden");
});

closeButton.addEventListener("click", () => {
    popupForm.classList.add("hidden");
});

const editPopup = document.getElementById("editPopup");
const closeEditButton = document.getElementById("closeEditButton");

function openEditPopup(id, name, category, type, serial_number, purchase_date, maintenance_due, next_checkup, warranty_expiry, location, supplier, hours_used, condition, purchase_cost, active, last_service_by, service_interval_days, maintenance_history, notes) {
    document.getElementById("editId").value = id;
    document.getElementById("editName").value = name;
    document.getElementById("editCategory").value = category;
    document.getElementById("editType").value = type;
    document.getElementById("editSerialNumber").value = serial_number;
    document.getElementById("editPurchaseDate").value = purchase_date;
    document.getElementById("editMaintenanceDate").value = maintenance_due;
    document.getElementById("editNextCheckup").value = next_checkup;
    document.getElementById("editWarrantyExpiry").value = warranty_expiry;
    document.getElementById("editLocation").value = location;
    document.getElementById("editSupplier").value = supplier;
    document.getElementById("editHoursUsed").value = hours_used;
    document.getElementById("editCondition").value = condition;
    document.getElementById("editPurchaseCost").value = purchase_cost;
    document.getElementById("editActive").value = active;
    document.getElementById("editLastServiceBy").value = last_service_by;
    document.getElementById("editServiceInterval").value = service_interval_days;
    document.getElementById("editMaintenanceHistory").value = maintenance_history;
    document.getElementById("editNotes").value = notes;
    editPopup.classList.remove("hidden");
}

closeEditButton.addEventListener("click", () => {
    editPopup.classList.add("hidden");
});

// Delete Popup Logic
const deletePopup = document.getElementById("deletePopup");
const closeDeleteButton = document.getElementById("closeDeleteButton");

function openDeletePopup(id, name) {
    document.getElementById("deleteId").value = id;
    document.getElementById("deleteEquipmentName").textContent = name;
    deletePopup.classList.remove("hidden");
}

closeDeleteButton.addEventListener("click", () => {
    deletePopup.classList.add("hidden");
});