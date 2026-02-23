const addButton = document.getElementById("addButton");
const popupForm = document.getElementById("popupForm");
const closeButton = document.getElementById("closeButton");

/*
Opening notes of a supply.
*/
const notesPopup = document.getElementById("notesPopup");
const closeNotesButton = document.getElementById("closeNotesButton");
const outputNotes = document.getElementById("notesOfSupplyOutput");
// Button for it.
closeNotesButton.addEventListener("click", () => {
    notesPopup.classList.add("hidden");
});

// Function for it.
function openNotesPopup(notesToShow) {
    // console.log(notesToShow);
    outputNotes.value = `${notesToShow}`;
    notesPopup.classList.remove("hidden");
}




addButton.addEventListener("click", () => {
    popupForm.classList.remove("hidden");
});

closeButton.addEventListener("click", () => {
    popupForm.classList.add("hidden");
});

const editPopup = document.getElementById("editPopup");
const closeEditButton = document.getElementById("closeEditButton");

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