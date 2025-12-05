// Клиентская логика простого чат-прототипа
// Элементы DOM, с которыми работает скрипт
const messagesEl = document.getElementById('messages'); // контейнер сообщений
const input = document.getElementById('input'); // поле ввода сообщения
const sendBtn = document.getElementById('send'); // кнопка отправки
const historyEl = document.getElementById('history'); // боковая панель истории
const newChatBtn = document.getElementById('newChat'); // кнопка нового чата
const convTitle = document.getElementById('convTitle'); // заголовок текущей беседы
const modelSelect = document.getElementById('modelSelect'); // селектор модели/режима (демо)
// Новые элементы: input для файла и кнопки управления
const fileInput = document.getElementById('fileInput');
const fileBtn = document.getElementById('fileBtn');
const voiceBtn = document.getElementById('voiceBtn');
const deleteBtn = document.getElementById('deleteBtn');

// Текущий активный чат
let currentChatId = null;
// Текущая выбранная кнопка в панели истории
let currentHistoryBtn = null;

// API функции
async function apiRequest(url, options = {}) {
    const defaultOptions = {
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        }
    };
    const response = await fetch(url, { ...defaultOptions, ...options });
    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Ошибка запроса' }));
        throw new Error(error.detail || 'Ошибка запроса');
    }
    return response.json();
}

// Загрузка списка чатов
async function loadChats() {
    try {
        const chats = await apiRequest('/api/chats');
        historyEl.innerHTML = '';
        chats.forEach(chat => {
            addChatToHistory(chat);
        });
    } catch (error) {
        console.error('Ошибка загрузки чатов:', error);
    }
}

// Добавление чата в историю
function addChatToHistory(chat) {
    const btn = document.createElement('div');
    btn.className = 'history-item';
    btn.dataset.chatId = chat.id;
    btn.dataset.title = chat.title;
    
    const icon = document.createElement('i');
    icon.className = 'far fa-comment-alt';
    
    const text = document.createElement('span');
    text.textContent = chat.title.length > 30 ? chat.title.slice(0, 30) + '…' : chat.title;
    
    btn.appendChild(icon);
    btn.appendChild(text);
    
    btn.addEventListener('click', async () => {
        await loadChat(chat.id);
        // Подсветка активного чата
        document.querySelectorAll('#history .history-item').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        // Меняем иконку на активную
        document.querySelectorAll('#history .history-item i').forEach(i => i.className = 'far fa-comment-alt');
        icon.className = 'fas fa-comment-alt';
    });
    
    historyEl.appendChild(btn);
}

// Загрузка чата и его сообщений
async function loadChat(chatId) {
    try {
        currentChatId = chatId;
        const chat = await apiRequest(`/api/chats/${chatId}`);
        const messages = await apiRequest(`/api/chats/${chatId}/messages`);
        
        convTitle.textContent = chat.title;
        messagesEl.innerHTML = '';
        
        // Восстановление сообщений
        messages.forEach(msg => {
            renderMessage(msg);
        });
        
        if (messagesEl.lastElementChild) {
            messagesEl.lastElementChild.scrollIntoView({ behavior: 'smooth', block: 'end' });
        }
    } catch (error) {
        console.error('Ошибка загрузки чата:', error);
        alert('Ошибка загрузки чата');
    }
}

// Рендеринг сообщения
function renderMessage(msg) {
    const el = document.createElement('div');
    el.className = 'msg ' + msg.role;
    
    if (msg.type === 'image') {
        const img = document.createElement('img');
        img.src = msg.content;
        img.style.maxWidth = '240px';
        img.style.borderRadius = '8px';
        el.appendChild(img);
    } else if (msg.type === 'audio') {
        const audio = document.createElement('audio');
        audio.controls = true;
        audio.src = msg.content;
        audio.style.maxWidth = '320px';
        el.appendChild(audio);
    } else if (msg.type === 'file') {
        const link = document.createElement('a');
        link.href = msg.content;
        link.textContent = msg.metadata?.name || msg.content.split('/').pop();
        link.download = msg.metadata?.name || '';
        el.appendChild(link);
    } else {
        el.textContent = msg.content;
    }
    
    messagesEl.appendChild(el);
    return el;
}

// Сохранение сообщения в БД
async function saveMessage(role, content, messageType = 'text', metadata = null) {
    if (!currentChatId) {
        // Создаем новый чат, если его нет
        try {
            const chat = await apiRequest('/api/chats', {
                method: 'POST',
                body: JSON.stringify({ title: 'New Chat' })
            });
            currentChatId = chat.id;
            convTitle.textContent = chat.title;
            addChatToHistory(chat);
        } catch (error) {
            console.error('Ошибка создания чата:', error);
            return;
        }
    }
    
    try {
        await apiRequest(`/api/chats/${currentChatId}/messages`, {
            method: 'POST',
            body: JSON.stringify({
                role: role,
                content: content,
                type: messageType,
                metadata: metadata
            })
        });
    } catch (error) {
        console.error('Ошибка сохранения сообщения:', error);
    }
}

