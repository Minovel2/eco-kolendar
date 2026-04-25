const API_URL = 'http://127.0.0.1:8000/api';
        let currentFilters = { type: 'all', region: 'all', search: '' };
        let currentView = 'grid';
        let allHolidays = [];
        let currentHolidayId = null;
        let currentUser = null; // { id, email, role, name }

        // Проверка при загрузке
        if (localStorage.getItem('user')) {
            currentUser = JSON.parse(localStorage.getItem('user'));
            updateUserUI();
        }
        
        // Календарь
        let calendarYear = new Date().getFullYear();
        let calendarMonth = new Date().getMonth(); // 0-11

        const typeLabels = { eco: 'Экология', national: 'Национальный', world: 'Мировой' };
        const typeClasses = { eco: 'type-eco', national: 'type-national', world: 'type-world' };
        const regionLabels = { russia: 'Россия', world: 'Весь мир' };
        const months = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 
                       'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря'];
        const monthNames = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
                           'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];

        // Переключение вида
        function switchView(view) {
            currentView = view;
            
            // Обновляем кнопки
            document.querySelectorAll('.view-btn').forEach(b => b.classList.remove('active'));
            event.target.classList.add('active');
            
            // Показываем/скрываем контейнеры
            document.getElementById('gridView').style.display = view === 'grid' ? 'block' : 'none';
            document.getElementById('calendarView').style.display = view === 'calendar' ? 'block' : 'none';
            
            if (view === 'calendar') {
                renderCalendar();
            }
        }

        function updateUserUI() {
    if (currentUser) {
        document.getElementById('userArea').style.display = 'none';
        document.getElementById('adminArea').style.display = 'flex';
        document.getElementById('userName').textContent = currentUser.name;
        
        // Показываем кнопки админа только для админов
        const adminBtns = document.querySelectorAll('.admin-only');
        adminBtns.forEach(b => b.style.display = currentUser.role === 1 ? 'inline-block' : 'none');
        
        // Кнопка "+ Праздник" видна только админу
        document.querySelector('.btn-admin').style.display = currentUser.role === 1 ? 'inline-block' : 'none';
    } else {
        document.getElementById('userArea').style.display = 'flex';
        document.getElementById('adminArea').style.display = 'none';
    }
}

function showLogin() {
    // Удаляем старую форму если есть
    const oldForm = document.getElementById('authForm');
    if (oldForm) oldForm.remove();
    // Удаляем форму добавления праздника если открыта
    const holidayForm = document.getElementById('holidayForm');
    if (holidayForm) holidayForm.remove();
    
    const formHtml = `
        <div class="auth-form" id="authForm">
            <h2 style="color: #5A5A40; margin-bottom: 20px;">🔑 Вход</h2>
            <input type="email" id="loginEmail" placeholder="Email">
            <input type="password" id="loginPassword" placeholder="Пароль">
            <button onclick="login()">Войти</button>
            <p class="form-switch" onclick="showRegister()">Нет аккаунта? Зарегистрироваться</p>
            <p class="form-switch" onclick="closeAuthForm()">Отмена</p>
        </div>`;
    
    document.getElementById('gridView').insertAdjacentHTML('beforebegin', formHtml);
}

function showRegister() {
    // Удаляем старую форму если есть
    const oldForm = document.getElementById('authForm');
    if (oldForm) oldForm.remove();
    
    const formHtml = `
        <div class="auth-form" id="authForm">
            <h2 style="color: #5A5A40; margin-bottom: 20px;">📝 Регистрация</h2>
            <input type="text" id="regLastName" placeholder="Фамилия">
            <input type="text" id="regFirstName" placeholder="Имя">
            <input type="text" id="regPatronymic" placeholder="Отчество (необязательно)">
            <input type="email" id="regEmail" placeholder="Email">
            <input type="password" id="regPassword" placeholder="Пароль">
            <button onclick="register()">Зарегистрироваться</button>
            <p class="form-switch" onclick="showLogin()">Уже есть аккаунт? Войти</p>
            <p class="form-switch" onclick="closeAuthForm()">Отмена</p>
        </div>`;
    
    document.getElementById('gridView').insertAdjacentHTML('beforebegin', formHtml);
}

function closeAuthForm() {
    const form = document.getElementById('authForm');
    if (form) form.remove();
}

async function login() {
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    
    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        
        if (response.ok) {
            currentUser = await response.json();
            localStorage.setItem('user', JSON.stringify(currentUser));
            updateUserUI();
            closeAuthForm();
        } else {
            const error = await response.json();
            alert('Ошибка: ' + error.detail);
        }
    } catch (error) {
        alert('Ошибка соединения с сервером');
    }
}

