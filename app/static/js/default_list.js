/*
Opening notes of a category object.
*/
const notesPopup = document.getElementById("notesPopup");
const closeNotesButton = document.getElementById("closeNotesButton");
const outputNotes = document.getElementById("notesOfObjectOutput");
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

/*
For searching.
*/
const searchFilterButton = document.getElementById("searchFilterButton");
const searchFilterPopup = document.getElementById("searchFilterPopup");
const closeSearchPopupButton = document.getElementById("closeSearchFormButton");

searchFilterButton.addEventListener("click", () => {
    searchFilterPopup.classList.remove("hidden");
});

closeSearchPopupButton.addEventListener("click", () => {
    searchFilterPopup.classList.add("hidden");
});

function clearSearchFilters() {
    const form = document.getElementById("searchForm");

    form.querySelectorAll('input').forEach(input => input.value = '');
}

/*
Add, edit, and delete.
*/
// For Add.
const addButton = document.getElementById("addButton");
const popupForm = document.getElementById("popupForm");
const closeButton = document.getElementById("closeButton");

addButton.addEventListener("click", () => {
    popupForm.classList.remove("hidden");
});

closeButton.addEventListener("click", () => {
    popupForm.classList.add("hidden");
});


// For delete.
const deletePopup = document.getElementById("deletePopup");
const closeDeleteButton = document.getElementById("closeDeleteButton");

function openDeletePopup(id, name) {
    document.getElementById("deleteId").value = id;
    document.getElementById("deleteObjectName").textContent = name;
    deletePopup.classList.remove("hidden");
}

closeDeleteButton.addEventListener("click", () => {
    deletePopup.classList.add("hidden");
});

// For edit.
const editPopup = document.getElementById("editPopup");
const closeEditButton = document.getElementById("closeEditButton");
closeEditButton.addEventListener("click", () => {
    editPopup.classList.add("hidden");
});

// For edit : What needs to be manually done in each JS file.
// Example below is that for supplies.
// function openEditPopup(id, name, category, quantity, unit, last_restocked, minimum_required, cost_per_unit, procurement_date, notes) {
//     document.getElementById("editId").value = id;
//     document.getElementById("editName").value = name;
//     document.getElementById("editCategory").value = category;
//     document.getElementById("editQuantity").value = quantity;
//     document.getElementById("editUnit").value = unit;
//     document.getElementById("editLastRestocked").value = last_restocked;
//     document.getElementById("editMinimumRequired").value = minimum_required;
//     document.getElementById("editCostPerUnit").value = cost_per_unit;
//     document.getElementById("editProcurementDate").value = procurement_date;
//     document.getElementById("editNotes").value = notes;
//     editPopup.classList.remove("hidden");
// }
