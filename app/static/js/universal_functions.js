function urlButtonStyling(elementId) {
    const urlBtn = document.getElementById(elementId);
    const originalText = urlBtn.textContent;

    const originalBackgroundColor = 'bg-green-800';
    const originalTextColor = 'text-white';
    const originalHoverColor = 'hover:bg-green-700';
    const loadingBackgroundColor = 'bg-[#f0f7f1]';
    const loadingTextColor = 'text-[#335D43]';

    // Do the loading styling.
    urlBtn.textContent = 'Loading, please wait...';
    urlBtn.disabled = true;
    urlBtn.classList.remove(originalBackgroundColor, originalTextColor, originalHoverColor);
    urlBtn.classList.add(loadingBackgroundColor, loadingTextColor, 'pointer-events-none');

    setTimeout(() => {
        // Restore original styling.
        urlBtn.textContent = originalText;
        urlBtn.disabled = false;
        urlBtn.classList.remove(loadingBackgroundColor, loadingTextColor, 'pointer-events-none');
        urlBtn.classList.add(originalBackgroundColor, originalTextColor, originalHoverColor);
    }, 3000);
}