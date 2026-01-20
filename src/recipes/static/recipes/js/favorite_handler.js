document.addEventListener('DOMContentLoaded', () => {
    const favoriteForm = document.querySelector('.favorite-form');

    if (favoriteForm) {
        favorite.Form.addEventListener('submit', (e) => {
            e.preventDefault();

            const btn = favorite.Form.querySelector('.favorite-btn');
            const url = favoriteForm.getAttribute('action');
            const csrfToken = favoriteForm.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.is_favorited) {
                    btn.classList.add('favorited');
                    btn.textContent = 'Favorited';
                } else {
                    btn.classList.remove('favorited');
                    btn.textContent = 'Add Favorite';
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
});