// Функция добавляет сообщение в DOM
function addMessage(text, who = 'assistant', scroll = true) {
    const el = document.createElement('div');
    el.className = 'msg ' + (who === 'user' ? 'user' : 'assistant');
    el.textContent = text;
    messagesEl.appendChild(el);
    if (scroll) el.scrollIntoView({ behavior: 'smooth', block: 'end' });
    return el;
}

// Отправка текстового сообщения
async function sendMessage() {
    const text = input.value.trim();
    if (!text) return;
    
    // Добавляем сообщение пользователя в UI
    addMessage(text, 'user');
    input.value = '';
    sendBtn.disabled = true;
    
    // Сохраняем сообщение пользователя в БД
    await saveMessage('user', text);
    
    // Показываем индикатор загрузки ответа
    const placeholder = addMessage('...', 'assistant');
    
    // Имитация ответа ассистента (здесь можно подключить реальный API)
    setTimeout(async () => {
        const reply = text; // эхо (замените на реальный ответ от AI)
        placeholder.textContent = reply;
        sendBtn.disabled = false;
        
        // Сохраняем ответ ассистента в БД
        await saveMessage('assistant', reply);
    }, 700);
}

// Привязки для кнопки отправки и Enter в textarea
if (sendBtn) {
    sendBtn.addEventListener('click', sendMessage);
}
if (input) {
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
}

// Обработчик прикрепления файла
if (fileBtn && fileInput) {
    fileBtn.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', async (e) => {
        const file = e.target.files && e.target.files[0];
        if (!file) return;
        const name = file.name;
        const placeholder = addMessage('Attached file: ' + name, 'user');
        try {
            const url = URL.createObjectURL(file);
            let messageType = 'file';
            let content = url;
            let metadata = { name: name };
            
            if (file.type.startsWith('image/')) {
                placeholder.textContent = '';
                const img = document.createElement('img');
                img.src = url;
                img.style.maxWidth = '240px';
                img.style.borderRadius = '8px';
                placeholder.appendChild(img);
                messageType = 'image';
            } else {
                placeholder.textContent = '';
                const link = document.createElement('a');
                link.href = url;
                link.textContent = name;
                link.download = name;
                placeholder.appendChild(link);
            }
            
            // Сохраняем файл в БД
            await saveMessage('user', content, messageType, metadata);
        } catch (err) {
            console.error('File attach error', err);
            addMessage('File attach error', 'assistant');
        } finally {
            fileInput.value = '';
        }
    });
}

let recognition = null;
let recognizing = false;
let recorder = null;
let mediaStream = null;
let chunks = [];

if (voiceBtn) {
    voiceBtn.addEventListener('click', async () => {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition || null;
        if (SpeechRecognition) {
            if (recognizing && recognition) {
                try { recognition.stop(); } catch (e) {}
                voiceBtn.classList.remove('recording');
                voiceBtn.textContent = '🎤';
                return;
            }
            recognition = new SpeechRecognition();
            recognition.lang = navigator.language || 'ru-RU';
            recognition.interimResults = true;
            recognition.maxAlternatives = 1;
            recognition.onstart = () => {
                recognizing = true;
                voiceBtn.classList.add('recording');
                voiceBtn.textContent = '■';
            };
            recognition.onresult = (ev) => {
                try {
                    const transcript = Array.from(ev.results).map(r => r[0].transcript).join('');
                    if (transcript != null) {
                        input.value = transcript.trim();
                        input.focus();
                        try { input.selectionStart = input.selectionEnd = input.value.length; } catch (e) {}
                    }
                } catch (err) {
                    console.error('Recognition result error', err);
                    addMessage('Recognition processing error.', 'assistant');
                }
            };
            recognition.onerror = (ev) => {
                console.error('SpeechRecognition error', ev);
                addMessage('Speech recognition error: ' + (ev.error || ev.message || 'unknown'), 'assistant');
            };
            recognition.onend = () => {
                recognizing = false;
                voiceBtn.classList.remove('recording');
                voiceBtn.textContent = '🎤';
            };
            try { recognition.start(); } catch (e) {
                console.error('Recognition start failed', e);
                addMessage('Speech recognition start failed.', 'assistant');
            }
            return;
        }

        if (recorder && recorder.state === 'recording') {
            try { recorder.stop(); } catch (e) { console.warn('Stop recorder failed', e); }
            voiceBtn.classList.remove('recording');
            voiceBtn.textContent = '🎤';
            return;
        }

        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            addMessage('Your browser does not support microphone access (navigator.mediaDevices).', 'assistant');
            return;
        }
        if (typeof MediaRecorder === 'undefined') {
            addMessage('MediaRecorder API is not available in this browser.', 'assistant');
            return;
        }

        try {
            mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
            let options = {};
            if (MediaRecorder.isTypeSupported) {
                if (MediaRecorder.isTypeSupported('audio/webm;codecs=opus')) options.mimeType = 'audio/webm;codecs=opus';
                else if (MediaRecorder.isTypeSupported('audio/webm')) options.mimeType = 'audio/webm';
                else if (MediaRecorder.isTypeSupported('audio/mp4')) options.mimeType = 'audio/mp4';
            }
            try {
                recorder = Object.keys(options).length ? new MediaRecorder(mediaStream, options) : new MediaRecorder(mediaStream);
            } catch (e) {
                recorder = new MediaRecorder(mediaStream);
            }
            chunks = [];
            recorder.ondataavailable = e => {
                if (e.data && e.data.size) chunks.push(e.data);
            };
            recorder.onstop = async () => {
                try {
                    const mime = chunks[0] && chunks[0].type ? chunks[0].type : 'audio/webm';
                    const blob = new Blob(chunks, { type: mime });
                    const url = URL.createObjectURL(blob);
                    const placeholder = addMessage('Voice message', 'user');
                    placeholder.textContent = '';
                    const audio = document.createElement('audio');
                    audio.controls = true;
                    audio.src = url;
                    audio.style.maxWidth = '320px';
                    placeholder.appendChild(audio);
                    
                    // Сохраняем голосовое сообщение в БД
                    await saveMessage('user', url, 'audio', { mime: mime });
                    
                    if (mediaStream) {
                        mediaStream.getTracks().forEach(t => t.stop());
                        mediaStream = null;
                    }
                } catch (err) {
                    console.error('Error processing recorded audio', err);
                    addMessage('Recording failed to process.', 'assistant');
                }
            };
            recorder.onerror = (ev) => {
                console.error('Recorder error', ev);
                addMessage('Recording error: ' + (ev?.error?.name || ev?.error || 'unknown'), 'assistant');
            };
            recorder.start();
            voiceBtn.classList.add('recording');
            voiceBtn.textContent = '■';
        } catch (err) {
            console.error('Voice record error', err);
            if (err && (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError')) {
                addMessage('Permission to use microphone was denied.', 'assistant');
            } else {
                addMessage('Voice input not supported or permission denied.', 'assistant');
            }
            try {
                if (mediaStream) {
                    mediaStream.getTracks().forEach(t => t.stop());
                    mediaStream = null;
                }
            } catch (e) {}
        }
    });
}

