/* KCS Capital - listen.js
 * MP3 playback for briefs and research reports with scrubber + time display.
 *
 * For each page, looks for an MP3 at /audio/{slug}.mp3
 * (slug = the page's filename without .html). If the MP3 exists, wires up the
 * Listen button + scrubber. If not, hides the button + controls so they don't appear.
 *
 * Drop a new MP3 into /audio/{slug}.mp3 on any report and the player lights up
 * automatically - no code changes needed.
 */
(function () {
  var btn = document.getElementById('kcs-listen-btn');
  if (!btn) return;

  var label = btn.querySelector('.kcs-listen-label');
  var icon = btn.querySelector('.kcs-listen-icon');
  var speedBtn = document.getElementById('kcs-listen-speed');
  var stopBtn = document.getElementById('kcs-listen-stop');
  var scrub = document.getElementById('kcs-listen-scrub');
  var timeEl = document.getElementById('kcs-listen-time');
  var controls = document.querySelector('.kcs-listen-controls');

  // Derive slug from the page URL
  var path = location.pathname.replace(/^\//, '').replace(/\/$/, '').replace(/\.html$/, '');
  if (!path) { hideUI(); return; }

  var audioUrl = '/audio/' + path + '.mp3';

  function hideUI() {
    if (btn) btn.style.display = 'none';
    if (controls) controls.style.display = 'none';
  }

  function formatTime(secs) {
    if (!isFinite(secs) || secs < 0) return '0:00';
    var m = Math.floor(secs / 60);
    var s = Math.floor(secs % 60);
    return m + ':' + (s < 10 ? '0' : '') + s;
  }

  // HEAD-check whether the audio file exists. If it doesn't, hide the player UI.
  if (!('fetch' in window)) {
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

    var scrubDragging = false;

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
      if (scrub) scrub.value = 0;
      if (timeEl && audio.duration) timeEl.textContent = '0:00 / ' + formatTime(audio.duration);
    });

    // Update time display + scrubber position
    audio.addEventListener('loadedmetadata', function () {
      if (timeEl) timeEl.textContent = '0:00 / ' + formatTime(audio.duration);
    });

    audio.addEventListener('timeupdate', function () {
      if (scrub && audio.duration && !scrubDragging) {
        scrub.value = (audio.currentTime / audio.duration) * 1000;
      }
      if (timeEl && audio.duration) {
        timeEl.textContent = formatTime(audio.currentTime) + ' / ' + formatTime(audio.duration);
      }
    });

    // Scrubber drag-to-seek
    if (scrub) {
      scrub.addEventListener('input', function () {
        scrubDragging = true;
        if (audio.duration) {
          var seekTo = (parseFloat(scrub.value) / 1000) * audio.duration;
          if (timeEl) timeEl.textContent = formatTime(seekTo) + ' / ' + formatTime(audio.duration);
        }
      });
      scrub.addEventListener('change', function () {
        if (audio.duration) {
          audio.currentTime = (parseFloat(scrub.value) / 1000) * audio.duration;
        }
        scrubDragging = false;
      });
      scrub.addEventListener('mouseup', function () { scrubDragging = false; });
      scrub.addEventListener('touchend', function () { scrubDragging = false; });
    }

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
        if (scrub) scrub.value = 0;
        if (timeEl && audio.duration) timeEl.textContent = '0:00 / ' + formatTime(audio.duration);
      });
    }

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
