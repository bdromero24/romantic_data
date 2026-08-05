"""Interactive birthday invitation letter component for Streamlit."""

from __future__ import annotations

import html
import json
from typing import Any

import streamlit.components.v1 as components


DEFAULT_COMPONENT_HEIGHT = 1040
FALLBACK_LETTER_BODY = [
    "Tengo una invitacion especial para ti.",
]


def render_birthday_invitation(config: dict[str, Any]) -> None:
    """Render the optional birthday invitation as an isolated HTML component."""
    if not config.get("enabled", False):
        return

    components.html(
        build_birthday_invitation_html(config),
        height=DEFAULT_COMPONENT_HEIGHT,
        scrolling=False,
    )


def build_birthday_invitation_html(config: dict[str, Any]) -> str:
    """Build the isolated HTML/CSS/JS for the birthday invitation."""
    component_config = _build_component_config(config)
    json_config = _json_for_script(component_config)
    body_paragraphs = "\n".join(
        f"          <p>{html.escape(paragraph)}</p>"
        for paragraph in component_config["letterBody"]
    )
    link_buttons = "\n".join(
        _build_link_button(link)
        for link in component_config["links"]
        if link["url"] and link["text"]
    )

    return f"""
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600;700&family=Nunito:wght@500;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --birthday-pink: #ffd1ea;
      --birthday-fuchsia: #ff007f;
      --birthday-deep: #9d004f;
      --birthday-paper: #f4e4c8;
      --birthday-paper-dark: #d6b98e;
      --birthday-ink: #3f2435;
      --birthday-soft-shadow: rgba(157, 0, 79, 0.28);
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      background: transparent;
      color: var(--birthday-ink);
      font-family: "Nunito", "Quicksand", system-ui, sans-serif;
      letter-spacing: 0;
    }}

    .birthday-invitation-root {{
      width: min(100%, 820px);
      margin: 0 auto;
      min-height: 100%;
      padding: 12px 12px 28px;
      overflow: visible;
    }}

    .birthday-envelope-stage {{
      position: relative;
      min-height: 430px;
      display: grid;
      place-items: center;
      overflow: hidden;
      border: 1px solid rgba(255, 255, 255, 0.58);
      border-radius: 8px;
      background:
        radial-gradient(circle at 18% 16%, rgba(255, 255, 255, 0.92) 0 10%, transparent 11%),
        radial-gradient(circle at 72% 20%, rgba(255, 255, 255, 0.72) 0 9%, transparent 10%),
        linear-gradient(180deg, #ffe7f4 0%, #ffd1ea 52%, #ffc3e3 100%);
      box-shadow:
        0 0 0 1px rgba(255, 255, 255, 0.32) inset,
        0 22px 56px rgba(157, 0, 79, 0.22),
        0 0 32px rgba(255, 0, 127, 0.18);
      cursor: pointer;
    }}

    .birthday-envelope-stage::before,
    .birthday-envelope-stage::after {{
      content: "";
      position: absolute;
      width: 148px;
      height: 44px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.70);
      box-shadow:
        38px 2px 0 rgba(255, 255, 255, 0.62),
        76px 10px 0 rgba(255, 255, 255, 0.50);
      opacity: 0.82;
    }}

    .birthday-envelope-stage::before {{
      top: 34px;
      left: 26px;
      animation: birthday-cloud-drift 8s ease-in-out infinite;
    }}

    .birthday-envelope-stage::after {{
      right: 28px;
      bottom: 62px;
      transform: scale(0.78);
      animation: birthday-cloud-drift 9s ease-in-out infinite reverse;
    }}

    .birthday-closed-card {{
      position: relative;
      z-index: 2;
      display: grid;
      justify-items: center;
      gap: 18px;
      width: min(100%, 460px);
      padding: 28px 20px;
      text-align: center;
      transition: opacity 320ms ease, transform 320ms ease;
    }}

    .birthday-envelope {{
      position: relative;
      width: min(82vw, 300px);
      aspect-ratio: 1.45;
      border: 3px solid rgba(157, 0, 79, 0.34);
      border-radius: 8px;
      background:
        linear-gradient(145deg, transparent 49%, rgba(255, 0, 127, 0.20) 50%),
        linear-gradient(215deg, transparent 49%, rgba(255, 0, 127, 0.18) 50%),
        linear-gradient(180deg, #fffaff, #fff1f8);
      box-shadow:
        0 14px 26px rgba(157, 0, 79, 0.24),
        0 0 32px rgba(255, 0, 127, 0.35);
      animation: birthday-envelope-float 3.8s ease-in-out infinite;
    }}

    .birthday-envelope::before {{
      content: "";
      position: absolute;
      inset: 0;
      clip-path: polygon(0 0, 50% 56%, 100% 0);
      background: linear-gradient(180deg, #ffffff, #ffe3f1);
      border-radius: 5px 5px 0 0;
    }}

    .birthday-envelope-wing {{
      position: absolute;
      top: 35%;
      width: 82px;
      height: 54px;
      background: rgba(255, 255, 255, 0.92);
      border: 2px solid rgba(157, 0, 79, 0.16);
      box-shadow: 0 8px 22px rgba(157, 0, 79, 0.16);
    }}

    .birthday-envelope-wing-left {{
      left: -70px;
      border-radius: 80% 18% 72% 28%;
      transform: rotate(-10deg);
    }}

    .birthday-envelope-wing-right {{
      right: -70px;
      border-radius: 18% 80% 28% 72%;
      transform: rotate(10deg);
    }}

    .birthday-envelope-wing::after {{
      content: "";
      position: absolute;
      inset: 10px 12px;
      border-top: 2px solid rgba(255, 0, 127, 0.18);
      border-bottom: 2px solid rgba(255, 0, 127, 0.12);
      border-radius: inherit;
    }}

    .birthday-heart-sticker {{
      position: absolute;
      left: 50%;
      top: 58%;
      width: 54px;
      height: 54px;
      display: grid;
      place-items: center;
      border-radius: 50%;
      background: linear-gradient(180deg, #ff4fa3, var(--birthday-fuchsia));
      color: #ffffff;
      font-size: 28px;
      transform: translate(-50%, -50%);
      box-shadow:
        0 0 18px rgba(255, 0, 127, 0.76),
        0 0 0 7px rgba(255, 209, 234, 0.72);
    }}

    .birthday-closed-title {{
      margin: 0;
      color: var(--birthday-deep);
      font-family: "Dancing Script", "Great Vibes", cursive;
      font-size: clamp(34px, 8vw, 54px);
      line-height: 1;
      overflow-wrap: anywhere;
      text-shadow: 0 0 16px rgba(255, 0, 127, 0.20);
    }}

    .birthday-closed-subtitle {{
      margin: 0;
      color: #7b1647;
      font-size: clamp(16px, 4vw, 20px);
      font-weight: 800;
      line-height: 1.4;
      overflow-wrap: anywhere;
    }}

    .birthday-floating-heart {{
      position: absolute;
      color: rgba(157, 0, 79, 0.45);
      font-size: 22px;
      animation: birthday-heart-rise 7s ease-in-out infinite;
    }}

    .birthday-heart-one {{
      left: 16%;
      bottom: 22%;
    }}

    .birthday-heart-two {{
      right: 18%;
      top: 24%;
      animation-delay: -2.4s;
    }}

    .birthday-heart-three {{
      left: 52%;
      top: 14%;
      animation-delay: -4s;
    }}

    .birthday-letter {{
      position: relative;
      display: none;
      width: min(100%, 680px);
      margin: 0 auto;
      padding: clamp(28px, 6vw, 48px);
      border: 2px solid rgba(120, 79, 36, 0.22);
      border-radius: 8px;
      background:
        radial-gradient(circle at 18% 20%, rgba(255, 255, 255, 0.34), transparent 18%),
        radial-gradient(circle at 82% 78%, rgba(157, 0, 79, 0.08), transparent 19%),
        repeating-linear-gradient(105deg, rgba(120, 79, 36, 0.035) 0 2px, transparent 2px 8px),
        linear-gradient(180deg, #f8ecd5, var(--birthday-paper));
      box-shadow:
        0 18px 44px rgba(75, 38, 16, 0.20),
        0 0 0 8px rgba(255, 245, 226, 0.45) inset,
        0 0 32px rgba(255, 0, 127, 0.20);
      transform: translateY(22px);
      opacity: 0;
    }}

    .birthday-letter::before,
    .birthday-letter::after {{
      content: "";
      position: absolute;
      left: 18px;
      right: 18px;
      height: 10px;
      border-radius: 50%;
      background: rgba(120, 79, 36, 0.10);
      filter: blur(2px);
    }}

    .birthday-letter::before {{
      top: 10px;
    }}

    .birthday-letter::after {{
      bottom: 10px;
    }}

    .birthday-letter-open .birthday-closed-card {{
      display: none;
      opacity: 0;
      transform: translateY(-12px) scale(0.98);
      pointer-events: none;
    }}

    .birthday-letter-open .birthday-envelope-stage {{
      min-height: 920px;
      align-items: start;
      padding: 26px 14px 48px;
      cursor: default;
      overflow: visible;
    }}

    .birthday-letter-open .birthday-letter {{
      display: block;
      animation: birthday-letter-unfold 520ms ease forwards;
    }}

    .birthday-letter-title,
    .birthday-letter-signature {{
      margin: 0;
      color: var(--birthday-deep);
      font-family: "Dancing Script", "Great Vibes", cursive;
      font-size: clamp(34px, 7vw, 50px);
      line-height: 1.1;
      overflow-wrap: anywhere;
    }}

    .birthday-letter-body {{
      display: grid;
      gap: 14px;
      margin: 22px 0;
      color: var(--birthday-ink);
      font-size: clamp(16px, 3.8vw, 19px);
      font-weight: 700;
      line-height: 1.65;
    }}

    .birthday-letter-body p {{
      margin: 0;
    }}

    .birthday-letter-links {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
      margin: 26px 0 24px;
    }}

    .birthday-link-button {{
      min-height: 48px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 12px 16px;
      border: 1px solid rgba(255, 255, 255, 0.58);
      border-radius: 6px;
      background:
        linear-gradient(180deg, rgba(255, 112, 180, 0.96), var(--birthday-fuchsia));
      color: #ffffff;
      font-size: 15px;
      font-weight: 900;
      line-height: 1.25;
      text-align: center;
      text-decoration: none;
      overflow-wrap: anywhere;
      box-shadow:
        0 8px 18px rgba(157, 0, 79, 0.26),
        0 0 18px rgba(255, 0, 127, 0.34);
    }}

    .birthday-link-button:hover {{
      transform: translateY(-1px);
      box-shadow:
        0 10px 22px rgba(157, 0, 79, 0.30),
        0 0 24px rgba(255, 0, 127, 0.44);
    }}

    .birthday-paper-sticker {{
      position: absolute;
      top: 18px;
      right: 20px;
      width: 42px;
      height: 42px;
      display: grid;
      place-items: center;
      border-radius: 50%;
      background: rgba(255, 209, 234, 0.80);
      color: var(--birthday-fuchsia);
      font-size: 22px;
      box-shadow: 0 0 0 6px rgba(255, 255, 255, 0.28);
    }}

    @keyframes birthday-envelope-float {{
      0%, 100% {{
        transform: translateY(0);
      }}
      50% {{
        transform: translateY(-10px);
      }}
    }}

    @keyframes birthday-cloud-drift {{
      0%, 100% {{
        transform: translateX(0);
      }}
      50% {{
        transform: translateX(14px);
      }}
    }}

    @keyframes birthday-heart-rise {{
      0%, 100% {{
        opacity: 0.36;
        transform: translateY(0) scale(1);
      }}
      50% {{
        opacity: 0.78;
        transform: translateY(-18px) scale(1.08);
      }}
    }}

    @keyframes birthday-letter-unfold {{
      from {{
        opacity: 0;
        transform: translateY(28px) scaleY(0.94);
      }}
      to {{
        opacity: 1;
        transform: translateY(0) scaleY(1);
      }}
    }}

    @media (max-width: 640px) {{
      .birthday-invitation-root {{
        padding-left: 4px;
        padding-right: 4px;
      }}

      .birthday-envelope-stage {{
        min-height: 430px;
      }}

      .birthday-letter-open .birthday-envelope-stage {{
        min-height: 980px;
        padding: 18px 8px 38px;
      }}

      .birthday-letter {{
        width: min(96vw, 680px);
        padding: 30px 20px 34px;
      }}

      .birthday-envelope-wing {{
        width: 62px;
        height: 44px;
      }}

      .birthday-envelope-wing-left {{
        left: -48px;
      }}

      .birthday-envelope-wing-right {{
        right: -48px;
      }}

      .birthday-letter-links {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <script id="birthday-invitation-config" type="application/json">{json_config}</script>
  <section class="birthday-invitation-root" data-birthday-root>
    <div class="birthday-envelope-stage" data-birthday-open-trigger>
      <span class="birthday-floating-heart birthday-heart-one" aria-hidden="true">♥</span>
      <span class="birthday-floating-heart birthday-heart-two" aria-hidden="true">♥</span>
      <span class="birthday-floating-heart birthday-heart-three" aria-hidden="true">♥</span>
      <div class="birthday-closed-card">
        <div class="birthday-envelope" aria-hidden="true">
          <span class="birthday-envelope-wing birthday-envelope-wing-left"></span>
          <span class="birthday-envelope-wing birthday-envelope-wing-right"></span>
          <span class="birthday-heart-sticker">♥</span>
        </div>
        <h1 class="birthday-closed-title">{html.escape(component_config["closedTitle"])}</h1>
        <p class="birthday-closed-subtitle">{html.escape(component_config["closedSubtitle"])}</p>
      </div>
      <article class="birthday-letter" aria-live="polite">
        <span class="birthday-paper-sticker" aria-hidden="true">♥</span>
        <h2 class="birthday-letter-title">{html.escape(component_config["letterTitle"])}</h2>
        <div class="birthday-letter-body">
{body_paragraphs}
        </div>
        <div class="birthday-letter-links">
{link_buttons}
        </div>
        <p class="birthday-letter-signature">{html.escape(component_config["signature"])}</p>
      </article>
    </div>
  </section>
  <script>
    (() => {{
      const configElement = document.getElementById("birthday-invitation-config");
      JSON.parse(configElement.textContent);
      const root = document.querySelector("[data-birthday-root]");
      const trigger = document.querySelector("[data-birthday-open-trigger]");

      trigger.addEventListener("click", (event) => {{
        if (event.target.closest("a")) {{
          return;
        }}
        root.classList.add("birthday-letter-open");
      }});
    }})();
  </script>
</body>
</html>
"""


