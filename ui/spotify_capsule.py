"""Spotify-inspired 8-bit neon capsule component for Streamlit."""

from __future__ import annotations

from base64 import b64encode
import json
import mimetypes
from pathlib import Path
from typing import Any

import streamlit.components.v1 as streamlit_components

from logger.logger import log_critical_error


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_COMPONENT_HEIGHT = 760


def render_spotify_8bit_player(config: dict[str, Any]) -> None:
    """Render the Spotify-inspired capsule as an isolated HTML component."""
    streamlit_components.html(
        build_spotify_8bit_player_html(config),
        height=DEFAULT_COMPONENT_HEIGHT,
        scrolling=False,
    )


def build_spotify_8bit_player_html(config: dict[str, Any]) -> str:
    """Build the isolated HTML/CSS/JS for the Spotify capsule."""
    component_config = _build_component_config(config)
    json_config = _json_for_script(component_config)

    return f"""
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap" rel="stylesheet">
  <style>
    :root {{
      --neon-pink: #ff007f;
      --soft-pink: #ffd1ea;
      --deep-pink: #b0005a;
      --white-glass: rgba(255, 255, 255, 0.16);
      --dark-panel: rgba(35, 10, 28, 0.55);
      --ink: #fff7fc;
      --mint: #7dffda;
      --amber: #ffd166;
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      background: transparent;
      color: var(--ink);
      font-family: "VT323", monospace;
      letter-spacing: 0;
    }}

    .spotify-capsule-shell {{
      width: min(100%, 760px);
      margin: 0 auto;
      padding: 20px 12px 34px;
    }}

    .capsule-trigger {{
      width: min(100%, 360px);
      min-height: 48px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      margin: 0 auto 18px;
      border: 2px solid var(--neon-pink);
      border-radius: 6px;
      background:
        linear-gradient(180deg, rgba(255, 255, 255, 0.20), rgba(255, 0, 127, 0.18)),
        rgba(35, 10, 28, 0.78);
      color: var(--soft-pink);
      cursor: pointer;
      font-family: "Press Start 2P", monospace;
      font-size: clamp(10px, 2.4vw, 12px);
      line-height: 1.4;
      text-transform: uppercase;
      box-shadow:
        0 0 0 2px rgba(255, 209, 234, 0.12) inset,
        0 0 16px rgba(255, 0, 127, 0.58),
        0 0 38px rgba(255, 0, 127, 0.34);
      text-shadow: 0 0 10px rgba(255, 209, 234, 0.82);
    }}

    .capsule-trigger:hover {{
      transform: translateY(-1px);
      box-shadow:
        0 0 0 2px rgba(255, 209, 234, 0.18) inset,
        0 0 20px rgba(255, 0, 127, 0.70),
        0 0 46px rgba(255, 0, 127, 0.42);
    }}

    .capsule-player {{
      position: relative;
      display: none;
      overflow: hidden;
      min-height: 640px;
      padding: clamp(18px, 4vw, 32px);
      border: 2px solid var(--neon-pink);
      border-radius: 8px;
      background:
        linear-gradient(135deg, rgba(255, 255, 255, 0.20), rgba(255, 255, 255, 0.05)),
        radial-gradient(circle at 50% 0%, rgba(255, 0, 127, 0.40), transparent 36%),
        linear-gradient(180deg, rgba(20, 4, 18, 0.84), rgba(62, 10, 47, 0.66));
      backdrop-filter: blur(18px);
      -webkit-backdrop-filter: blur(18px);
      box-shadow:
        0 0 0 1px rgba(255, 209, 234, 0.22) inset,
        0 0 28px rgba(255, 0, 127, 0.70),
        0 0 80px rgba(255, 0, 127, 0.34),
        0 30px 80px rgba(20, 4, 18, 0.46);
    }}

    .spotify-capsule-shell.is-open .capsule-player {{
      display: block;
      animation: capsule-boot 360ms steps(4, end);
    }}

    .capsule-player::before {{
      content: "";
      position: absolute;
      inset: 0;
      pointer-events: none;
      background:
        repeating-linear-gradient(
          180deg,
          rgba(255, 255, 255, 0.07) 0,
          rgba(255, 255, 255, 0.07) 1px,
          transparent 1px,
          transparent 5px
        );
      mix-blend-mode: screen;
      opacity: 0.28;
    }}

    .capsule-player::after {{
      content: "";
      position: absolute;
      left: 16%;
      right: 16%;
      bottom: 10px;
      height: 22px;
      border: 1px solid rgba(255, 0, 127, 0.86);
      border-radius: 4px;
      background:
        linear-gradient(180deg, rgba(255, 209, 234, 0.20), rgba(255, 0, 127, 0.34)),
        rgba(22, 4, 18, 0.82);
      box-shadow:
        0 0 16px rgba(255, 0, 127, 0.78),
        0 12px 34px rgba(255, 0, 127, 0.42);
    }}

    .capsule-content {{
      position: relative;
      z-index: 1;
      display: grid;
      gap: 18px;
    }}

    .capsule-top {{
      display: grid;
      grid-template-columns: minmax(160px, 240px) minmax(0, 1fr);
      gap: clamp(16px, 4vw, 28px);
      align-items: center;
    }}

    .cover-frame {{
      position: relative;
      aspect-ratio: 1;
      border: 2px solid rgba(255, 209, 234, 0.82);
      border-radius: 6px;
      background:
        linear-gradient(135deg, rgba(255, 0, 127, 0.34), rgba(125, 255, 218, 0.16)),
        rgba(20, 4, 18, 0.78);
      box-shadow:
        0 0 16px rgba(255, 0, 127, 0.72),
        0 0 44px rgba(255, 0, 127, 0.42),
        inset 0 0 28px rgba(255, 255, 255, 0.10);
      overflow: hidden;
    }}

    .spotify-cover-img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      image-rendering: pixelated;
      opacity: 1;
      transform: scale(1);
      filter:
        saturate(1.15)
        contrast(1.08)
        drop-shadow(0 0 14px rgba(255, 0, 127, 0.68));
      transition:
        opacity 420ms ease,
        filter 420ms ease,
        transform 420ms ease;
    }}

    .spotify-cover-img.is-changing {{
      opacity: 0.35;
      transform: scale(1.015);
      filter:
        blur(1px)
        saturate(1.22)
        contrast(1.12)
        drop-shadow(0 0 18px rgba(255, 0, 127, 0.95));
    }}

    .cover-frame.is-glowing {{
      box-shadow:
        0 0 22px rgba(255, 0, 127, 0.86),
        0 0 58px rgba(255, 0, 127, 0.54),
        inset 0 0 34px rgba(255, 255, 255, 0.14);
    }}

    .cover-placeholder {{
      height: 100%;
      display: grid;
      place-items: center;
      padding: 18px;
      color: var(--soft-pink);
      font-family: "Press Start 2P", monospace;
      font-size: 12px;
      line-height: 1.7;
      text-align: center;
      text-shadow: 0 0 12px rgba(255, 0, 127, 0.90);
    }}

    .song-meta {{
      min-width: 0;
    }}

    .badge {{
      display: inline-flex;
      max-width: 100%;
      padding: 8px 10px;
      border: 1px solid rgba(125, 255, 218, 0.86);
      border-radius: 4px;
      color: var(--mint);
      background: rgba(9, 35, 30, 0.42);
      font-family: "Press Start 2P", monospace;
      font-size: clamp(9px, 2vw, 11px);
      line-height: 1.45;
      overflow-wrap: anywhere;
      text-shadow: 0 0 10px rgba(125, 255, 218, 0.70);
    }}

    .song-title {{
      margin: 18px 0 8px;
      color: var(--soft-pink);
      font-family: "Press Start 2P", monospace;
      font-size: clamp(18px, 5vw, 36px);
      line-height: 1.25;
      overflow-wrap: anywhere;
      text-shadow:
        0 0 10px rgba(255, 209, 234, 0.85),
        0 0 26px rgba(255, 0, 127, 0.72);
    }}

    .song-artist {{
      color: #ffffff;
      font-size: clamp(28px, 6vw, 42px);
      line-height: 1;
      text-shadow: 0 0 14px rgba(255, 0, 127, 0.72);
    }}

    .waveform {{
      height: 74px;
      display: grid;
      grid-template-columns: repeat(28, 1fr);
      align-items: end;
      gap: 5px;
      padding: 12px;
      border: 1px solid rgba(255, 209, 234, 0.34);
      border-radius: 6px;
      background: rgba(20, 4, 18, 0.44);
      box-shadow: inset 0 0 20px rgba(255, 0, 127, 0.16);
    }}

    .waveform span {{
      height: calc(var(--bar-height) * 1%);
      min-height: 8px;
      background: linear-gradient(180deg, var(--soft-pink), var(--neon-pink));
      border-radius: 2px 2px 0 0;
      box-shadow: 0 0 10px rgba(255, 0, 127, 0.70);
      opacity: 0.62;
      transform-origin: bottom;
    }}

    .is-playing .waveform span {{
      animation: pixel-wave 720ms steps(3, end) infinite;
      animation-delay: calc(var(--bar-index) * -42ms);
      opacity: 1;
    }}

    .progress-panel {{
      display: grid;
      gap: 8px;
    }}

    .progress-track {{
      height: 16px;
      overflow: hidden;
      border: 1px solid rgba(255, 209, 234, 0.78);
      border-radius: 3px;
      background: rgba(20, 4, 18, 0.68);
      box-shadow: inset 0 0 14px rgba(255, 0, 127, 0.22);
    }}

    .progress-fill {{
      width: 0%;
      height: 100%;
      background:
        repeating-linear-gradient(
          90deg,
          var(--neon-pink) 0 10px,
          var(--soft-pink) 10px 14px
        );
      box-shadow: 0 0 16px rgba(255, 0, 127, 0.86);
      transition: width 120ms linear;
    }}

    .time-row {{
      display: flex;
      justify-content: space-between;
      gap: 12px;
      color: var(--soft-pink);
      font-family: "Press Start 2P", monospace;
      font-size: 10px;
      line-height: 1.4;
    }}

    .control-row {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
    }}

    .arcade-button {{
      min-height: 48px;
      border: 2px solid rgba(255, 209, 234, 0.72);
      border-radius: 5px;
      background:
        linear-gradient(180deg, rgba(255, 209, 234, 0.24), rgba(255, 0, 127, 0.28)),
        rgba(20, 4, 18, 0.74);
      color: #ffffff;
      cursor: pointer;
      font-family: "Press Start 2P", monospace;
      font-size: clamp(10px, 2vw, 12px);
      line-height: 1.3;
      text-shadow: 0 0 10px rgba(255, 209, 234, 0.90);
      box-shadow:
        0 4px 0 rgba(130, 0, 70, 0.92),
        0 0 16px rgba(255, 0, 127, 0.46);
    }}

    .arcade-button:disabled {{
      cursor: not-allowed;
      opacity: 0.56;
      filter: grayscale(0.45);
    }}

    .arcade-button:not(:disabled):active {{
      transform: translateY(3px);
      box-shadow:
        0 1px 0 rgba(130, 0, 70, 0.92),
        0 0 12px rgba(255, 0, 127, 0.40);
    }}

    .lyric-box {{
      min-height: 112px;
      padding: 16px;
      border: 2px solid rgba(255, 209, 234, 0.50);
      border-radius: 6px;
      background:
        linear-gradient(180deg, rgba(255, 255, 255, 0.10), rgba(255, 0, 127, 0.08)),
        rgba(20, 4, 18, 0.66);
      box-shadow:
        inset 0 0 26px rgba(255, 0, 127, 0.16),
        0 0 18px rgba(255, 0, 127, 0.22);
    }}

    .dialog-label {{
      margin-bottom: 8px;
      color: var(--amber);
      font-family: "Press Start 2P", monospace;
      font-size: 10px;
      line-height: 1.45;
      text-shadow: 0 0 10px rgba(255, 209, 102, 0.72);
    }}

    .lyric-text {{
      min-height: 52px;
      color: #ffffff;
      font-size: clamp(24px, 5vw, 34px);
      line-height: 1.1;
      overflow-wrap: anywhere;
      text-shadow: 0 0 12px rgba(255, 0, 127, 0.78);
    }}

    .status-line {{
      color: var(--soft-pink);
      font-size: 22px;
      line-height: 1.1;
      text-align: center;
      text-shadow: 0 0 10px rgba(255, 0, 127, 0.58);
    }}

    audio {{
      display: none;
    }}

    @keyframes capsule-boot {{
      from {{
        opacity: 0;
        transform: translateY(10px);
      }}
      to {{
        opacity: 1;
        transform: translateY(0);
      }}
    }}

    @keyframes pixel-wave {{
      0%, 100% {{
        transform: scaleY(0.72);
      }}
      50% {{
        transform: scaleY(1.22);
      }}
    }}

    @media (max-width: 640px) {{
      .spotify-capsule-shell {{
        padding-left: 4px;
        padding-right: 4px;
      }}

      .capsule-player {{
        min-height: 700px;
      }}

      .capsule-top,
      .control-row {{
        grid-template-columns: 1fr;
      }}

      .cover-frame {{
        width: min(100%, 230px);
        margin: 0 auto;
      }}

      .song-meta {{
        text-align: center;
      }}

      .badge {{
        justify-content: center;
      }}
    }}
  </style>
</head>
<body>
  <script id="spotify-capsule-config" type="application/json">{json_config}</script>
  <section class="spotify-capsule-shell" data-capsule-shell>
    <button class="capsule-trigger" type="button" data-trigger>Presiona aqui hermosa</button>
    <article class="capsule-player" data-player>
      <div class="capsule-content">
        <div class="capsule-top">
          <div class="cover-frame" data-cover-frame></div>
          <div class="song-meta">
            <div class="badge" data-badge></div>
            <h1 class="song-title" data-title></h1>
            <div class="song-artist" data-artist></div>
          </div>
        </div>
        <div class="waveform" aria-hidden="true" data-waveform></div>
        <div class="progress-panel">
          <div class="progress-track">
            <div class="progress-fill" data-progress></div>
          </div>
          <div class="time-row">
            <span data-current-time>00:00</span>
            <span data-total-time>00:00</span>
          </div>
        </div>
        <div class="control-row">
          <button class="arcade-button" type="button" data-back>-5s</button>
          <button class="arcade-button" type="button" data-play>Play</button>
          <button class="arcade-button" type="button" data-forward>+5s</button>
        </div>
        <div class="lyric-box">
          <div class="dialog-label">RPG DIALOG</div>
          <div class="lyric-text" data-lyric></div>
        </div>
        <div class="status-line" data-status></div>
      </div>
      <audio preload="metadata" data-audio></audio>
    </article>
  </section>
  <script>
    (() => {{
      const configElement = document.getElementById("spotify-capsule-config");
      const config = JSON.parse(configElement.textContent);
      const shell = document.querySelector("[data-capsule-shell]");
      const trigger = document.querySelector("[data-trigger]");
      const player = document.querySelector("[data-player]");
      const coverFrame = document.querySelector("[data-cover-frame]");
      const badge = document.querySelector("[data-badge]");
      const title = document.querySelector("[data-title]");
      const artist = document.querySelector("[data-artist]");
      const waveform = document.querySelector("[data-waveform]");
      const progress = document.querySelector("[data-progress]");
      const currentTime = document.querySelector("[data-current-time]");
      const totalTime = document.querySelector("[data-total-time]");
      const backButton = document.querySelector("[data-back]");
      const playButton = document.querySelector("[data-play]");
      const forwardButton = document.querySelector("[data-forward]");
      const lyric = document.querySelector("[data-lyric]");
      const status = document.querySelector("[data-status]");
      const audio = document.querySelector("[data-audio]");

      const startTime = Number(config.startTimeSeconds || 0);
      const duration = Math.max(Number(config.durationSeconds || 45), 1);
      const endTime = startTime + duration;
      const lyrics = Array.isArray(config.lyricsData) ? config.lyricsData : [];
      const hasAudio = Boolean(config.audioDataUri);
      const coverImages = Array.isArray(config.coverImageDataUris)
        ? config.coverImageDataUris.filter(Boolean)
        : [];
      const coverRotationSeconds = Number(config.coverRotationSeconds);
      const coverRotationMs = Math.max(
        Number.isFinite(coverRotationSeconds) ? coverRotationSeconds : 15,
        1
      ) * 1000;
      let firstPlay = true;
      let currentLyricIndex = -1;
      let currentCoverIndex = 0;
      let typingTimer = null;
      let coverTimer = null;

      function setText(element, value) {{
        element.textContent = value || "";
      }}

      function formatTime(seconds) {{
        const safeSeconds = Math.max(0, Math.floor(seconds));
        const minutes = String(Math.floor(safeSeconds / 60)).padStart(2, "0");
        const remainingSeconds = String(safeSeconds % 60).padStart(2, "0");
        return `${{minutes}}:${{remainingSeconds}}`;
      }}

      function clampToFragment(seconds) {{
        return Math.min(Math.max(seconds, startTime), endTime);
      }}

      function updateProgress() {{
        const elapsed = clampToFragment(audio.currentTime || startTime) - startTime;
        const percent = Math.min(Math.max((elapsed / duration) * 100, 0), 100);
        progress.style.width = `${{percent}}%`;
        currentTime.textContent = formatTime(elapsed);
        totalTime.textContent = formatTime(duration);
      }}

      function typeText(text) {{
        window.clearInterval(typingTimer);
        lyric.textContent = "";

        const characters = Array.from(text || "");
        if (characters.length === 0) {{
          return;
        }}

        let index = 0;
        typingTimer = window.setInterval(() => {{
          lyric.textContent += characters[index];
          index += 1;
          if (index >= characters.length) {{
            window.clearInterval(typingTimer);
          }}
        }}, 24);
      }}

      function updateLyric() {{
        const now = audio.currentTime || startTime;
        let nextIndex = -1;

        lyrics.forEach((entry, index) => {{
          if (Number(entry.time) <= now) {{
            nextIndex = index;
          }}
        }});

        if (nextIndex === -1 && lyrics.length > 0) {{
          nextIndex = 0;
        }}

        if (nextIndex !== currentLyricIndex) {{
          currentLyricIndex = nextIndex;
          const text = nextIndex >= 0 ? lyrics[nextIndex].text : config.badgeText;
          typeText(text || config.badgeText || "Nuestra cancion");
        }}
      }}

      function stopAtEnd() {{
        audio.pause();
        audio.currentTime = startTime;
        firstPlay = true;
        shell.classList.remove("is-playing");
        playButton.textContent = "Play";
        status.textContent = "Fragmento finalizado";
        updateProgress();
      }}

      function seekBy(deltaSeconds) {{
        if (!hasAudio) {{
          return;
        }}
        audio.currentTime = clampToFragment((audio.currentTime || startTime) + deltaSeconds);
        updateProgress();
        updateLyric();
      }}

      function renderCover() {{
        if (coverImages.length > 0) {{
          const image = document.createElement("img");
          image.className = "spotify-cover-img";
          image.src = coverImages[0];
          image.alt = "";
          coverFrame.appendChild(image);

          if (coverImages.length > 1) {{
            window.clearInterval(coverTimer);
            coverTimer = window.setInterval(() => {{
              rotateCover(image);
            }}, coverRotationMs);
          }}

          return;
        }}

        const placeholder = document.createElement("div");
        placeholder.className = "cover-placeholder";
        placeholder.textContent = "8-BIT LOVE TRACK";
        coverFrame.appendChild(placeholder);
      }}

      function rotateCover(image) {{
        currentCoverIndex = (currentCoverIndex + 1) % coverImages.length;
        image.classList.add("is-changing");
        coverFrame.classList.add("is-glowing");

        window.setTimeout(() => {{
          image.src = coverImages[currentCoverIndex];
          image.classList.remove("is-changing");
        }}, 240);

        window.setTimeout(() => {{
          coverFrame.classList.remove("is-glowing");
        }}, 520);
      }}

      function renderWaveform() {{
        const heights = [28, 48, 72, 38, 64, 88, 46, 30, 68, 92, 52, 36, 78, 58, 42, 84, 62, 34, 74, 96, 50, 40, 70, 86, 44, 60, 32, 76];
        heights.forEach((height, index) => {{
          const bar = document.createElement("span");
          bar.style.setProperty("--bar-height", String(height));
          bar.style.setProperty("--bar-index", String(index));
          waveform.appendChild(bar);
        }});
      }}

      async function togglePlayback() {{
        if (!hasAudio) {{
          status.textContent = "Agrega el audio local para activar el player";
          return;
        }}

        try {{
          if (audio.paused) {{
            if (firstPlay || audio.currentTime < startTime || audio.currentTime >= endTime) {{
              audio.currentTime = startTime;
              firstPlay = false;
            }}
            await audio.play();
            shell.classList.add("is-playing");
            playButton.textContent = "Pause";
            status.textContent = "";
            updateLyric();
          }} else {{
            audio.pause();
            shell.classList.remove("is-playing");
            playButton.textContent = "Play";
            status.textContent = "Pausado";
          }}
        }} catch (error) {{
          status.textContent = "El navegador bloqueo o no pudo cargar el audio";
        }}
      }}

      setText(badge, config.badgeText);
      setText(title, config.title);
      setText(artist, config.artist);
      renderCover();
      renderWaveform();
      typeText(config.badgeText || "Presiona aquí hermosa");
      updateProgress();

      if (hasAudio) {{
        audio.src = config.audioDataUri;
      }} else {{
        playButton.disabled = true;
        backButton.disabled = true;
        forwardButton.disabled = true;
        status.textContent = "Audio pendiente: coloca el fragmento local configurado";
      }}

      trigger.addEventListener("click", () => {{
        shell.classList.toggle("is-open");
      }});
      playButton.addEventListener("click", togglePlayback);
      backButton.addEventListener("click", () => seekBy(-5));
      forwardButton.addEventListener("click", () => seekBy(5));

      audio.addEventListener("loadedmetadata", () => {{
        audio.currentTime = startTime;
        updateProgress();
      }});
      audio.addEventListener("timeupdate", () => {{
        if (audio.currentTime >= endTime) {{
          stopAtEnd();
          return;
        }}
        updateProgress();
        updateLyric();
      }});
      audio.addEventListener("ended", stopAtEnd);
      audio.addEventListener("error", () => {{
        status.textContent = "No se pudo cargar el audio configurado";
      }});
    }})();
  </script>
</body>
</html>
"""


