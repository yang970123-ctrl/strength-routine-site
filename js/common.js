// 공통 하단 네비게이션 & 헤더 렌더링
function renderChrome(activePage) {
  const nav = [
    { id: 'home', label: '홈', icon: '🏠', href: 'index.html' },
    { id: 'onerm', label: '1RM계산', icon: '🏋️', href: '1rm-calculator.html' },
    { id: 'standard', label: '강도표준', icon: '📊', href: 'strength-standards.html' },
    { id: 'log', label: '운동기록', icon: '📝', href: 'workout-log.html' },
  ];

  const header = document.createElement('header');
  header.className = 'top';
  header.innerHTML = `
    <div class="container">
      <a href="index.html" class="brand">오늘의 <span>근력루틴</span></a>
    </div>`;
  document.body.prepend(header);

  const navEl = document.createElement('nav');
  navEl.className = 'bottom-nav';
  navEl.innerHTML = nav.map(item => `
    <a href="${item.href}" class="${item.id === activePage ? 'active' : ''}">
      <span class="nav-icon">${item.icon}</span>${item.label}
    </a>`).join('');
  document.body.appendChild(navEl);
}

// localStorage 기반 운동 기록
const LOG_KEY = 'strength_workout_log_v1';

function getLogs() {
  try {
    return JSON.parse(localStorage.getItem(LOG_KEY)) || [];
  } catch (e) {
    return [];
  }
}

function saveLogs(logs) {
  localStorage.setItem(LOG_KEY, JSON.stringify(logs));
}

function addLog(entry) {
  const logs = getLogs();
  logs.unshift({ ...entry, id: Date.now(), date: new Date().toISOString().slice(0, 10) });
  saveLogs(logs);
  return logs;
}

function deleteLog(id) {
  const logs = getLogs().filter(l => l.id !== id);
  saveLogs(logs);
  return logs;
}
