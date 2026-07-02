let currentImageIndex = 0;
const carouselImages = document.getElementById('carouselImages');
const images = carouselImages.getElementsByTagName('img');

function moveCarousel(direction) {
    currentImageIndex += direction;
    if (currentImageIndex >= images.length) {
        currentImageIndex = 0;
    }
    if (currentImageIndex < 0) {
        currentImageIndex = images.length - 1;
    }
    const offset = -currentImageIndex * 100;
    carouselImages.style.transform = `translateX(${offset}%)`;
}

// Function to handle tabs
function openTab(event, tabName) {
    // Hide all tab contents
    const tabContents = document.getElementsByClassName('tab-content');
    for (let i = 0; i < tabContents.length; i++) {
        tabContents[i].classList.remove('active');
    }

    // Deactivate all tab buttons
    const tabButtons = document.getElementsByClassName('tab-btn');
    for (let i = 0; i < tabButtons.length; i++) {
        tabButtons[i].classList.remove('active');
    }

    // Show the current tab and activate the button
    document.getElementById(tabName).classList.add('active');
    event.currentTarget.classList.add('active');
}