document.addEventListener('DOMContentLoaded', function() {
    const authForm = document.querySelector('.auth-form');

    if (authForm) {
        authForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const username = authForm.querySelector('.login').value.trim();
            const password = authForm.querySelector('.password').value.trim();

            if (!username || !password) {
                alert('Пожалуйста, заполните все поля');
                return;
            }

            fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            })
            .then(response => {
                return response.json().then(data => ({ status: response.status, data }));
            })
            .then(({ status, data }) => {
                if (status === 200) {
                    alert('Вход выполнен успешно!');
                    window.location.href = '/profile';
                } else {
                    alert(data.error || 'Ошибка при входе');
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
                alert('Ошибка при входе. Попробуйте еще раз.');
            });
        });
    }
});
