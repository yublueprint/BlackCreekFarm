// ---------- Add Popup ----------
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

function handleEditClick(btn) {
  // pull values from data-* attributes
  const id = btn.dataset.id || "";
  const name = btn.dataset.name || "";
  const category = btn.dataset.category || "";
  const type = btn.dataset.type || "";
  const purchase = btn.dataset.purchase || "";
  const maintenance = btn.dataset.maintenance || "";
  const notes = btn.dataset.notes || "";

  const setVal = (id, value) => {
    const el = document.getElementById(id);
    if (el) el.value = value;
  };

  setVal("editId", id);
  setVal("editName", name);
  setVal("editCategory", category);
  setVal("editType", type);
  setVal("editPurchaseDate", purchase);
  setVal("editMaintenanceDate", maintenance);
  setVal("editNotes", notes);

  if (editPopup) editPopup.classList.remove("hidden");
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
  const idEl = document.getElementById("deleteId");
  const nameEl = document.getElementById("deleteEquipmentName");

  if (idEl) idEl.value = id;
  if (nameEl) nameEl.textContent = name;

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

// ---------- Optional: close popups when clicking the dark overlay ----------
[popupForm, editPopup, deletePopup, notesPopup].forEach((popup) => {
  if (!popup) return;
  popup.addEventListener("click", (e) => {
    if (e.target === popup) popup.classList.add("hidden");
  });
});