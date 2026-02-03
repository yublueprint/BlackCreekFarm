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

function openEditPopup(id, name, crop_type, planting, harvest, yieldValue, yieldEfficiency, waterUsage, nextCheckup, region, notes) {
    document.getElementById("editId").value = id;
    document.getElementById("editName").value = name;
    document.getElementById("editCropType").value = crop_type;
    document.getElementById("editPlantingDate").value = planting;
    document.getElementById("editHarvestDate").value = harvest;
    document.getElementById("editExpectedYield").value = yieldValue;
    document.getElementById("editYieldEfficiency").value = yieldEfficiency;
    document.getElementById("editWaterUsageLiters").value = waterUsage;
    document.getElementById("editNextCheckup").value = nextCheckup;
    document.getElementById("editRegion").value = region;
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
    document.getElementById("deleteCropName").textContent = name;
    deletePopup.classList.remove("hidden");
}

closeDeleteButton.addEventListener("click", () => {
    deletePopup.classList.add("hidden");
});