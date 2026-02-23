
const addButton = document.getElementById("addButton");
const popupForm = document.getElementById("popupForm");
const closeButton = document.getElementById("closeButton");

if (addButton && popupForm) {
  addButton.addEventListener("click", (e) => {
    e.preventDefault();
    popupForm.classList.remove("hidden");
  });
}

if (closeButton && popupForm) {
  closeButton.addEventListener("click", (e) => {
    e.preventDefault();
    popupForm.classList.add("hidden");
  });
}

// ---------- Edit Popup ----------
const editPopup = document.getElementById("editPopup");
const closeEditButton = document.getElementById("closeEditButton");

<<<<<<< HEAD
// NEW signature includes category + notes
function openEditPopup(id, name, category, type, purchase_date, maintenance_due, notes) {
  document.getElementById("editId").value = id;
  document.getElementById("editName").value = name;
  document.getElementById("editCategory").value = category;
  document.getElementById("editType").value = type;

  // Dates can be null/empty now
  document.getElementById("editPurchaseDate").value = purchase_date || "";
  document.getElementById("editMaintenanceDate").value = maintenance_due || "";

  // Notes optional
  const notesEl = document.getElementById("editNotes");
  if (notesEl) notesEl.value = notes || "";

  if (editPopup) editPopup.classList.remove("hidden");
=======
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
>>>>>>> origin/prod
}

if (closeEditButton && editPopup) {
  closeEditButton.addEventListener("click", (e) => {
    e.preventDefault();
    editPopup.classList.add("hidden");
  });
}

// ---------- Delete Popup ----------
const deletePopup = document.getElementById("deletePopup");
const closeDeleteButton = document.getElementById("closeDeleteButton");

function openDeletePopup(id, name) {
  document.getElementById("deleteId").value = id;
  document.getElementById("deleteEquipmentName").textContent = name;
  if (deletePopup) deletePopup.classList.remove("hidden");
}

if (closeDeleteButton && deletePopup) {
  closeDeleteButton.addEventListener("click", (e) => {
    e.preventDefault();
    deletePopup.classList.add("hidden");
  });
}

// ---------- Notes View Popup (Read-only) ----------
const notesPopup = document.getElementById("notesPopup");
const closeNotesButton = document.getElementById("closeNotesButton");

function openNotesPopup(equipmentName, notes) {
  const nameEl = document.getElementById("notesEquipmentName");
  const notesEl = document.getElementById("notesContent");

  if (nameEl) nameEl.textContent = equipmentName || "";
  if (notesEl) notesEl.textContent = notes || "—";

  if (notesPopup) notesPopup.classList.remove("hidden");
}

if (closeNotesButton && notesPopup) {
  closeNotesButton.addEventListener("click", (e) => {
    e.preventDefault();
    notesPopup.classList.add("hidden");
  });
}

// Optional: close popups when clicking the dark overlay
[popupForm, editPopup, deletePopup, notesPopup].forEach((popup) => {
  if (!popup) return;
  popup.addEventListener("click", (e) => {
    if (e.target === popup) popup.classList.add("hidden");
  });
});