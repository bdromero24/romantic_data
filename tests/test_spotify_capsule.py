"""Unit tests for the Spotify-inspired neon capsule component."""

from __future__ import annotations

from ui import spotify_capsule


def test_spotify_capsule_embeds_local_assets(tmp_path, monkeypatch) -> None:
    image_path = tmp_path / "cover.png"
    audio_path = tmp_path / "song.mp3"
    image_path.write_bytes(b"fake-image")
    audio_path.write_bytes(b"fake-audio")
    monkeypatch.setattr(spotify_capsule, "PROJECT_ROOT", tmp_path)

    html = spotify_capsule.build_spotify_8bit_player_html(
        {
            "title": "Mujer Amante",
            "artist": "Rata Blanca",
            "badge_text": "Nuestra cancion",
            "cover_image_path": "cover.png",
            "song_path": "song.mp3",
            "start_time_seconds": 45,
            "duration_seconds": 45,
            "lyrics_data": [{"time": 52, "text": "Frase manual"}],
        }
    )

    assert "data:image/png;base64,ZmFrZS1pbWFnZQ==" in html
    assert "data:audio/mpeg;base64,ZmFrZS1hdWRpbw==" in html
    assert '"coverImageDataUris": ["data:image/png;base64,ZmFrZS1pbWFnZQ=="]' in html
    assert '"startTimeSeconds": 45.0' in html
    assert '"durationSeconds": 45.0' in html


def test_spotify_capsule_embeds_multiple_cover_images(
    tmp_path,
    monkeypatch,
) -> None:
    first_image_path = tmp_path / "cover-1.png"
    second_image_path = tmp_path / "cover-2.jpg"
    first_image_path.write_bytes(b"first-image")
    second_image_path.write_bytes(b"second-image")
    monkeypatch.setattr(spotify_capsule, "PROJECT_ROOT", tmp_path)

    html = spotify_capsule.build_spotify_8bit_player_html(
        {
            "cover_image_paths": ["cover-1.png", "missing.png", "cover-2.jpg"],
            "cover_rotation_seconds": 15,
        }
    )

    assert "data:image/png;base64,Zmlyc3QtaW1hZ2U=" in html
    assert "data:image/jpeg;base64,c2Vjb25kLWltYWdl" in html
    assert '"coverRotationSeconds": 15.0' in html
    assert "window.setInterval" in html


def test_spotify_capsule_falls_back_when_assets_are_missing(
    tmp_path,
    monkeypatch,
) -> None:
    monkeypatch.setattr(spotify_capsule, "PROJECT_ROOT", tmp_path)

    html = spotify_capsule.build_spotify_8bit_player_html(
        {
            "cover_image_path": "missing.png",
            "song_path": "missing.mp3",
        }
    )

    assert '"audioDataUri": null' in html
    assert '"coverImageDataUris": []' in html
    assert "Audio pendiente: coloca el fragmento local configurado" in html
    assert "8-BIT LOVE TRACK" in html


def test_spotify_capsule_falls_back_when_cover_image_paths_are_empty(
    tmp_path,
    monkeypatch,
) -> None:
    monkeypatch.setattr(spotify_capsule, "PROJECT_ROOT", tmp_path)

    html = spotify_capsule.build_spotify_8bit_player_html(
        {
            "cover_image_paths": [],
            "cover_image_path": "legacy-cover.png",
        }
    )

    assert '"coverImageDataUris": []' in html
    assert "8-BIT LOVE TRACK" in html


def test_spotify_capsule_sorts_manual_lyrics_and_serializes_safely() -> None:
    html = spotify_capsule.build_spotify_8bit_player_html(
        {
            "title": '</script><script>alert("x")</script>',
            "lyrics_data": [
                {"time": 68, "text": "Tercera"},
                {"time": 45, "text": "Primera"},
            ],
        }
    )

    assert "</script><script>" not in html
    assert "\\u003c/script\\u003e" in html
    assert html.index('"text": "Primera"') < html.index('"text": "Tercera"')


def test_render_spotify_8bit_player_uses_streamlit_html(monkeypatch) -> None:
    calls: list[tuple[str, int, bool]] = []

    monkeypatch.setattr(
        spotify_capsule.streamlit_components,
        "html",
        lambda html, height, scrolling: calls.append((html, height, scrolling)),
    )

    spotify_capsule.render_spotify_8bit_player({"title": "Mujer Amante"})

    rendered_html, height, scrolling = calls[0]
    assert "spotify-capsule-shell" in rendered_html
    assert height == spotify_capsule.DEFAULT_COMPONENT_HEIGHT
    assert scrolling is False
