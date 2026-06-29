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

// Function for it.
function openNotesPopup(noteHeaderText="Note Popup", notesToShow) {
    // console.log(notesToShow);
    const notesPopup = document.getElementById("notesPopup");
    const closeNotesButton = document.getElementById("closeNotesButton");
    const outputNotes = document.getElementById("notesOfObjectOutput");
    const noteHeader = document.getElementById("noteHeader");
    // Button for it.
    closeNotesButton.addEventListener("click", () => {
        notesPopup.classList.add("hidden");
    });
    noteHeader.textContent = noteHeaderText;
    outputNotes.value = `${notesToShow}`;
    notesPopup.classList.remove("hidden");
}

/*
Opening QR Code Popup of a category object.
*/
let currentItemName = "";
let currentQRBase64 = "";

function openQRCodePopup(QRCodeHeaderText="QR Code Popup", category_given, id_given) {
    currentItemName = `${category_given}-${id_given}`;
    currentQRBase64 = document.getElementById(`qr-source-${id_given}`).innerText;

    const QRCodePopup = document.getElementById("qrcodePopup");
    const closeQRCodeButton = document.getElementById("closeQRCodeButton");
    const qrcodeImage = document.getElementById("qrcodeImage");
    const qrcodeHeader = document.getElementById("qrcodeHeader");
    // Button for it.
    closeQRCodeButton.addEventListener("click", () => {
        QRCodePopup.classList.add("hidden");
    });
    qrcodeHeader.textContent = QRCodeHeaderText;
    qrcodeImage.src = currentQRBase64;
    QRCodePopup.classList.remove("hidden");
}

function downloadQR() {
    const link = document.createElement('a');
    link.href = currentQRBase64;
    // Cleans up the item name to make it a safe filename
    const safeName = currentItemName.toLowerCase().replace(/[^a-z0-9]/g, '-');
    link.download = `qr-${safeName}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Action: Isolated Printable View
function printQR() {
    // Open a temporary blank window
    const printWindow = window.open('', '_blank', 'width=400,height=400');
    
    // Write an ultra-minimal HTML document containing just the image and text label
    printWindow.document.write(`
        <html>
        <head>
            <title>Print QR - ${currentItemName}</title>
            <style>
                body { 
                    font-family: sans-serif; 
                    text-align: center; 
                    padding: 40px; 
                }
                img { width: 250px; height: 250px; }
                h2 { margin-top: 15px; font-size: 20px; color: #333; }
            </style>
        </head>
        <body>
            <img src="${currentQRBase64}" />
            <h2>${currentItemName}</h2>
            <script>
                // Auto trigger print setup as soon as image loads, then self-close
                window.onload = function() {
                    window.print();
                    window.close();
                };
            <\/script>
        </body>
        </html>
    `);
    printWindow.document.close();
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
    form.querySelectorAll(`select[data-has-dropdown='N']`).forEach(select => select.value = 'None');
    form.querySelectorAll(`select[data-has-dropdown='Y']`).forEach(select => {
        select.value = 'all';
        select.dispatchEvent(new Event('change'));
    });
}

function toggleInputs(mode_id, container_id) {
    const mode = document.getElementById(mode_id).value;
    const container = document.getElementById(container_id);

    if (mode === 'range' || mode === 'highest' || mode === 'lowest') {
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
            if (element.tagName === 'INPUT' || element.tagName === 'SELECT' || element.tagName === 'TEXTAREA' || element.tagName === '') {
                if (element.type === 'checkbox') {
                    console.log(element.type, element.checked, element.value)
                    element.checked = value;
                }
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