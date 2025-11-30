document.addEventListener('DOMContentLoaded', function() {
    const profileForm = document.getElementById('profileForm');
    const passwordForm = document.getElementById('passwordForm');
    const logoutBtn = document.getElementById('logoutBtn');

    // Загрузка данных пользователя (пример - можно получать с сервера)
    function loadUserData() {
        // В реальном приложении здесь будет запрос к серверу
        const userData = JSON.parse(localStorage.getItem('userData') || '{}');
        
        if (userData.username) {
            document.getElementById('username').value = userData.username;
        }
        if (userData.city) {
            document.getElementById('city').value = userData.city;
        }
        if (userData.district) {
            document.getElementById('district').value = userData.district;
        }
        if (userData.age) {
            document.getElementById('age').value = userData.age;
        }
    }

    // Сохранение данных профиля
    profileForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = {
            username: document.getElementById('username').value.trim(),
            city: document.getElementById('city').value.trim(),
            district: document.getElementById('district').value.trim(),
            age: document.getElementById('age').value.trim()
        };

        if (!formData.city || !formData.district) {
            alert('Пожалуйста, заполните все обязательные поля');
            return;
        }

        // В реальном приложении здесь будет отправка на сервер
        const userData = JSON.parse(localStorage.getItem('userData') || '{}');
        Object.assign(userData, formData);
        localStorage.setItem('userData', JSON.stringify(userData));

        alert('Данные успешно сохранены!');
        console.log('Profile data:', formData);
    });

    // Изменение пароля
    passwordForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const currentPassword = document.getElementById('currentPassword').value;
        const newPassword = document.getElementById('newPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;

        if (!currentPassword || !newPassword || !confirmPassword) {
            alert('Пожалуйста, заполните все поля');
            return;
        }

        if (newPassword !== confirmPassword) {
            alert('Новые пароли не совпадают');
            return;
        }

        if (newPassword.length < 6) {
            alert('Пароль должен содержать минимум 6 символов');
            return;
        }

        // В реальном приложении здесь будет отправка на сервер
        alert('Пароль успешно изменен!');
        console.log('Password change requested');
        
        // Очистка формы
        passwordForm.reset();
    });

    // Выход из аккаунта
    logoutBtn.addEventListener('click', function() {
        if (confirm('Вы уверены, что хотите выйти?')) {
            // В реальном приложении здесь будет запрос на сервер для выхода
            localStorage.removeItem('userData');
            localStorage.removeItem('authToken');
            
            // Перенаправление на страницу входа
            window.location.href = '/resources/templates/auth/auth.html';
        }
    });

    // Загрузка данных при загрузке страницы
    loadUserData();
});
