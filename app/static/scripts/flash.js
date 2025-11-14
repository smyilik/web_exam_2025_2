document.addEventListener('DOMContentLoaded', function() {
    const flashes = document.querySelectorAll('.flash');
    
    flashes.forEach(flash => {
        // Автоматическое скрытие через 5 секунд
        const autoRemoveTimer = setTimeout(() => {
            removeFlash(flash);
        }, 5000);

        // Находим кнопку закрытия
        const closeBtn = flash.querySelector('.flash-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                clearTimeout(autoRemoveTimer); // Отменяем автоудаление
                removeFlash(flash);
            });
        }
    });
});

function removeFlash(flashElement) {
    flashElement.style.opacity = '0';
    flashElement.style.transform = 'translateY(-20px)'; // Измените на translateY
    setTimeout(() => {
        if (flashElement.parentElement) {
            flashElement.remove();
        }
    }, 300);
}