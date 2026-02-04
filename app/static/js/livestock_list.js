const addButton = document.getElementById("addButton");
const popupForm = document.getElementById("popupForm");
const closeButton = document.getElementById("closeButton");

addButton.addEventListener("click", () => {
    popupForm.classList.remove("hidden");
});

closeButton.addEventListener("click", () => {
    popupForm.classList.add("hidden");
});

// Logic for Edit Popup this is to display the edit popup with pre-filled data from the row which we are editing
const editPopup = document.getElementById("editPopup");
const closeEditButton = document.getElementById("closeEditButton");

function openEditPopup(id, name, breed, age, weight, healthStatus, purchasePrice, currentValue, vaccinationDate, notes) {
    document.getElementById("editId").value = id;
    document.getElementById("editName").value = name;
    document.getElementById("editBreed").value = breed;
    document.getElementById("editAge").value = age;
    document.getElementById("editWeight").value = weight;
    document.getElementById("editHealthStatus").value = healthStatus;
    document.getElementById("editPurchasePrice").value = purchasePrice;
    document.getElementById("editCurrentValue").value = currentValue;
    document.getElementById("editNextVaccinationDate").value = vaccinationDate;
    document.getElementById("editNotes").value = notes;
    editPopup.classList.remove("hidden");
}

closeEditButton.addEventListener("click", () => {
    editPopup.classList.add("hidden");
});


//Logic for Delete Popup
const deletePopup = document.getElementById("deletePopup");
const closeDeleteButton = document.getElementById("closeDeleteButton");

function openDeletePopup(id, name) {
    document.getElementById("deleteId").value = id;
    document.getElementById("deleteName").textContent = name;
    deletePopup.classList.remove("hidden");
}

closeDeleteButton.addEventListener("click", () => {
    deletePopup.classList.add("hidden");
});