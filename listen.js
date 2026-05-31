/* KCS Capital — listen.js
 * Native Web Speech API text-to-speech for briefs and research reports.
 * Reads the .prose body, skips nav/sidebar/footer/sources/disclaimer.
 * Play / Pause / Resume / Stop, plus speed cycling (1x → 1.25x → 1.5x → 1.75x → 0.75x).
 * Works on iOS Safari (Siri voices), Android Chrome (Google voices), desktop browsers.
 */
(function () {
  if (typeof window === 'undefined' || !('speechSynthesis' in window) || typeof SpeechSynthesisUtterance === 'undefined') {
    var unsupported = document.getElementById('kcs-listen-btn');
    if (unsupported) unsupported.style.display = 'none';
    return;
  }

  var btn = document.getElementById('kcs-listen-btn');
  if (!btn) return;
  var label = btn.querySelector('.kcs-listen-label');
  var icon = btn.querySelector('.kcs-listen-icon');
  var speedBtn = document.getElementById('kcs-listen-speed');
  var stopBtn = document.getElementById('kcs-listen-stop');
  var controls = document.querySelector('.kcs-listen-controls');

  var chunks = [];
  var currentIndex = 0;
  var state = 'idle'; // idle | playing | paused
  var voice = null;
  var rate = 1.0;

  function pickVoice() {
    var voices = window.speechSynthesis.getVoices() || [];
    if (!voices.length) return;
    // Preference order: enhanced/natural en-US -> Google en-US -> any en-US -> any en -> first
    voice = voices.find(function (v) { return /en[-_]US/i.test(v.lang) && /(enhanced|premium|natural|siri|samantha|alex)/i.test(v.name); })
         || voices.find(function (v) { return /en[-_]US/i.test(v.lang) && /Google/i.test(v.name); })
         || voices.find(function (v) { return /en[-_](US|CA|GB)/i.test(v.lang); })
         || voices.find(function (v) { return /^en/i.test(v.lang); })
         || voices[0];
  }

  // iOS Safari and Chrome sometimes return [] on first call; voiceschanged fires later
  window.speechSynthesis.onvoiceschanged = pickVoice;
  pickVoice();

  function buildChunks() {
    var prose = document.querySelector('.prose');
    if (!prose) return [];
    var text = '';
    var els = prose.querySelectorAll('p, h2, h3, li');
    Array.prototype.forEach.call(els, function (el) {
      // Skip TOC, sources, disclaimer, sidebar bits
      if (el.closest('.brief-toc-aside') || el.closest('.brief-toc') || el.closest('.brief-sources') ||
          el.closest('.research-sidebar') || el.closest('.brief-sidebar') ||
          el.classList.contains('brief-disclaimer')) return;
      var txt = (el.textContent || '').replace(/\s+/g, ' ').trim();
      if (!txt) return;
      // Add a period if the chunk doesn't end with sentence punctuation, so TTS pauses correctly
      if (!/[.!?:;]$/.test(txt)) txt += '.';
      text += txt + ' ';
    });

    // Split into smaller utterances (~200 chars at sentence boundaries) — many browsers truncate long utterances
    var sentences = text.split(/(?<=[.!?])\s+/);
    var arr = [];
    var current = '';
    sentences.forEach(function (s) {
      if ((current.length + s.length) > 200 && current.length) {
        arr.push(current);
        current = s;
      } else {
        current += (current ? ' ' : '') + s;
      }
    });
    if (current) arr.push(current);
    return arr;
  }

  // Chrome (and some other browsers) stop TTS after ~15 seconds. Pause/resume every 13 seconds keeps it alive.
  setInterval(function () {
    if (state === 'playing' && window.speechSynthesis.speaking) {
      window.speechSynthesis.pause();
      window.speechSynthesis.resume();
    }
  }, 13000);

  function speakNext() {
    if (currentIndex >= chunks.length) {
      stopAll();
      return;
    }
    var u = new SpeechSynthesisUtterance(chunks[currentIndex]);
    if (voice) u.voice = voice;
    u.rate = rate;
    u.pitch = 1.0;
    u.onend = function () {
      currentIndex++;
      if (state === 'playing') speakNext();
    };
    u.onerror = function () {
      currentIndex++;
      if (state === 'playing') speakNext();
    };
    window.speechSynthesis.speak(u);
  }

  function setUiPlaying() {
    btn.classList.add('playing');
    if (label) label.textContent = 'Pause';
    if (icon) icon.textContent = '❚❚';
    if (controls) controls.classList.add('kcs-listen-active');
  }

  function setUiPaused() {
    btn.classList.remove('playing');
    if (label) label.textContent = 'Resume';
    if (icon) icon.textContent = '▶';
  }

  function setUiIdle() {
    btn.classList.remove('playing');
    if (label) label.textContent = 'Listen';
    if (icon) icon.textContent = '▶';
    if (controls) controls.classList.remove('kcs-listen-active');
  }

  function play() {
    // Try to pick a voice again in case voices weren't loaded on first call
    if (!voice) pickVoice();
    if (!chunks.length) chunks = buildChunks();
    if (!chunks.length) return;
    state = 'playing';
    setUiPlaying();
    speakNext();
  }

  function pause() {
    state = 'paused';
    setUiPaused();
    try { window.speechSynthesis.pause(); } catch (e) {}
  }

  function resume() {
    state = 'playing';
    setUiPlaying();
    try { window.speechSynthesis.resume(); } catch (e) {}
  }

  function stopAll() {
    state = 'idle';
    currentIndex = 0;
    setUiIdle();
    try { window.speechSynthesis.cancel(); } catch (e) {}
  }

  window.kcsToggleListen = function () {
    if (state === 'idle') play();
    else if (state === 'playing') pause();
    else if (state === 'paused') resume();
  };

  if (speedBtn) {
    speedBtn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      var speeds = [1.0, 1.25, 1.5, 1.75, 0.75];
      var i = speeds.indexOf(rate);
      if (i < 0) i = 0;
      rate = speeds[(i + 1) % speeds.length];
      speedBtn.textContent = rate + 'x';
      // If currently playing, restart current chunk at new rate
      if (state === 'playing') {
        try { window.speechSynthesis.cancel(); } catch (e) {}
        speakNext();
      }
    });
  }

  if (stopBtn) {
    stopBtn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      stopAll();
    });
  }

  // Stop TTS if the user navigates away or switches tabs
  window.addEventListener('beforeunload', stopAll);
  document.addEventListener('visibilitychange', function () {
    if (document.hidden && state === 'playing') pause();
  });
})();
