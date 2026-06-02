/* KCS Capital — listen.js
 * MP3 playback for briefs and research reports.
 *
 * For each page, looks for an MP3 at /audio/{slug}.mp3
 * (slug = the page's filename without .html). If the MP3 exists, wires up the
 * Listen button. If not, hides the button + controls so they don't appear at all.
 *
 * Drop a new MP3 into /audio/{slug}.mp3 on any report and the player lights up
 * automatically — no code changes needed.
 */
(function () {
  var btn = document.getElementById('kcs-listen-btn');
  if (!btn) return;

  var label = btn.querySelector('.kcs-listen-label');
  var icon = btn.querySelector('.kcs-listen-icon');
  var speedBtn = document.getElementById('kcs-listen-speed');
  var stopBtn = document.getElementById('kcs-listen-stop');
  var controls = document.querySelector('.kcs-listen-controls');

  // Derive slug from the page URL
  var path = location.pathname.replace(/^\//, '').replace(/\/$/, '').replace(/\.html$/, '');
  if (!path) {
    hideUI();
    return;
  }

  var audioUrl = '/audio/' + path + '.mp3';

  function hideUI() {
    if (btn) btn.style.display = 'none';
    if (controls) controls.style.display = 'none';
  }

  // HEAD-check whether the audio file exists. If it doesn't, hide the player UI.
  if (!('fetch' in window)) {
    // Old browser fallback: just try to load and let error handler hide it
    initPlayer();
    return;
  }

  fetch(audioUrl, { method: 'HEAD' }).then(function (res) {
    if (res && res.ok) {
      initPlayer();
    } else {
      hideUI();
    }
  }).catch(function () {
    hideUI();
  });

  function initPlayer() {
    var audio = new Audio();
    audio.preload = 'metadata';
    audio.src = audioUrl;

    // Fallback: if the file can't actually load (404 / blocked / bad CORS), hide the UI
    audio.addEventListener('error', function () {
      hideUI();
    });

    btn.addEventListener('click', function (e) {
      e.preventDefault();
      if (audio.paused) {
        audio.play().catch(function () {});
      } else {
        audio.pause();
      }
    });

    audio.addEventListener('play', function () {
      btn.classList.add('playing');
      if (label) label.textContent = 'Pause';
      if (icon) icon.textContent = '❚❚';
      if (controls) controls.classList.add('kcs-listen-active');
    });

    audio.addEventListener('pause', function () {
      // If user paused mid-track, show Resume. If at the end, show Listen.
      if (audio.currentTime > 0 && !audio.ended) {
        btn.classList.remove('playing');
        if (label) label.textContent = 'Resume';
        if (icon) icon.textContent = '▶';
      }
    });

    audio.addEventListener('ended', function () {
      audio.currentTime = 0;
      btn.classList.remove('playing');
      if (label) label.textContent = 'Listen';
      if (icon) icon.textContent = '▶';
      if (controls) controls.classList.remove('kcs-listen-active');
    });

    if (speedBtn) {
      speedBtn.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        var speeds = [1.0, 1.25, 1.5, 1.75, 0.75];
        var current = audio.playbackRate || 1.0;
        var i = -1;
        for (var k = 0; k < speeds.length; k++) {
          if (Math.abs(speeds[k] - current) < 0.001) { i = k; break; }
        }
        var nextRate = speeds[(i + 1) % speeds.length];
        audio.playbackRate = nextRate;
        speedBtn.textContent = nextRate + 'x';
      });
    }

    if (stopBtn) {
      stopBtn.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        audio.pause();
        audio.currentTime = 0;
        btn.classList.remove('playing');
        if (label) label.textContent = 'Listen';
        if (icon) icon.textContent = '▶';
        if (controls) controls.classList.remove('kcs-listen-active');
      });
    }

    // Pause when user switches tabs or navigates away
    document.addEventListener('visibilitychange', function () {
      if (document.hidden && !audio.paused) {
        audio.pause();
      }
    });

    window.addEventListener('beforeunload', function () {
      try { audio.pause(); } catch (e) {}
    });
  }
})();
