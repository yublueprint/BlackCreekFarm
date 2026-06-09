const addButton = document.getElementById("addButton");
const popupForm = document.getElementById("popupForm");
const closeButton = document.getElementById("closeButton");

addButton.addEventListener("click", () => {
  popupForm.classList.remove("hidden");
});

closeButton.addEventListener("click", () => {
  popupForm.classList.add("hidden");
});

// Notes popup logic (matches Supplies pattern)
const notesPopup = document.getElementById("notesPopup");
const closeNotesButton = document.getElementById("closeNotesButton");
const outputNotes = document.getElementById("notesOfCropOutput");

closeNotesButton.addEventListener("click", () => {
  notesPopup.classList.add("hidden");
});

function openNotesPopup(notesToShow) {
  outputNotes.value = notesToShow ? `${notesToShow}` : "—";
  notesPopup.classList.remove("hidden");
}

// Edit Popup Logic
const editPopup = document.getElementById("editPopup");
const closeEditButton = document.getElementById("closeEditButton");

function openEditPopup(
  id,
  name,
  crop_type,
  planting,
  harvest,
  yieldValue,
  yieldEfficiency,
  waterUsage,
  nextCheckup,
  region,
  notes
) {
  document.getElementById("editId").value = id;
  document.getElementById("editName").value = name;
  document.getElementById("editCropType").value = crop_type;
  document.getElementById("editPlantingDate").value = planting;

  // Avoid "null" in date inputs
  document.getElementById("editHarvestDate").value = harvest || "";
  document.getElementById("editNextCheckup").value = nextCheckup || "";

  document.getElementById("editExpectedYield").value = yieldValue || "";
  document.getElementById("editYieldEfficiency").value = yieldEfficiency || "0";
  document.getElementById("editWaterUsageLiters").value = waterUsage || "0";
  document.getElementById("editRegion").value = region || "";
  document.getElementById("editNotes").value = notes || "";

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
  document.getElementById("deleteCropName").textContent = name;
  deletePopup.classList.remove("hidden");
}

closeDeleteButton.addEventListener("click", () => {
  deletePopup.classList.add("hidden");
});