"""app/templates/scripts.py — Shared game engine JS."""

SHARED_JS = r"""
/* ══════════════════════════════════════════════════════════════
   FRAME DETECTIVE — GAME ENGINE
══════════════════════════════════════════════════════════════ */

/* ── SOUND ENGINE (Synthesized via Web Audio) ── */
var _audioCtx = null;
function initAudio() { if (!_audioCtx) _audioCtx = new (window.AudioContext || window.webkitAudioContext)(); }

function playSynth(freq, type, dur, vol, slide) {
  try {
    initAudio();
    if (_audioCtx.state === 'suspended') _audioCtx.resume();
    var osc = _audioCtx.createOscillator();
    var gain = _audioCtx.createGain();
    osc.type = type || 'sine';
    osc.frequency.setValueAtTime(freq, _audioCtx.currentTime);
    if (slide) osc.frequency.exponentialRampToValueAtTime(slide, _audioCtx.currentTime + dur);
    gain.gain.setValueAtTime(vol || 0.1, _audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.0001, _audioCtx.currentTime + dur);
    osc.connect(gain); gain.connect(_audioCtx.destination);
    osc.start(); osc.stop(_audioCtx.currentTime + dur);
  } catch(e) {}
}

function playSound(name) {
  if (name === 'click')      playSynth(440, 'square', 0.05, 0.05);
  if (name === 'correct')    { playSynth(523, 'sine', 0.1, 0.1); setTimeout(function(){ playSynth(659, 'sine', 0.1, 0.1); }, 80); setTimeout(function(){ playSynth(783, 'sine', 0.2, 0.1); }, 160); }
  if (name === 'wrong')      playSynth(150, 'sawtooth', 0.4, 0.1, 50);
  if (name === 'levelup')    for(var i=0; i<4; i++) setTimeout(function(f){ return function(){ playSynth(f, 'square', 0.15, 0.08); }; }(440 + i*110), i*100);
  if (name === 'achievement') { playSynth(880, 'sine', 0.1, 0.1); setTimeout(function(){ playSynth(1174, 'sine', 0.3, 0.1); }, 100); }
}

/* ── STATE ── */
var _STATE_KEY = 'fd_state_v3';
function defaultState() { return { xp:0, totalXP:0, level:1, hp:3, streak:0, bestStreak:0, done:[], badges:[] }; }
function loadState() { try { var s = JSON.parse(localStorage.getItem(_STATE_KEY)); return s || defaultState(); } catch(e) { return defaultState(); } }
function getState() { return loadState(); }
function saveState(s) { try { localStorage.setItem(_STATE_KEY, JSON.stringify(s)); } catch(e){} }
function clearState() { try { localStorage.removeItem(_STATE_KEY); } catch(e){} }

/* ── XP & LEVELLING ── */
var _XP_PER_LEVEL = 200;
function addXP(amount) {
  var s = loadState();
  s.xp = (s.xp||0) + amount; s.totalXP = (s.totalXP||0) + amount;
  while (s.xp >= _XP_PER_LEVEL) {
    s.xp -= _XP_PER_LEVEL; s.level = (s.level||1) + 1;
    spawnParticles(window.innerWidth/2, window.innerHeight/2, 30, ['#00e5ff','#ffe600','#39ff14','#ffffff']);
    showAchievement('⬆ LEVEL UP!', 'You reached Level ' + s.level + '!');
    playSound('levelup');
  }
  saveState(s); renderHUD(); showXPPop('+' + amount + ' XP');
}
function incrementStreak() {
  var s = loadState(); s.streak = (s.streak||0) + 1;
  if (s.streak > (s.bestStreak || 0)) s.bestStreak = s.streak;
  saveState(s); renderHUD();
  var el = document.getElementById('hud-streak');
  if (el) { el.classList.add('bump'); setTimeout(function(){ el.classList.remove('bump'); }, 350); }
}
function loseHP() {
  var s = loadState(); s.hp = Math.max(0, (s.hp !== undefined ? s.hp : 3) - 1); s.streak = 0;
  saveState(s); renderHUD();
  playSound('wrong');
  var fl = document.createElement('div'); fl.className = 'dmg-flash'; document.body.appendChild(fl);
  setTimeout(function(){ fl.remove(); }, 450);
  document.body.classList.add('screen-shake'); setTimeout(function(){ document.body.classList.remove('screen-shake'); }, 450);
}
function markDone(missionId) {
  var s = loadState(); if (s.done.indexOf(missionId) === -1) s.done.push(missionId);
  if (s.badges.indexOf(missionId) === -1) s.badges.push(missionId);
  saveState(s); renderHUD();
}

/* ── HUD ── */
function renderHUD() {
  var s = loadState();
  var fill = document.getElementById('xp-fill');
  var xpn = document.getElementById('xp-num');
  if (fill) fill.style.width = Math.min(100, ((s.xp||0) / _XP_PER_LEVEL * 100)) + '%';
  if (xpn) xpn.textContent = (s.totalXP||0) + ' XP';
  var lvl = document.getElementById('hud-lvl');
  if (lvl) lvl.textContent = 'LVL ' + (s.level||1);
  var hp = s.hp !== undefined ? s.hp : 3;
  for (var i = 0; i < 3; i++) {
    var h = document.getElementById('ht' + i);
    if (h) { if (i < hp) h.classList.remove('dead'); else h.classList.add('dead'); }
  }
  var st = document.getElementById('hud-streak');
  if (st) st.textContent = s.streak || 0;
  for (var j = 0; j < 8; j++) {
    var b = document.getElementById('bdg' + j);
    if (b) { if (s.badges && s.badges.indexOf(j) !== -1) b.classList.remove('locked'); else b.classList.add('locked'); }
  }
}

/* ── TIMER ── */
var _timerInterval = null;
function startTimer(seconds, onExpire) {
  var remaining = seconds;
  var fill = document.getElementById('timer-fill');
  var count = document.getElementById('timer-num');
  if (fill) fill.style.width = '100%';
  if (count) count.textContent = remaining;
  clearInterval(_timerInterval);
  _timerInterval = setInterval(function() {
    remaining--;
    var pct = Math.max(0, remaining / seconds * 100);
    if (fill) fill.style.width = pct + '%';
    if (count) count.textContent = Math.max(0, remaining);
    if (remaining <= 0) { clearInterval(_timerInterval); if (typeof onExpire === 'function') onExpire(); }
  }, 1000);
}
function stopTimer() { clearInterval(_timerInterval); }

/* ── QUIZ ENGINE ── */
var _currentQuiz = { answered: false, startTime: 0 };

function initQuiz(missionId, options, nextPage, baseXP, factHtml) {
  _currentQuiz = { 
    mid: missionId, opts: options, next: nextPage, 
    xp: baseXP, fact: factHtml, answered: false, 
    t0: Date.now() 
  };
  
  var buttons = document.querySelectorAll('.qbtn');
  buttons.forEach(function(btn, i) {
    btn.onclick = function() { handleQuizAnswer(i); };
  });

  document.onkeydown = function(e) {
    if (_currentQuiz.answered) return;
    var k = e.key.toLowerCase();
    var idx = {'a':0,'b':1,'c':2,'d':3,'1':0,'2':1,'3':2,'4':3}[k];
    if (idx !== undefined && buttons[idx]) buttons[idx].click();
  };

  setTimeout(function() {
    var hp = document.getElementById('hint-panel');
    if (hp && !_currentQuiz.answered) hp.classList.add('show');
  }, 20000);

  startTimer(60, function() {
    if (!_currentQuiz.answered && buttons[0]) buttons[0].click();
  });
}

function handleQuizAnswer(idx) {
  if (_currentQuiz.answered) return;
  _currentQuiz.answered = true;
  stopTimer();

  var btn = document.querySelectorAll('.qbtn')[idx];
  var correct = _currentQuiz.opts[idx].correct;
  var elapsed = (Date.now() - _currentQuiz.t0) / 1000;
  var speedBonus = elapsed < 25 ? 25 : 0;
  
  var fb = document.getElementById('quiz-feedback');
  var nx = document.getElementById('next-bar');
  var hp = document.getElementById('boss-hp-bar');

  document.querySelectorAll('.qbtn').forEach(function(b, i) {
    b.disabled = true;
    if (_currentQuiz.opts[i].correct) b.classList.add('correct');
  });

  if (correct) {
    btn.classList.add('correct');
    playSound('correct');
    addXP(_currentQuiz.xp + 50 + speedBonus);
    incrementStreak();
    markDone(_currentQuiz.mid);
    if (hp) hp.style.width = '0%';
    spawnParticles(btn.getBoundingClientRect().left + btn.offsetWidth/2, btn.getBoundingClientRect().top + window.scrollY, 25, ['#39ff14','#00e5ff','#ffffff']);
    if (fb) {
      fb.className = 'quiz-feedback win'; fb.style.display = 'block';
      fb.innerHTML = '<strong>✅ CORRECT!</strong>' + (speedBonus ? ' <span style="color:var(--yellow)">⚡ +' + speedBonus + ' SPEED BONUS!</span>' : '') + '<br>' + (window.QUIZ_WIN[_currentQuiz.mid] || '') + (_currentQuiz.fact || '');
    }
  } else {
    btn.classList.add('wrong');
    loseHP();
    markDone(_currentQuiz.mid);
    if (fb) {
      fb.className = 'quiz-feedback lose'; fb.style.display = 'block';
      fb.innerHTML = '<strong>❌ WRONG.</strong><br>' + (window.QUIZ_LOSE[_currentQuiz.mid] || '') + (_currentQuiz.fact || '');
    }
  }
  if (nx) nx.style.display = 'block';
}

/* ── UTILS ── */
function initTypewriters() {
  document.querySelectorAll('[data-tw]').forEach(function(el) {
    var text = el.getAttribute('data-tw'); var i = 0; el.textContent = '';
    var iv = setInterval(function() {
      if (i >= text.length) { clearInterval(iv); return; }
      el.appendChild(document.createTextNode(text[i++]));
    }, 25);
  });
}
function spawnParticles(x, y, n, colors) {
  for (var i = 0; i < n; i++) {
    var p = document.createElement('div'); var ang = Math.random()*Math.PI*2; var spd = 60+Math.random()*80;
    p.className = 'particle';
    p.style.cssText = 'left:'+x+'px;top:'+y+'px;background:'+colors[Math.floor(Math.random()*colors.length)]+';--px:'+(Math.cos(ang)*spd)+'px;--py:'+(Math.sin(ang)*spd-60)+'px;--pt:'+(.6+Math.random()*.6)+'s;';
    document.body.appendChild(p); setTimeout(function(el){ return function(){ el.remove(); }; }(p), 1200);
  }
}
function spawnConfetti() {
  var colors = ['#00e5ff','#ffe600','#39ff14','#ff2244'];
  for (var i = 0; i < 50; i++) {
    var c = document.createElement('div'); c.className = 'confetti-bit';
    c.style.cssText = 'left:'+(10+Math.random()*80)+'vw;top:'+(Math.random()*20)+'vh;background:'+colors[Math.floor(Math.random()*colors.length)]+';--cx:'+(-50+Math.random()*100)+'px;--cy:'+(150+Math.random()*150)+'px;--ct:'+(1+Math.random())+'s;--cd:'+(Math.random()*.5)+'s;';
    document.body.appendChild(c); setTimeout(function(el){ return function(){ el.remove(); }; }(c), 2000);
  }
}
function showXPPop(t) { var e = document.createElement('div'); e.className = 'xp-popup'; e.textContent = t; document.body.appendChild(e); setTimeout(function(){ e.remove(); }, 2000); }
function showAchievement(t, b) {
  playSound('achievement');
  var e = document.createElement('div'); e.className = 'toast'; e.innerHTML = '<div class="toast-head">'+t+'</div><div class="toast-body">'+b+'</div>';
  document.body.appendChild(e); setTimeout(function(){ e.style.opacity='0'; }, 3000); setTimeout(function(){ e.remove(); }, 3400);
}
function navigateTo(url) {
  var v = document.getElementById('page-veil');
  if (v) { v.classList.add('out'); setTimeout(function(){ window.location.href = url; }, 320); }
  else { window.location.href = url; }
}
document.addEventListener('click', function(e) {
  playSound('click');
  var a = e.target.closest('a[href]'); if (!a) return;
  var h = a.getAttribute('href'); if (!h || h[0]==='#' || h.indexOf('http')===0 && h.indexOf(location.origin)!==0) return;
  e.preventDefault(); navigateTo(h);
}, true);
"""
