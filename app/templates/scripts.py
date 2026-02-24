"""app/templates/scripts.py — shared client-side game engine."""

SHARED_JS = r"""
/* ── CONSTANTS ─────────────────────────────────────────────── */
var XP_PER_LEVEL  = 200;
var XP_CORRECT    = 50;
var HP_MAX        = 3;
var SAVE_KEY      = 'fd_save_v2';

/* ── AUDIO ENGINE (Web Audio API) ───────────────────────────── */
var _ac = null;
function getAC() {
  if (!_ac) {
    try { _ac = new (window.AudioContext||window.webkitAudioContext)(); } catch(e) {}
  }
  return _ac;
}
function playTone(freq, type, dur, vol, delay) {
  var ac = getAC(); if (!ac) return;
  var osc = ac.createOscillator();
  var gain = ac.createGain();
  osc.connect(gain); gain.connect(ac.destination);
  osc.type = type || 'sine';
  osc.frequency.setValueAtTime(freq, ac.currentTime + (delay||0));
  gain.gain.setValueAtTime(vol||0.18, ac.currentTime + (delay||0));
  gain.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + (delay||0) + dur);
  osc.start(ac.currentTime + (delay||0));
  osc.stop(ac.currentTime + (delay||0) + dur + 0.05);
}
function playSound(name) {
  var ac = getAC(); if (!ac) return;
  if (name === 'correct') {
    playTone(440, 'sine', 0.12, 0.12, 0.00);
    playTone(554, 'sine', 0.12, 0.12, 0.12);
    playTone(659, 'sine', 0.22, 0.15, 0.24);
  } else if (name === 'wrong') {
    playTone(200, 'sawtooth', 0.08, 0.15, 0.00);
    playTone(150, 'sawtooth', 0.18, 0.12, 0.10);
  } else if (name === 'level_up') {
    [523,659,784,1047].forEach(function(f,i){playTone(f,'triangle',0.14,0.14,i*0.1);});
  } else if (name === 'boss_defeated') {
    [392,523,659,784,1047].forEach(function(f,i){playTone(f,'sine',0.18,0.16,i*0.09);});
  } else if (name === 'hint') {
    playTone(660, 'triangle', 0.18, 0.08, 0);
  } else if (name === 'click') {
    playTone(1000, 'square', 0.04, 0.06, 0);
  }
}

/* ── STATE MANAGEMENT ───────────────────────────────────────── */
function saveState(s) {
  try { localStorage.setItem(SAVE_KEY, JSON.stringify(s)); } catch(e) {}
}
function loadState() {
  try { var r = localStorage.getItem(SAVE_KEY); return r ? JSON.parse(r) : null; }
  catch(e) { return null; }
}
function clearState() {
  try { localStorage.removeItem(SAVE_KEY); } catch(e) {}
}
function getState() {
  var s = loadState();
  if (!s) s = { xp:0, level:1, hp:HP_MAX, done:[], answered:{},
                streak:0, bestStreak:0, totalXP:0, startTime:Date.now(),
                quizAttempts:{} };
  /* back-compat: ensure all fields exist */
  if (s.hp    === undefined) s.hp    = HP_MAX;
  if (s.streak === undefined) s.streak = 0;
  if (s.bestStreak === undefined) s.bestStreak = 0;
  return s;
}

/* ── HUD RENDERER ───────────────────────────────────────────── */
function renderHUD() {
  var s   = getState();
  var cap = XP_PER_LEVEL * s.level;
  var pct = Math.min((s.xp / cap) * 100, 100).toFixed(1);

  var xpFill = document.getElementById('xp-fill');
  var xpNum  = document.getElementById('xp-num');
  var lvl    = document.getElementById('hud-lvl');
  var strk   = document.getElementById('hud-streak');

  if (xpFill) xpFill.style.width = pct + '%';
  if (xpNum)  xpNum.textContent  = s.xp + ' / ' + cap + ' XP';
  if (lvl)    lvl.textContent    = 'LVL ' + s.level;
  if (strk) {
    strk.textContent = s.streak > 0 ? '🔥 ' + s.streak : '';
    if (s.streak >= 3) strk.classList.add('bump');
    else               strk.classList.remove('bump');
  }

  for (var i = 0; i < HP_MAX; i++) {
    var h = document.getElementById('ht' + i);
    if (h) h.classList[i >= s.hp ? 'add' : 'remove']('dead');
  }
  for (var j = 0; j < 8; j++) {
    var b = document.getElementById('bdg' + j);
    if (b) b.classList[s.done.indexOf(j) === -1 ? 'add' : 'remove']('locked');
  }
}

/* ── XP AND HP ──────────────────────────────────────────────── */
function addXP(amount) {
  var s   = getState();
  s.xp   += amount;
  s.totalXP = (s.totalXP || 0) + amount;
  /* Level up loop */
  var cap = XP_PER_LEVEL * s.level;
  while (s.xp >= cap) {
    s.xp -= cap;
    s.level++;
    cap = XP_PER_LEVEL * s.level;
    playSound('level_up');
    showAchievement('⬆ LEVEL UP!', 'You reached Level ' + s.level + '!');
  }
  saveState(s);
  renderHUD();
  showXPPop('+' + amount + ' XP');
}

function loseHP() {
  var s  = getState();
  if (s.hp > 0) s.hp--;
  s.streak = 0;
  saveState(s);
  renderHUD();
  /* Visual damage flash */
  var fl = document.createElement('div');
  fl.className = 'dmg-flash';
  document.body.appendChild(fl);
  document.body.classList.add('screen-shake');
  setTimeout(function(){ document.body.classList.remove('screen-shake'); fl.remove(); }, 440);
  playSound('wrong');
}

function markDone(missionId, missionXP) {
  var s = getState();
  if (s.done.indexOf(missionId) === -1) {
    s.done.push(missionId);
    addXP(missionXP);
  }
  saveState(s);
  renderHUD();
}

function incrementStreak() {
  var s = getState();
  s.streak = (s.streak || 0) + 1;
  if (s.streak > (s.bestStreak || 0)) s.bestStreak = s.streak;
  saveState(s);
  renderHUD();
  if (s.streak === 3)  showAchievement('🔥 ON FIRE!',     '3-answer streak!');
  if (s.streak === 5)  showAchievement('💥 UNSTOPPABLE!', '5-answer streak!');
  if (s.streak === 8)  showAchievement('👑 LEGENDARY!',   '8-answer streak!');
}

/* ── FLOATING EFFECTS ───────────────────────────────────────── */
function showXPPop(txt) {
  var el = document.createElement('div');
  el.className = 'xp-pop';
  el.textContent = txt;
  document.body.appendChild(el);
  setTimeout(function(){ el.remove(); }, 2200);
}

function showAchievement(title, body) {
  var el = document.createElement('div');
  el.className = 'achievement-toast';
  el.innerHTML = '<div class="toast-title">🏆 ACHIEVEMENT</div>'
               + '<div class="toast-body"><strong>' + title + '</strong><br>' + body + '</div>';
  document.body.appendChild(el);
  setTimeout(function(){ el.remove(); }, 3200);
}

function spawnParticles(x, y, count, colors) {
  colors = colors || ['#00f5ff','#39ff14','#ffe600','#ffffff'];
  for (var i = 0; i < (count||18); i++) {
    var p  = document.createElement('div');
    p.className = 'particle';
    var c  = colors[Math.floor(Math.random()*colors.length)];
    var sz = 4 + Math.random()*7;
    var dx = (Math.random()-0.5)*260;
    var dy = -(60 + Math.random()*160);
    p.style.cssText = [
      'left:'        + x + 'px',
      'top:'         + y + 'px',
      'width:'       + sz + 'px',
      'height:'      + sz + 'px',
      'background:'  + c,
      'box-shadow:0 0 8px ' + c,
      '--px:'        + dx + 'px',
      '--py:'        + dy + 'px',
      '--pt:'        + (0.8 + Math.random()*0.7) + 's',
    ].join(';');
    document.body.appendChild(p);
    setTimeout(function(el){ el.remove(); }, 1600, p);
  }
}

function spawnConfetti() {
  var colors = ['#ffe600','#00f5ff','#39ff14','#ff2244','#bf5fff','#ff8c00','#ffffff'];
  for (var i = 0; i < 90; i++) {
    var c  = document.createElement('div');
    c.className = 'confetti-piece';
    var col = colors[i % colors.length];
    var cx  = (Math.random()-0.5)*260;
    var cy  = 180 + Math.random()*280;
    c.style.cssText = [
      'left:'       + (20 + Math.random()*60) + '%',
      'top:'        + '30%',
      'background:' + col,
      '--cx:'       + cx + 'px',
      '--cy:'       + cy + 'px',
      '--ct:'       + (1.2 + Math.random()*1.2) + 's',
      '--cd:'       + (Math.random()*0.6) + 's',
    ].join(';');
    document.body.appendChild(c);
    setTimeout(function(el){ el.remove(); }, 3000, c);
  }
}

/* ── TYPEWRITER ─────────────────────────────────────────────── */
function typewriterElement(el, text, speed) {
  speed = speed || 28;
  el.textContent = '';
  var cursor = document.createElement('span');
  cursor.className = 'tw-cursor';
  el.appendChild(cursor);
  var i = 0;
  function tick() {
    if (i < text.length) {
      el.insertBefore(document.createTextNode(text[i]), cursor);
      i++;
      setTimeout(tick, speed + Math.random()*18);
    } else {
      setTimeout(function(){ cursor.remove(); }, 900);
    }
  }
  setTimeout(tick, 200);
}

function initTypewriters() {
  var els = document.querySelectorAll('[data-tw]');
  els.forEach(function(el, idx) {
    var text = el.getAttribute('data-tw') || el.textContent;
    el.setAttribute('data-tw', text);
    setTimeout(function(){
      typewriterElement(el, text, 22);
    }, idx * 120);
  });
}

/* ── BOSS BATTLE TIMER ──────────────────────────────────────── */
var _timerInterval  = null;
var _timerRemaining = 60;
var _timerStarted   = false;

function startTimer(seconds, onExpire) {
  if (_timerStarted) return;
  _timerStarted   = true;
  _timerRemaining = seconds || 60;
  var fill = document.getElementById('timer-fill');
  var num  = document.getElementById('timer-num');
  _timerInterval = setInterval(function() {
    _timerRemaining--;
    if (fill) fill.style.width = Math.max(0, (_timerRemaining / seconds) * 100) + '%';
    if (num)  num.textContent  = _timerRemaining;
    if (_timerRemaining <= 15 && fill) fill.style.boxShadow = '0 0 12px rgba(255,34,68,.7)';
    if (_timerRemaining <= 0) {
      clearInterval(_timerInterval);
      if (typeof onExpire === 'function') onExpire();
    }
  }, 1000);
}

function stopTimer() {
  clearInterval(_timerInterval);
}
"""
