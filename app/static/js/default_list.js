/*
Form validation.
*/
function limitInputLength(element) {
    if (element.value.length > element.maxLength) {
        element.value = element.value.slice(0, element.maxLength);
    }
}

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

function toggleInputs(mode_id, container_id) {
    const mode = document.getElementById(mode_id).value;
    const container = document.getElementById(container_id);

    if (mode === 'range') {
        container.style.display = 'block';
    } else {
        container.style.display = 'none';
        container.querySelectorAll('input').forEach(i => i.value = '');
    }
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

function openDeletePopup(id, name="item") {
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

function openEditPopup(...pairs) {
    pairs.forEach(([elementId, value]) => {
        const element = document.getElementById(elementId);
        
        if (element) {
            // Check if it's an input/select or just a text container
            if (element.tagName === 'INPUT' || element.tagName === 'SELECT' || element.tagName === 'TEXTAREA') {
                element.value = value;
            } else {
                element.textContent = value;
            }
        } else {
            console.warn(`Element with ID "${elementId}" not found.`);
        }
    });

    if (editPopup) editPopup.classList.remove('hidden');
}