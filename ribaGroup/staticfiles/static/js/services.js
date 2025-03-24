// Получаем все карточки
const cards = document.querySelectorAll('.service_card');

// Добавляем обработчики событий на каждую карточку
cards.forEach(card => {
    card.addEventListener('mouseenter', () => {
        // Удаляем класс active у всех карточек
        cards.forEach(c => {
            c.classList.remove('active');
            c.classList.remove('inactive'); // Убираем inactive для всех
            c.style.transform = 'scale(0.9)'; // Уменьшаем все карточки по умолчанию
        });
        // Добавляем класс active к текущей карточке
        card.classList.add('active');
        const scale = card.getAttribute('data-scale'); // Получаем уникальный размер из атрибута
        card.style.transform = `scale(${scale})`; // Применяем уникальный размер
    });

    card.addEventListener('mouseleave', () => {
        // Убираем класс active у текущей карточки
        card.classList.remove('active');

        // Проверяем, есть ли активная карточка после mouseleave
        const activeCard = Array.from(cards).some(c => c.classList.contains('active'));
        if (!activeCard) {
            // Если нет активной карточки, убираем все классы
            cards.forEach(c => {
                c.classList.remove('inactive');
                c.style.transform = 'scale(1)'; // Возвращаем карточки к исходному размеру
            });
        }
    });
});
