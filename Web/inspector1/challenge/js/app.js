function wireReactions() {
    const buttons = document.querySelectorAll('.reaction-btn');

    buttons.forEach((button) => {
        button.addEventListener('click', () => {
            const countSpan = button.querySelector('.reaction-count');
            if (!countSpan) return;

            const current = parseInt(countSpan.textContent, 10) || 0;
            countSpan.textContent = current + 1;
        });
    });
}

wireReactions();
