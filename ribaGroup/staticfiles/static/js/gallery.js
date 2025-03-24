let currentIndex = 0;
let images = []; // Оставляем здесь, чтобы потом инициализировать из HTML

function changeImage(direction) {
    currentIndex = (currentIndex + direction + images.length) % images.length;
    document.getElementById("currentImage").src = images[currentIndex];
}

function setImages(imageArray) {
    images = imageArray; // Устанавливаем переданный массив изображений
    if (images.length > 0) {
        document.getElementById("currentImage").src = images[0]; // Устанавливаем первое изображение
    }
}

// Ждем полной загрузки страницы
document.addEventListener("DOMContentLoaded", function() {
    setImages(images); // Функция будет вызвана, когда DOM полностью загружен
});
