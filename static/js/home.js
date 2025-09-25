// Get modal elements
const modal = document.getElementById('createListingModal');
const modalOverlay = document.getElementById('modalOverlay');
const createListingBtn = document.getElementById('createListingBtn');
const closeModalBtn = document.getElementById('closeModalBtn');

// Show the modal
createListingBtn.addEventListener('click', () => {
    modal.classList.add('active');
    modalOverlay.classList.add('active');
});

// Hide the modal
closeModalBtn.addEventListener('click', () => {
    modal.classList.remove('active');
    modalOverlay.classList.remove('active');
});

// Hide the modal when clicking outside of it
modalOverlay.addEventListener('click', () => {
    modal.classList.remove('active');
    modalOverlay.classList.remove('active');
});

// Optional: Close modal with Escape key
document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && modal.classList.contains('active')) {
        modal.classList.remove('active');
        modalOverlay.classList.remove('active');
    }
});
