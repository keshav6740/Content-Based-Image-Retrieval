document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;
    const testImageContainer = document.getElementById('test-image-container');
    const testImagePreview = document.getElementById('test-image-preview');
    const imageUpload = document.getElementById('image-upload');
    const searchButton = document.getElementById('search-button');
    const resetButton = document.getElementById('reset-button');
    const similarImagesContainer = document.getElementById('similar-images-container');

    // Theme toggle functionality
    themeToggle.addEventListener('click', () => {
        body.classList.toggle('dark-mode');
    });

    // Image upload functionality
    imageUpload.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                testImagePreview.src = e.target.result;
                testImagePreview.style.display = 'block';
                testImageContainer.querySelector('.upload-icon').style.display = 'none';
                searchButton.disabled = false;
            };
            reader.readAsDataURL(file);
        }
    });

    // Search functionality with API integration
    searchButton.addEventListener('click', () => {
        searchButton.disabled = true;
        searchButton.innerHTML = '<svg class="spinner" viewBox="0 0 50 50"><circle class="path" cx="25" cy="25" r="20" fill="none" stroke-width="5"></circle></svg>Searching...';

        const formData = new FormData();
        formData.append("image", imageUpload.files[0]);

        // Fetch API to send the image to the backend
        fetch('http://localhost:5000/search', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            displaySimilarImages(data.map(item => item.path));
            searchButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>Search Similar Images';
            searchButton.disabled = false;
        })
        .catch(error => {
            console.error("Error:", error);
            searchButton.innerHTML = "Search Similar Images";
            searchButton.disabled = false;
        });
    });

    // Reset functionality
    resetButton.addEventListener('click', () => {
        testImagePreview.src = '';
        testImagePreview.style.display = 'none';
        testImageContainer.querySelector('.upload-icon').style.display = 'block';
        searchButton.disabled = true;
        imageUpload.value = '';
        similarImagesContainer.innerHTML = '';
    });

    function displaySimilarImages(images) {
        similarImagesContainer.innerHTML = '';
        images.forEach((src, index) => {
            const img = document.createElement('img');
            img.src = src;
            img.alt = `Similar Image ${index + 1}`;
            img.className = 'similar-image fade-in';
            img.style.animationDelay = `${index * 0.1}s`;
            similarImagesContainer.appendChild(img);
        });
    }
});
