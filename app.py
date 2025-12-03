"""
Основной файл Flask приложения для городского помощника.
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from database import db, User
from functools import wraps

app = Flask(__name__, 
            template_folder='resources/templates',
            static_folder='resources/static',
            static_url_path='/resources/static')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://localhost/city_helper')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
db.init_app(app)

# Создание таблиц будет происходить через init_db.py


def login_required(f):
    """Декоратор для проверки авторизации."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Требуется авторизация'}), 401
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    """Главная страница."""
    return render_template('index.html')


@app.route('/api/register', methods=['POST'])
def register():
    """Регистрация нового пользователя."""
    data = request.get_json()
    
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    city = data.get('city', '').strip()
    district = data.get('district', '').strip()
    age = data.get('age', '').strip()
    
    if not username or not password:
        return jsonify({'error': 'Логин и пароль обязательны'}), 400
    
    if len(password) < 6:
        return jsonify({'error': 'Пароль должен содержать минимум 6 символов'}), 400
    
    # Проверка существования пользователя
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Пользователь с таким логином уже существует'}), 400
    
    # Создание нового пользователя
    try:
        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            city=city if city else None,
            district=district if district else None,
            age=int(age) if age and age.isdigit() else None
        )
        db.session.add(user)
        db.session.commit()
        
        # Автоматический вход после регистрации
        session['user_id'] = user.id
        session['username'] = user.username
        
        return jsonify({
            'message': 'Регистрация успешна',
            'user': {
                'id': user.id,
                'username': user.username,
                'city': user.city,
                'district': user.district,
                'age': user.age
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Ошибка при регистрации: {str(e)}'}), 500


@app.route('/api/login', methods=['POST'])
def login():
    """Вход пользователя."""
    data = request.get_json()
    
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    if not username or not password:
        return jsonify({'error': 'Логин и пароль обязательны'}), 400
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Неверный логин или пароль'}), 401
    
    session['user_id'] = user.id
    session['username'] = user.username
    
    return jsonify({
        'message': 'Вход выполнен успешно',
        'user': {
            'id': user.id,
            'username': user.username,
            'city': user.city,
            'district': user.district,
            'age': user.age
        }
    }), 200


@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    """Выход пользователя."""
    session.clear()
    return jsonify({'message': 'Выход выполнен успешно'}), 200


@app.route('/api/user', methods=['GET'])
@login_required
def get_user():
    """Получение данных текущего пользователя."""
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        return jsonify({'error': 'Пользователь не найден'}), 404
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'city': user.city,
        'district': user.district,
        'age': user.age,
        'created_at': user.created_at.isoformat() if user.created_at else None
    }), 200


@app.route('/api/user', methods=['PUT'])
@login_required
def update_user():
    """Обновление данных пользователя."""
    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({'error': 'Пользователь не найден'}), 404
    
    data = request.get_json()
    
    if 'city' in data:
        user.city = data['city'].strip() if data['city'] else None
    if 'district' in data:
        user.district = data['district'].strip() if data['district'] else None
    if 'age' in data:
        age = data['age']
        user.age = int(age) if age and str(age).isdigit() else None
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Данные обновлены успешно',
            'user': {
                'id': user.id,
                'username': user.username,
                'city': user.city,
                'district': user.district,
                'age': user.age
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Ошибка при обновлении: {str(e)}'}), 500


@app.route('/api/change-password', methods=['POST'])
@login_required
def change_password():
    """Изменение пароля пользователя."""
    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({'error': 'Пользователь не найден'}), 404
    
    data = request.get_json()
    current_password = data.get('currentPassword', '').strip()
    new_password = data.get('newPassword', '').strip()
    confirm_password = data.get('confirmPassword', '').strip()
    
    if not current_password or not new_password or not confirm_password:
        return jsonify({'error': 'Все поля обязательны'}), 400
    
    if not check_password_hash(user.password_hash, current_password):
        return jsonify({'error': 'Текущий пароль неверен'}), 401
    
    if new_password != confirm_password:
        return jsonify({'error': 'Новые пароли не совпадают'}), 400
    
    if len(new_password) < 6:
        return jsonify({'error': 'Пароль должен содержать минимум 6 символов'}), 400
    
    try:
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        return jsonify({'message': 'Пароль успешно изменен'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Ошибка при изменении пароля: {str(e)}'}), 500


@app.route('/api/check-auth', methods=['GET'])
def check_auth():
    """Проверка авторизации пользователя."""
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            return jsonify({
                'authenticated': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'city': user.city,
                    'district': user.district,
                    'age': user.age
                }
            }), 200
    return jsonify({'authenticated': False}), 200


# Роуты для страниц
@app.route('/auth/login')
def login_page():
    """Страница входа."""
    return render_template('auth/auth.html')


@app.route('/auth/register')
def register_page():
    """Страница регистрации."""
    return render_template('auth/regist.html')


@app.route('/profile')
def profile_page():
    """Страница профиля."""
    return render_template('profile/profile.html')


@app.route('/chat')
def chat_page():
    """Страница чата."""
    return render_template('chat/chat.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