def _build_component_config(config: dict[str, Any]) -> dict[str, Any]:
    lyrics_data = config.get("lyrics_data", [])
    if not isinstance(lyrics_data, list):
        lyrics_data = []

    return {
        "title": _safe_text(config.get("title"), "Mujer Amante"),
        "artist": _safe_text(config.get("artist"), "Rata Blanca"),
        "badgeText": _safe_text(config.get("badge_text"), "Nuestra primera cancion"),
        "startTimeSeconds": _safe_number(config.get("start_time_seconds"), 0.0),
        "durationSeconds": _safe_number(config.get("duration_seconds"), 45.0),
        "lyricsData": _normalize_lyrics_data(lyrics_data),
        "audioDataUri": _audio_to_data_uri(_safe_text(config.get("song_path"), "")),
        "coverImageDataUris": _image_paths_to_data_uris(config),
        "coverRotationSeconds": _safe_number(
            config.get("cover_rotation_seconds"),
            15.0,
        ),
    }


def _normalize_lyrics_data(lyrics_data: list[Any]) -> list[dict[str, Any]]:
    normalized_lyrics = []
    for item in lyrics_data:
        if not isinstance(item, dict):
            continue

        normalized_lyrics.append(
            {
                "time": _safe_number(item.get("time"), 0.0),
                "text": _safe_text(item.get("text"), ""),
            }
        )

    return sorted(normalized_lyrics, key=lambda item: item["time"])


