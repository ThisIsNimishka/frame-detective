"""app/templates/scripts.py — Shared game engine JS."""

SHARED_JS = r"""
/* ══════════════════════════════════════════════════════════════
   FRAME DETECTIVE — GAME ENGINE
   All functions defined here are available to every page.
══════════════════════════════════════════════════════════════ */

/* ── STATE ─────────────────────────────────────────────────── */
var _STATE_KEY = 'fd_state_v3';

function defaultState() {
  return { xp:0, totalXP:0, level:1, hp:3, streak:0, bestStreak:0,
           done:[], badges:[] };
}

function loadState() {
  try {
    var s = JSON.parse(localStorage.getItem(_STATE_KEY));
    return s || defaultState();
  } catch(e) { return defaultState(); }
}

function getState() { return loadState(); }

function saveState(s) {
  try { localStorage.setItem(_STATE_KEY, JSON.stringify(s)); } catch(e){}
}

function clearState() {
  try { localStorage.removeItem(_STATE_KEY); } catch(e){}
}

/* ── XP & LEVELLING ────────────────────────────────────────── */
var _XP_PER_LEVEL = 200;

function addXP(amount) {
  var s = loadState();
  s.xp      = (s.xp      || 0) + amount;
  s.totalXP = (s.totalXP || 0) + amount;
  // level up
  while (s.xp >= _XP_PER_LEVEL) {
    s.xp -= _XP_PER_LEVEL;
    s.level = (s.level || 1) + 1;
    // level-up fanfare
    spawnParticles(window.innerWidth/2, window.innerHeight/2, 30,
          ['#00e5ff','#ffe600','#39ff14','#ffffff']);
    showAchievement('⬆ LEVEL UP!', 'You reached Level ' + s.level + '!');
  }
  saveState(s);
  renderHUD();
  showXPPop('+' + amount + ' XP');
}

function incrementStreak() {
  var s = loadState();
  s.streak = (s.streak || 0) + 1;
  if (s.streak > (s.bestStreak || 0)) s.bestStreak = s.streak;
  saveState(s);
  renderHUD();
  var el = document.getElementById('hud-streak');
  if (el) { el.classList.add('bump'); setTimeout(function(){ el.classList.remove('bump'); }, 350); }
}

function loseHP() {
  var s = loadState();
  s.hp = Math.max(0, (s.hp !== undefined ? s.hp : 3) - 1);
  s.streak = 0;
  saveState(s);
  renderHUD();
  // damage flash
  var fl = document.createElement('div');
  fl.className = 'dmg-flash';
  document.body.appendChild(fl);
  setTimeout(function(){ fl.remove(); }, 450);
  document.body.classList.add('screen-shake');
  setTimeout(function(){ document.body.classList.remove('screen-shake'); }, 450);
}

function markDone(missionId, _unused) {
  var s = loadState();
  if (s.done.indexOf(missionId) === -1) s.done.push(missionId);
  // award badge
  if (s.badges.indexOf(missionId) === -1) s.badges.push(missionId);
  saveState(s);
  renderHUD();
}

/* ── HUD RENDER ────────────────────────────────────────────── */
function renderHUD() {
  var s = loadState();

  /* XP bar */
  var fill = document.getElementById('xp-fill');
  var xpn  = document.getElementById('xp-num');
  if (fill) fill.style.width = Math.min(100, ((s.xp||0) / _XP_PER_LEVEL * 100)) + '%';
  if (xpn)  xpn.textContent  = (s.totalXP||0) + ' XP';

  /* Level badge */
  var lvl = document.getElementById('hud-lvl');
  if (lvl) lvl.textContent = 'LVL ' + (s.level||1);

  /* HP hearts */
  var hp = s.hp !== undefined ? s.hp : 3;
  for (var i = 0; i < 3; i++) {
    var h = document.getElementById('ht' + i);
    if (!h) continue;
    if (i < hp) h.classList.remove('dead');
    else         h.classList.add('dead');
  }

  /* Streak */
  var st = document.getElementById('hud-streak');
  if (st) st.textContent = s.streak || 0;

  /* Badges */
  for (var j = 0; j < 8; j++) {
    var b = document.getElementById('bdg' + j);
    if (!b) continue;
    if (s.badges && s.badges.indexOf(j) !== -1) b.classList.remove('locked');
    else b.classList.add('locked');
  }
}

/* ── TIMER ─────────────────────────────────────────────────── */
var _timerInterval = null;

function startTimer(seconds, onExpire) {
  var remaining = seconds;
  var fill  = document.getElementById('timer-fill');
  var count = document.getElementById('timer-num');
  if (fill)  fill.style.width  = '100%';
  if (count) count.textContent = remaining;

  clearInterval(_timerInterval);
  _timerInterval = setInterval(function() {
    remaining--;
    var pct = Math.max(0, remaining / seconds * 100);
    if (fill)  fill.style.width  = pct + '%';
    if (count) count.textContent = Math.max(0, remaining);
    if (remaining <= 0) {
      clearInterval(_timerInterval);
      if (typeof onExpire === 'function') onExpire();
    }
  }, 1000);
}

function stopTimer() {
  clearInterval(_timerInterval);
}

/* ── TYPEWRITER ────────────────────────────────────────────── */
function initTypewriters() {
  document.querySelectorAll('[data-tw]').forEach(function(el) {
    var text  = el.getAttribute('data-tw');
    var cur   = document.createElement('span');
    cur.className = 'tw-cursor';
    el.textContent = '';
    el.appendChild(cur);
    var i = 0;
    var iv = setInterval(function() {
      if (i >= text.length) { clearInterval(iv); cur.remove(); return; }
      el.insertBefore(document.createTextNode(text[i++]), cur);
    }, 28);
  });
}

/* ── SOUND (no-op stubs — ready for Web Audio expansion) ───── */
function playSound(name) {
  /* sounds would be added here with Web Audio API */
}

/* ── FX: PARTICLES ─────────────────────────────────────────── */
function spawnParticles(x, y, n, colors) {
  for (var i = 0; i < (n||20); i++) {
    var p   = document.createElement('div');
    var ang = Math.random() * Math.PI * 2;
    var spd = 60 + Math.random() * 80;
    var sz  = 4 + Math.random() * 5;
    p.className = 'particle';
    p.style.cssText = 'width:' + sz + 'px;height:' + sz + 'px;' +
      'left:' + x + 'px;top:' + y + 'px;' +
      'background:' + colors[Math.floor(Math.random()*colors.length)] + ';' +
      '--px:' + (Math.cos(ang)*spd).toFixed(1) + 'px;' +
      '--py:' + (Math.sin(ang)*spd - 60).toFixed(1) + 'px;' +
      '--pt:' + (.6 + Math.random()*.6).toFixed(2) + 's;';
    document.body.appendChild(p);
    setTimeout(function(el){ return function(){ el.remove(); }; }(p), 1400);
  }
}

/* ── FX: CONFETTI ──────────────────────────────────────────── */
function spawnConfetti() {
  var colors = ['#00e5ff','#ffe600','#39ff14','#ff2244','#bf5fff','#ff8c00'];
  for (var i = 0; i < 60; i++) {
    var c = document.createElement('div');
    c.className = 'confetti-bit';
    c.style.cssText =
      'left:' + (10 + Math.random()*80) + 'vw;' +
      'top:' + (Math.random()*30) + 'vh;' +
      'background:' + colors[Math.floor(Math.random()*colors.length)] + ';' +
      '--cx:' + (-50+Math.random()*100).toFixed(1) + 'px;' +
      '--cy:' + (120+Math.random()*200).toFixed(1) + 'px;' +
      '--ct:' + (1.1+Math.random()*.8).toFixed(2) + 's;' +
      '--cd:' + (Math.random()*.6).toFixed(2) + 's;';
    document.body.appendChild(c);
    setTimeout(function(el){ return function(){ el.remove(); }; }(c), 2200);
  }
}

/* ── XP POPUP ──────────────────────────────────────────────── */
function showXPPop(text) {
  var el = document.createElement('div');
  el.className = 'xp-popup';
  el.textContent = text;
  document.body.appendChild(el);
  setTimeout(function(){ el.remove(); }, 2200);
}

/* ── ACHIEVEMENT TOAST ─────────────────────────────────────── */
function showAchievement(title, body) {
  var t = document.createElement('div');
  t.className = 'toast';
  t.innerHTML = '<div class="toast-head">' + title + '</div>' +
                '<div class="toast-body">' + body  + '</div>';
  document.body.appendChild(t);
  setTimeout(function(){ t.style.opacity='0'; t.style.transform='translateX(28px)'; t.style.transition='all .3s'; }, 3000);
  setTimeout(function(){ t.remove(); }, 3400);
}

/* ── PAGE NAVIGATION (with veil transition) ─────────────────── */
function navigateTo(url) {
  var veil = document.getElementById('page-veil');
  if (veil) {
    veil.classList.add('out');
    setTimeout(function(){ window.location.href = url; }, 340);
  } else {
    window.location.href = url;
  }
}

/* Intercept all link clicks for smooth transition */
document.addEventListener('click', function(e) {
  var a = e.target.closest('a[href]');
  if (!a) return;
  var href = a.getAttribute('href');
  if (!href || href[0] === '#') return;
  if (href.indexOf('mailto:') === 0 || href.indexOf('javascript:') === 0) return;
  if (href.indexOf('http') === 0 && href.indexOf(location.origin) !== 0) return;
  e.preventDefault();
  navigateTo(href);
}, true);
"""