// Создать новый чат
newChatBtn.addEventListener('click', async () => {
    try {
        // Если есть текущий чат с сообщениями, сохраняем его заголовок
        if (currentChatId) {
            const messages = messagesEl.querySelectorAll('.msg');
            if (messages.length > 1) { // больше чем приветственное сообщение
                const lastUserMessage = Array.from(messages).reverse().find(m => m.classList.contains('user'));
                if (lastUserMessage) {
                    const title = lastUserMessage.textContent.slice(0, 40);
                    try {
                        await apiRequest(`/api/chats/${currentChatId}`, {
                            method: 'PUT',
                            body: JSON.stringify({ title: title || 'New Chat' })
                        });
                    } catch (e) {
                        console.error('Ошибка обновления заголовка чата:', e);
                    }
                }
            }
        }
        
        // Создаем новый чат
        const chat = await apiRequest('/api/chats', {
            method: 'POST',
            body: JSON.stringify({ title: 'New Chat' })
        });
        
        currentChatId = chat.id;
        convTitle.textContent = chat.title;
        messagesEl.innerHTML = '';
        addMessage('Hello! I am a local prototype. Ask me anything or write a task.', 'assistant');
        
        // Добавляем в историю
        addChatToHistory(chat);
        
        // Подсветка нового чата
        document.querySelectorAll('#history .history-item').forEach(b => b.classList.remove('active'));
        const newBtn = document.querySelector(`#history .history-item[data-chat-id="${chat.id}"]`);
        if (newBtn) {
            newBtn.classList.add('active');
            newBtn.querySelector('i').className = 'fas fa-comment-alt';
            currentHistoryBtn = newBtn;
        }
    } catch (error) {
        console.error('Ошибка создания нового чата:', error);
        alert('Ошибка создания нового чата');
    }
});

// Удаление текущего диалога
if (deleteBtn) {
    deleteBtn.addEventListener('click', async () => {
        if (!currentChatId) {
            alert('Нет активного чата для удаления');
            return;
        }
        
        const ok = confirm('Delete this conversation? This cannot be undone.');
        if (!ok) return;
        
        try {
            await apiRequest(`/api/chats/${currentChatId}`, {
                method: 'DELETE'
            });
            
            // Удаляем из истории
            if (currentHistoryBtn) {
                currentHistoryBtn.remove();
                currentHistoryBtn = null;
            }
            
            // Очищаем интерфейс
            currentChatId = null;
            messagesEl.innerHTML = '';
            convTitle.textContent = 'New Chat';
            addMessage('Conversation deleted.', 'assistant');
        } catch (error) {
            console.error('Ошибка удаления чата:', error);
            alert('Ошибка удаления чата');
        }
    });
}

// Загрузка чатов при загрузке страницы
document.addEventListener('DOMContentLoaded', async () => {
    await loadChats();
    // Фокус на поле ввода
    if (input) input.focus();
});