def _json_for_script(value: dict[str, Any]) -> str:
    json_text = json.dumps(value, ensure_ascii=False)
    return (
        json_text.replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
    )


def _asset_to_base64(path: str) -> str | None:
    asset_path = _resolve_repo_path(path)
    if asset_path is None or not asset_path.is_file():
        return None

    try:
        return b64encode(asset_path.read_bytes()).decode("ascii")
    except OSError as error:
        log_critical_error(
            error_type=type(error).__name__,
            error_message=str(error),
            module_name=__name__,
            function_name="_asset_to_base64",
        )
        return None


def _audio_to_data_uri(path: str) -> str | None:
    return _file_to_data_uri(path, fallback_mime_type="audio/mpeg")


def _image_to_data_uri(path: str) -> str | None:
    return _file_to_data_uri(path, fallback_mime_type="image/png")


def _image_paths_to_data_uris(config: dict[str, Any]) -> list[str]:
    return [
        data_uri
        for data_uri in (
            _image_to_data_uri(path)
            for path in _normalize_cover_image_paths(config)
        )
        if data_uri is not None
    ]


def _normalize_cover_image_paths(config: dict[str, Any]) -> list[str]:
    configured_paths = config.get("cover_image_paths")
    if isinstance(configured_paths, list):
        return [
            _safe_text(path, "")
            for path in configured_paths
            if _safe_text(path, "")
        ]

    legacy_path = _safe_text(config.get("cover_image_path"), "")
    if legacy_path:
        return [legacy_path]

    return []


def _file_to_data_uri(path: str, fallback_mime_type: str) -> str | None:
    encoded_asset = _asset_to_base64(path)
    if encoded_asset is None:
        return None

    mime_type = mimetypes.guess_type(path)[0] or fallback_mime_type
    return f"data:{mime_type};base64,{encoded_asset}"


def _resolve_repo_path(path: str) -> Path | None:
    if not path.strip():
        return None

    candidate_path = Path(path)
    if candidate_path.is_absolute():
        return None

    resolved_path = (PROJECT_ROOT / candidate_path).resolve()
    try:
        resolved_path.relative_to(PROJECT_ROOT)
    except ValueError:
        return None

    return resolved_path


def _safe_text(value: Any, fallback: str) -> str:
    if value is None:
        return fallback

    text = str(value).strip()
    return text or fallback


def _safe_number(value: Any, fallback: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback
