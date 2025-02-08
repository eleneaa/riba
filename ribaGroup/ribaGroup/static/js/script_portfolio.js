document.querySelectorAll('.image-gallery').forEach((gallery) => {
    let currentImageIndex = 0;
    const images = gallery.querySelectorAll('.image-container');

    function showImage(index) {
        images.forEach((img, i) => {
            img.classList.remove('active');
            if (i === index) {
                img.classList.add('active');
            }
        });
    }

    gallery.querySelector('.prev').addEventListener('click', () => {
        currentImageIndex = (currentImageIndex - 1 + images.length) % images.length;
        showImage(currentImageIndex);
    });

    gallery.querySelector('.next').addEventListener('click', () => {
        currentImageIndex = (currentImageIndex + 1) % images.length;
        showImage(currentImageIndex);
    });

    // Инициализация - показываем первое изображение
    showImage(currentImageIndex);
});
