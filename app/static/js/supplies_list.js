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

function openEditPopup(id, name, type, quantity, unit) {
    document.getElementById("editId").value = id;
    document.getElementById("editName").value = name;
    document.getElementById("editType").value = type;
    document.getElementById("editQuantity").value = quantity;
    document.getElementById("editUnit").value = unit;
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
    document.getElementById("deleteSupplyName").textContent = name;
    deletePopup.classList.remove("hidden");
}

closeDeleteButton.addEventListener("click", () => {
    deletePopup.classList.add("hidden");
});