def _build_component_config(config: dict[str, Any]) -> dict[str, Any]:
    letter_body = config.get("letter_body", FALLBACK_LETTER_BODY)
    if not isinstance(letter_body, list):
        letter_body = FALLBACK_LETTER_BODY

    normalized_body = [
        _safe_text(paragraph, "")
        for paragraph in letter_body
        if _safe_text(paragraph, "")
    ]

    return {
        "closedTitle": _safe_text(config.get("closed_title"), "Nueva carta para ti"),
        "closedSubtitle": _safe_text(
            config.get("closed_subtitle"),
            "Toca para abrir tu invitacion",
        ),
        "letterTitle": _safe_text(config.get("letter_title"), "Querida Mar:"),
        "letterBody": normalized_body or FALLBACK_LETTER_BODY,
        "signature": _safe_text(config.get("signature"), "Con amor, David"),
        "links": [
            {
                "text": _safe_text(config.get("primary_link_text"), ""),
                "url": _safe_url(config.get("primary_link_url")),
            },
            {
                "text": _safe_text(config.get("secondary_link_text"), ""),
                "url": _safe_url(config.get("secondary_link_url")),
            },
        ],
    }


def _build_link_button(link: dict[str, str]) -> str:
    safe_url = html.escape(link["url"], quote=True)
    safe_text = html.escape(link["text"])
    return (
        f'          <a class="birthday-link-button" href="{safe_url}" '
        f'target="_blank" rel="noopener noreferrer">{safe_text}</a>'
    )


def _json_for_script(value: dict[str, Any]) -> str:
    json_text = json.dumps(value, ensure_ascii=False)
    return (
        json_text.replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
    )


def _safe_text(value: Any, fallback: str) -> str:
    if value is None:
        return fallback

    text = str(value).strip()
    return text or fallback


def _safe_url(value: Any) -> str:
    if not isinstance(value, str):
        return ""

    text = value.strip()
    if not text or text.lower().startswith(("javascript:", "data:")):
        return ""

    return text
