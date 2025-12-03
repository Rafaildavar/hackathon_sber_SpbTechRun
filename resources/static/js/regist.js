document.addEventListener('DOMContentLoaded', function() {
  const nextStepBtn = document.getElementById('nextStepBtn');
  const step1Form = document.getElementById('step1Form');
  const step2Form = document.getElementById('step2Form');
  const step1Content = document.querySelector('.step-1');
  const step2VisualContent = document.querySelector('.step-2-visual-content');
  const step1Visual = document.querySelector('.step-1-visual');
  const step2FormContent = document.querySelector('.step-2-form-content');

  // Переход на второй этап
  if (nextStepBtn) {
    nextStepBtn.addEventListener('click', function(e) {
      e.preventDefault();

      const username = step1Form.querySelector('.login').value.trim();
      const password = step1Form.querySelector('.password').value.trim();

      if (!username || !password) {
        alert('Пожалуйста, заполните все поля');
        return;
      }

      if (password.length < 6) {
        alert('Пароль должен содержать минимум 6 символов');
        return;
      }

      // Анимация переходов
      step1Content.classList.add('leaving');
      step1Visual.classList.add('leaving');

      setTimeout(() => {
        step1Content.classList.remove('active');
        step1Visual.classList.remove('active');
        
        step2VisualContent.classList.add('active');
        step2FormContent.classList.add('active');
      }, 50);
    });
  }

  // Обработка отправки второго этапа
  if (step2Form) {
    step2Form.addEventListener('submit', function(e) {
      e.preventDefault();

      const username = step1Form.querySelector('.login').value.trim();
      const password = step1Form.querySelector('.password').value.trim();
      const city = step2Form.querySelector('.city').value.trim();
      const district = step2Form.querySelector('.district').value.trim();
      const age = step2Form.querySelector('.age').value.trim();

      if (!username || !password || !city || !district) {
        alert('Пожалуйста, заполните все обязательные поля');
        return;
      }

      // Отправка данных на сервер
      fetch('/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username,
          password: password,
          city: city,
          district: district,
          age: age || null
        })
      })
      .then(response => {
        return response.json().then(data => ({ status: response.status, data }));
      })
      .then(({ status, data }) => {
        if (status === 201 || status === 200) {
          alert('Регистрация успешна!');
          window.location.href = '/chat';
        } else {
          alert(data.error || 'Ошибка при регистрации');
        }
      })
      .catch(error => {
        console.error('Ошибка:', error);
        alert('Ошибка при регистрации. Попробуйте еще раз.');
      });
    });
  }
});