async function register() {
    const data = {
        last_name: document.getElementById('regLastName').value,
        first_name: document.getElementById('regFirstName').value,
        patronymic: document.getElementById('regPatronymic').value || '',
        email: document.getElementById('regEmail').value,
        password: document.getElementById('regPassword').value
    };
    
    try {
        const response = await fetch(`${API_URL}/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            alert('Регистрация успешна! Теперь войдите.');
            showLogin();
        } else {
            const error = await response.json();
            alert('Ошибка: ' + error.detail);
        }
    } catch (error) {
        alert('Ошибка соединения с сервером');
    }
}

function logout() {
    currentUser = null;
    localStorage.removeItem('user');
    updateUserUI();
}

function showAddHolidayForm() {
    if (!currentUser || currentUser.role !== 1) {
        alert('Только администратор может добавлять праздники');
        return;
    }
    
    // Удаляем старые формы
    const oldForm = document.getElementById('holidayForm');
    if (oldForm) oldForm.remove();
    const authForm = document.getElementById('authForm');
    if (authForm) authForm.remove();

    const formHtml = `
        <div class="auth-form" id="holidayForm" style="max-width: 600px;">
            <h2 style="color: #5A5A40; margin-bottom: 20px;">➕ Новый праздник</h2>
            <input type="text" id="newName" placeholder="Название">
            <div style="display: flex; gap: 10px;">
                <input type="number" id="newDay" placeholder="День" min="1" max="31" style="flex: 1;">
                <select id="newMonth" style="flex: 1; padding: 12px; border: 2px solid #e0e0d0; border-radius: 12px;">
                    ${monthNames.map((m, i) => `<option value="${i}">${m}</option>`).join('')}
                </select>
            </div>
            <select id="newType" style="width: 100%; padding: 12px; border: 2px solid #e0e0d0; border-radius: 12px; margin-bottom: 12px;">
                <option value="eco">Экологический</option>
                <option value="national">Национальный</option>
                <option value="world">Мировой</option>
            </select>
            <select id="newRegion" style="width: 100%; padding: 12px; border: 2px solid #e0e0d0; border-radius: 12px; margin-bottom: 12px;">
                <option value="russia">Россия</option>
                <option value="world">Весь мир</option>
            </select>
            <textarea id="newDescription" placeholder="Описание" rows="4" style="width: 100%; padding: 12px; border: 2px solid #e0e0d0; border-radius: 12px; margin-bottom: 12px;"></textarea>
            <input type="text" id="newEvents" placeholder="Мероприятия (через запятую)">
            <input type="url" id="newWikiUrl" placeholder="Ссылка на Википедию">
            <button onclick="addHoliday()">Сохранить</button>
            <p class="form-switch" onclick="document.getElementById('holidayForm').remove()">Отмена</p>
        </div>`;
    
    document.getElementById('gridView').insertAdjacentHTML('beforebegin', formHtml);
}

async function addHoliday() {
    const events = document.getElementById('newEvents').value
        .split(',')
        .map(e => e.trim())
        .filter(e => e);
    
    const data = {
        name: document.getElementById('newName').value,
        day: parseInt(document.getElementById('newDay').value),
        month: parseInt(document.getElementById('newMonth').value),
        type: document.getElementById('newType').value,
        region: document.getElementById('newRegion').value,
        description: document.getElementById('newDescription').value,
        events: events,
        wikipedia_url: document.getElementById('newWikiUrl').value
    };
    
    try {
        const response = await fetch(`${API_URL}/holidays`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            document.getElementById('holidayForm').remove();
            loadHolidays();
        }
    } catch (error) {
        alert('Ошибка при добавлении');
    }
}

        // Загрузка данных
        async function loadHolidays() {
            try {
                const params = new URLSearchParams();
                if (currentFilters.type !== 'all') params.append('type', currentFilters.type);
                if (currentFilters.region !== 'all') params.append('region', currentFilters.region);
                if (currentFilters.search) params.append('search', currentFilters.search);
                
                const response = await fetch(`${API_URL}/holidays?${params}`);
                allHolidays = await response.json();
                
                if (currentView === 'grid') {
                    renderGrid();
                } else {
                    renderCalendar();
                }
            } catch (error) {
                console.error('Ошибка загрузки:', error);
                const container = document.getElementById('holidaysContainer');
                container.innerHTML = '<div class="loading" style="color: red;">❌ Ошибка загрузки. Проверьте, запущен ли сервер на http://127.0.0.1:8000</div>';
            }
        }

        // Сетка (карточки)
        function renderGrid() {
            const container = document.getElementById('holidaysContainer');
            
            if (!allHolidays || allHolidays.length === 0) {
                container.innerHTML = `
                    <div class="empty" style="grid-column: 1/-1;">
                        <div class="empty-icon">🌍</div>
                        <h3>Ничего не найдено</h3>
                        <p>Попробуйте изменить параметры поиска</p>
                    </div>`;
                return;
            }
            
            container.innerHTML = allHolidays.map(holiday => `
                <div class="holiday-card" onclick="openModal(${holiday.id})">
                    <div class="card-header">
                        <div class="date-badge">📅 ${holiday.day} ${months[holiday.month]}</div>
                        <div class="type-badge ${typeClasses[holiday.type]}">${typeLabels[holiday.type]}</div>
                    </div>
                    <h2>${holiday.name}</h2>
                    <p>${holiday.description.substring(0, 150)}...</p>
                    <div class="card-footer">
                        <span>📍 ${regionLabels[holiday.region]}</span>
                        <span>🏷️ ${typeLabels[holiday.type]}</span>
                    </div>
                </div>
            `).join('');
        }

        // Календарь
        function renderCalendar() {
            document.getElementById('calendarMonthTitle').textContent = 
                `${monthNames[calendarMonth]} ${calendarYear}`;
            
            const daysContainer = document.getElementById('calendarDays');
            
            // Первый день месяца
            const firstDay = new Date(calendarYear, calendarMonth, 1);
            // Последний день месяца
            const lastDay = new Date(calendarYear, calendarMonth + 1, 0);
            
            // День недели первого дня (Пн=0, Вс=6)
            let startDay = firstDay.getDay() - 1;
            if (startDay < 0) startDay = 6;
            
            let html = '';
            
            // Пустые ячейки перед первым днем
            for (let i = 0; i < startDay; i++) {
                html += '<div class="day-cell other-month"></div>';
            }
            
            // Дни месяца
            for (let day = 1; day <= lastDay.getDate(); day++) {
                const dayHolidays = allHolidays.filter(h => 
                    h.day === day && h.month === calendarMonth
                );
                
                const isToday = (day === new Date().getDate() && 
                                calendarMonth === new Date().getMonth() && 
                                calendarYear === new Date().getFullYear());
                
                html += `<div class="day-cell ${isToday ? 'today' : ''}">`;
                html += `<div class="day-number">${day}</div>`;
                
                // Показываем первые 2 праздника
                const maxShow = 2;
                dayHolidays.slice(0, maxShow).forEach(h => {
                    html += `<div class="day-holiday ${h.type}" onclick="event.stopPropagation(); openModal(${h.id})" title="${h.name}">${h.name.substring(0, 25)}</div>`;
                });
                
                if (dayHolidays.length > maxShow) {
                    html += `<div class="more-badge">+${dayHolidays.length - maxShow} ещё</div>`;
                }
                
                html += '</div>';
            }
            
            daysContainer.innerHTML = html;
        }

        function prevMonth() {
            if (calendarMonth === 0) {
                calendarMonth = 11;
                calendarYear--;
            } else {
                calendarMonth--;
            }
            renderCalendar();
        }

        function nextMonth() {
            if (calendarMonth === 11) {
                calendarMonth = 0;
                calendarYear++;
            } else {
                calendarMonth++;
            }
            renderCalendar();
        }

        // Модальное окно
        function openModal(holidayId) {
            const holiday = allHolidays.find(h => h.id === holidayId);
            if (!holiday) return;
            
            currentHolidayId = holidayId;
            
            document.getElementById('modalBadges').innerHTML = `
                <span class="type-badge ${typeClasses[holiday.type]}" style="background: rgba(255,255,255,0.3); color: white;">
                    ${typeLabels[holiday.type]}
                </span>
                <span class="type-badge" style="background: rgba(255,255,255,0.3); color: white;">
                    ${regionLabels[holiday.region]}
                </span>
            `;
            
            document.getElementById('modalTitle').textContent = holiday.name;
            document.getElementById('modalDescription').textContent = holiday.description;
            
            let events = [];
            try {
                events = typeof holiday.events === 'string' ? JSON.parse(holiday.events) : holiday.events;
            } catch(e) {
                events = [];
            }
            
            document.getElementById('modalEvents').innerHTML = events.map(e => 
                `<li>🟢 ${e}</li>`
            ).join('');
            
            const wikiLink = document.getElementById('modalWiki');
            if (holiday.wikipedia_url) {
                wikiLink.href = holiday.wikipedia_url;
                wikiLink.style.display = 'inline-block';
            } else {
                wikiLink.style.display = 'none';
            }
            
            document.getElementById('holidayModal').classList.add('active');

            // Показываем кнопку удаления только для админа
            document.querySelector('.delete-btn').style.display = 
            (currentUser && currentUser.role === 1) ? 'inline-block' : 'none';
        }

        function closeModal() {
            document.getElementById('holidayModal').classList.remove('active');
            currentHolidayId = null;
        }

        async function deleteCurrentHoliday() {
    if (!currentHolidayId) return;
    if (!currentUser || currentUser.role !== 1) {
        alert('Только администратор может удалять праздники');
        return;
    }
    if (!confirm('Вы уверены, что хотите удалить этот праздник?')) return;
    
    try {
        await fetch(`${API_URL}/holidays/${currentHolidayId}`, { method: 'DELETE' });
        closeModal();
        loadHolidays();
    } catch (error) {
        alert('Ошибка при удалении');
    }
}

        // Фильтры
        function setFilter(type, value, button) {
            currentFilters[type] = value;
            
            button.parentElement.querySelectorAll('.btn').forEach(b => b.classList.remove('active'));
            button.classList.add('active');
            
            applyFilters();
        }

        function applyFilters() {
            currentFilters.search = document.getElementById('searchInput').value;
            loadHolidays();
        }

        // Закрытие модального окна по клику вне его
        document.getElementById('holidayModal').addEventListener('click', function(e) {
            if (e.target === this) closeModal();
        });

        // Первая загрузка
        loadHolidays();