"""HTML component helpers for the romantic Streamlit landing."""

from __future__ import annotations

from base64 import b64encode
from datetime import date, datetime
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

import streamlit as st
import streamlit.components.v1 as streamlit_components

from logger.logger import log_critical_error


ASSETS_DIR = Path(__file__).parent / "assets"
STRAWBERRY_IMAGE = ASSETS_DIR / "strawberry_8bit.png"
PARCHMENT_IMAGE = ASSETS_DIR / "perrgamino.png"
HEART_IMAGE = ASSETS_DIR / "corazon.png"
STRAWBERRY_IMAGE_MIME_TYPE = "image/png"

REVEAL_OBSERVER_HTML = """
<script>
(function () {
    const rootWindow = window.parent || window;
    let rootDocument = document;

    try {
        rootDocument = rootWindow.document || document;
    } catch (_error) {
        rootDocument = document;
    }

    const stateKey = "__romanticRevealOnScroll";

    function revealElementsImmediately(elements) {
        elements.forEach((element) => {
            element.classList.add("is-visible");
            element.dataset.revealObserved = "true";
        });
    }

    function getPendingElements() {
        return Array.from(
            rootDocument.querySelectorAll(
                ".reveal-on-scroll:not([data-reveal-observed='true'])"
            )
        );
    }

    if (!("IntersectionObserver" in rootWindow)) {
        revealElementsImmediately(
            Array.from(rootDocument.querySelectorAll(".reveal-on-scroll"))
        );
        return;
    }

    if (rootWindow[stateKey]) {
        rootWindow[stateKey].refresh();
        return;
    }

    const observer = new rootWindow.IntersectionObserver(
        (entries, observerInstance) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-visible");
                    observerInstance.unobserve(entry.target);
                }
            });
        },
        {
            threshold: 0.14,
            rootMargin: "0px 0px -40px 0px",
        }
    );

    function refresh() {
        getPendingElements().forEach((element) => {
            element.dataset.revealObserved = "true";
            observer.observe(element);
        });
    }

    const mutationObserver = new rootWindow.MutationObserver(() => {
        rootWindow.requestAnimationFrame(refresh);
    });

    mutationObserver.observe(rootDocument.body, {
        childList: true,
        subtree: true,
    });

    rootWindow[stateKey] = {
        refresh,
        observer,
        mutationObserver,
    };

    rootWindow.requestAnimationFrame(refresh);
    rootWindow.setTimeout(refresh, 250);
})();
</script>
"""


def render_hero(hero: dict[str, str]) -> None:
    """Render the romantic hero."""
    _render_html(build_hero_html(hero))


def build_hero_html(hero: dict[str, str]) -> str:
    """Build the romantic hero HTML."""
    strawberry_html = _build_hero_strawberry_html()

    return f"""
        <section class="romantic-hero reveal-on-scroll">
          <div class="hero-kicker">{_escape_value(hero.get("date_range", ""))}</div>
          <h1 class="glossy-fuchsia-text">{_escape_value(hero.get("title", "Nuestra historia"))}</h1>
          <p class="hero-subtitle">{_escape_value(hero.get("subtitle", ""))}</p>
          <div class="hero-date">{_escape_value(hero.get("welcome", ""))}</div>
          {strawberry_html}
        </section>
        """


def render_section_header(kicker: str, title: str, copy: str) -> None:
    """Render a consistent section heading."""
    _render_html(build_section_header_html(kicker, title, copy))


def build_section_header_html(kicker: str, title: str, copy: str) -> str:
    """Build a consistent section heading HTML."""
    return f"""
        <section class="section-block reveal-on-scroll">
          <div class="section-kicker">{_escape_value(kicker)}</div>
          <h2 class="section-title">{_escape_value(title)}</h2>
          <p class="section-copy">{_escape_value(copy)}</p>
        </section>
        """


def render_metric_cards(cards: list[dict[str, str]]) -> None:
    """Render summary metrics as a bento grid."""
    _render_html(build_metric_cards_html(cards))


def build_metric_cards_html(cards: list[dict[str, str]]) -> str:
    """Build summary metric card HTML."""
    html_cards = []
    heart_data_uri = _build_optional_image_data_uri(HEART_IMAGE)
    for index, card in enumerate(cards):
        size_class = _card_size_class(card.get("size", "small"))
        raw_label = card.get("label", "")
        label = _escape_value(raw_label)
        value = _escape_value(card.get("value", "0"))
        description = _escape_value(card.get("description", ""))
        first_te_amo_class = _first_te_amo_card_class(raw_label)
        heart_html = _build_first_te_amo_heart_html(
            heart_data_uri,
            raw_label,
        )
        html_cards.append(
            f"""
            <article class="bento-card {size_class}{first_te_amo_class} reveal-on-scroll" {_reveal_style(index)}>
              {heart_html}
              <div class="metric-label">{label}</div>
              <div class="metric-number">{value}</div>
              <p class="metric-description">{description}</p>
            </article>
            """
        )

    return f"""<section class="bento-grid">{''.join(html_cards)}</section>"""


def render_timeline(events: list[dict[str, str]]) -> None:
    """Render romantic timeline events."""
    _render_html(build_timeline_html(events))


def build_timeline_html(events: list[dict[str, str]]) -> str:
    """Build romantic timeline event card HTML."""
    event_cards = []
    heart_data_uri = _build_optional_image_data_uri(HEART_IMAGE)
    for index, event in enumerate(events):
        raw_title = event.get("title", "")
        first_te_amo_class = _first_te_amo_card_class(raw_title)
        heart_html = _build_first_te_amo_heart_html(
            heart_data_uri,
            raw_title,
        )
        event_cards.append(
            f"""
            <article class="timeline-card{first_te_amo_class} reveal-on-scroll" {_reveal_style(index)}>
              {heart_html}
              <div class="date-pill">{_escape_value(event.get("date", ""))}</div>
              <div class="timeline-title">{_escape_value(raw_title)}</div>
              <p class="timeline-detail">{_escape_value(event.get("detail", ""))}</p>
            </article>
            """
        )

    return f"""<section class="timeline-list">{''.join(event_cards)}</section>"""


def render_words(words: list[dict[str, str]]) -> None:
    """Render romantic words."""
    if not words:
        st.info(
            "Las palabras que nos representan apareceran cuando haya "
            "mensajes cargados."
        )
        return

    chips = []
    for index, word in enumerate(words):
        chips.append(
            f"""
            <article class="word-chip reveal-on-scroll" {_reveal_style(index)}>
              <strong>{_escape_value(word.get("word", ""))}</strong>
              <span>{_escape_value(word.get("count", "0"))} veces</span>
            </article>
            """
        )

    _render_html(f"""<section class="word-cloud">{''.join(chips)}</section>""")


def render_quotes(messages: list[dict[str, str]]) -> None:
    """Render featured romantic messages."""
    if not messages:
        st.info("Las frases bonitas apareceran cuando los mensajes esten cargados.")
        return

    _render_html(build_quote_cards_html(messages))


def build_quote_cards_html(messages: list[dict[str, str]]) -> str:
    """Build featured romantic message card HTML."""
    quote_cards = []
    parchment_data_uri = _build_optional_image_data_uri(PARCHMENT_IMAGE)
    for index, message in enumerate(messages):
        quote_cards.append(
            f"""
            <article class="quote-card scroll-quote-card reveal-on-scroll" {_quote_card_style(index, parchment_data_uri)}>
              <p class="quote-text">"{_escape_value(message.get("message", ""))}"</p>
              <div class="quote-sender">{_escape_value(message.get("sender", ""))}</div>
              <div class="quote-date">{_escape_value(message.get("date", ""))}</div>
            </article>
            """
        )

    return f"""<section class="quote-grid">{''.join(quote_cards)}</section>"""


def render_special_message(
    message: dict[str, Any] | None,
    title: str = "Un mensaje que quiero guardar",
    subtitle: str = "Hay palabras que merecen quedarse aqui.",
) -> None:
    """Render the manually selected special message."""
    _render_html(build_special_message_html(message, title, subtitle))


def build_special_message_html(
    message: dict[str, Any] | None,
    title: str = "Un mensaje que quiero guardar",
    subtitle: str = "Hay palabras que merecen quedarse aqui.",
) -> str:
    """Build the manually selected special message HTML."""
    selected_message = message or {}
    title_text = _safe_component_text(selected_message.get("title"), title)
    subtitle_text = _safe_component_text(selected_message.get("subtitle"), subtitle)
    class_name = (
        "special-message-card ig-chat-card quote-card-featured glitter-accent "
        "glossy-card-highlight reveal-on-scroll"
    )
    message_blocks = _build_special_message_blocks_html(selected_message)

    return f"""
        <article class="{class_name}">
          <div class="ig-chat-header">
            <div class="special-message-kicker ig-chat-title">{_escape_value(title_text)}</div>
            <p class="special-message-subtitle manual-subtitle">{_manual_html(subtitle_text)}</p>
          </div>
          {message_blocks}
        </article>
        """

    return f"""
        <article class="{class_name}">
          <div class="ig-chat-header">
            <div class="special-message-kicker ig-chat-title">{_escape_value(title_text)}</div>
            <p class="special-message-subtitle manual-subtitle">{_manual_html(subtitle_text)}</p>
          </div>
          <div class="ig-message-list">
            <div class="ig-bubble {bubble_class}">
              <p>"{_escape_value(message_text)}"</p>
              {_build_message_meta_html(sender_text, date_text)}
            </div>
          </div>
        </article>
        """


def render_conversation_starter(starter: dict[str, str]) -> None:
    """Render the conversation starter note."""
    sender = _escape_value(starter.get("sender", "Pendiente"))
    detail = _escape_value(starter.get("detail", ""))
    _render_html(
        f"""
        <article class="bento-card full reveal-on-scroll">
          <div class="metric-label">Quien prendio mas veces la conversacion</div>
          <div class="metric-number">{sender}</div>
          <p class="metric-description">{detail}</p>
        </article>
        """
    )


def render_closing() -> None:
    """Render the closing emotional section."""
    _render_html(
        """
        <section class="closing-card reveal-on-scroll">
          <h2>Estos datos no son solo numeros.</h2>
          <p>
            Son pedacitos de nosotros: dias, palabras y recuerdos que se
            quedaron guardados.
          </p>
        </section>
        """
    )


def _render_html(html: str) -> None:
    st.markdown(_normalize_html(html), unsafe_allow_html=True)


def _build_hero_strawberry_html(
    image_path: Path | None = None,
) -> str:
    resolved_image_path = image_path or STRAWBERRY_IMAGE
    if not resolved_image_path.exists():
        return ""

    image_data_uri = _build_image_data_uri(
        image_path=resolved_image_path,
        mime_type=STRAWBERRY_IMAGE_MIME_TYPE,
    )
    if not image_data_uri:
        return ""

    return (
        '<div class="hero-orb" aria-hidden="true">'
        f'<img class="hero-strawberry" src="{image_data_uri}" alt="" />'
        "</div>"
    )


def _build_image_data_uri(image_path: Path, mime_type: str) -> str:
    try:
        encoded_image = b64encode(image_path.read_bytes()).decode("ascii")
    except OSError as error:
        log_critical_error(
            error_type=type(error).__name__,
            error_message=str(error),
            module_name=__name__,
            function_name="_build_image_data_uri",
        )
        return ""

    return f"data:{mime_type};base64,{encoded_image}"


def _build_optional_image_data_uri(image_path: Path) -> str:
    if not image_path.exists():
        return ""

    return _build_image_data_uri(
        image_path=image_path,
        mime_type=STRAWBERRY_IMAGE_MIME_TYPE,
    )


def render_reveal_observer() -> None:
    """Inject the reveal-on-scroll observer after the landing HTML exists."""
    streamlit_components.html(REVEAL_OBSERVER_HTML, height=0)


def _escape_value(value: Any) -> str:
    return escape(str(value))


def _manual_html(value: Any) -> str:
    parser = _ManualStrongHTMLParser()
    parser.feed(str(value))
    parser.close()
    return parser.html


def _normalize_html(html: str) -> str:
    lines = [line.strip() for line in html.splitlines()]
    return "\n".join(line for line in lines if line)


def _card_size_class(size: Any) -> str:
    if size == "large":
        return "large"
    if size == "full":
        return "full"

    return ""


def _reveal_style(index: int) -> str:
    return f'style="--reveal-delay: {min(index * 90, 360)}ms;"'


def _quote_card_style(index: int, parchment_data_uri: str) -> str:
    reveal_delay = min(index * 90, 360)
    if not parchment_data_uri:
        return f'style="--reveal-delay: {reveal_delay}ms;"'

    return (
        f'style="--reveal-delay: {reveal_delay}ms; '
        f"--scroll-bg-image: url('{parchment_data_uri}');\""
    )


def _first_te_amo_card_class(value: Any) -> str:
    if _is_first_te_amo(value):
        return " first-te-amo-card"

    return ""


def _build_first_te_amo_heart_html(heart_data_uri: str, value: Any) -> str:
    if not heart_data_uri or not _is_first_te_amo(value):
        return ""

    return f'<img class="first-te-amo-heart" src="{heart_data_uri}" alt="" />'


def _is_first_te_amo(value: Any) -> bool:
    return "primer te amo" in str(value).casefold()


def _message_bubble_class(sender: str) -> str:
    normalized_sender = sender.casefold()
    if "mar" in normalized_sender or "fresita" in normalized_sender:
        return "ig-bubble-her"

    return "ig-bubble-me"


def _build_special_message_blocks_html(selected_message: dict[str, Any]) -> str:
    blocks = selected_message.get("blocks", [])
    if isinstance(blocks, list) and blocks:
        block_html = [
            _build_special_message_block_html(block)
            for block in blocks
            if isinstance(block, dict)
        ]
        rendered_blocks = "".join(block for block in block_html if block)
        if rendered_blocks:
            return rendered_blocks

    return _build_legacy_special_message_html(selected_message)


def _build_special_message_block_html(block: dict[str, Any]) -> str:
    messages = block.get("messages", [])
    if not isinstance(messages, list) or not messages:
        return ""

    bubbles = [
        _build_special_message_bubble_html(message)
        for message in messages
        if isinstance(message, dict)
    ]
    rendered_bubbles = "".join(bubble for bubble in bubbles if bubble)
    if not rendered_bubbles:
        return ""

    block_type = _safe_component_text(block.get("type"), "message_block")
    block_title = _optional_component_text(block.get("title"))
    block_header = _build_special_message_block_header_html(block_title)
    return f"""
          <section class="special-message-block special-message-block-{_component_class_token(block_type)}">
            {block_header}
            <div class="ig-message-list">
              {rendered_bubbles}
            </div>
          </section>
        """


def _build_special_message_bubble_html(message: dict[str, Any]) -> str:
    message_text = _safe_component_text(message.get("message"), "")
    if not message_text:
        return ""

    role = message.get("role")
    bubble_class = "ig-bubble-me" if role == "me" else "ig-bubble-her"
    sender_text = _safe_component_text(message.get("sender"), "Pendiente")
    date_text = _format_component_date(message.get("timestamp", message.get("date")))

    return f"""
            <div class="ig-bubble {bubble_class}">
              <p>"{_escape_value(message_text)}"</p>
              {_build_message_meta_html(sender_text, date_text)}
            </div>
        """


def _build_legacy_special_message_html(selected_message: dict[str, Any]) -> str:
    message_text = _safe_component_text(
        selected_message.get("message"),
        "Aun no hay un mensaje especial seleccionado.",
    )
    sender_text = _safe_component_text(selected_message.get("sender"), "Pendiente")
    date_text = _format_component_date(
        selected_message.get("timestamp", selected_message.get("date"))
    )
    bubble_class = _message_bubble_class(sender_text)

    return f"""
          <div class="ig-message-list">
            <div class="ig-bubble {bubble_class}">
              <p>"{_escape_value(message_text)}"</p>
              {_build_message_meta_html(sender_text, date_text)}
            </div>
          </div>
        """


def _build_message_meta_html(sender_text: str, date_text: str) -> str:
    return (
        '<span class="ig-bubble-meta">'
        f"{_escape_value(sender_text)} "
        '<span class="message-meta-separator">-</span> '
        f"{_escape_value(date_text)}"
        "</span>"
    )


def _component_class_token(value: Any) -> str:
    text = _safe_component_text(value, "message_block").casefold()
    return "".join(character if character.isalnum() else "-" for character in text)


def _safe_component_text(value: Any, fallback: str) -> str:
    if value is None:
        return fallback

    text = str(value).strip()
    return text or fallback


def _optional_component_text(value: Any) -> str:
    if value is None:
        return ""

    return str(value).strip()


def _build_special_message_block_header_html(title: str) -> str:
    if not title:
        return ""

    return f"""
            <div class="ig-chat-header">
              <div class="special-message-block-title">{_escape_value(title)}</div>
            </div>
        """


def _format_component_date(value: Any) -> str:
    if isinstance(value, datetime):
        return value.strftime("%d/%m/%Y")
    if isinstance(value, date):
        return value.strftime("%d/%m/%Y")

    return _safe_component_text(value, "Fecha pendiente")


class _ManualStrongHTMLParser(HTMLParser):
    """Allow only manual <strong> tags and escape all other text/tags."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self._parts: list[str] = []
        self._allowed_strong_depth = 0

    @property
    def html(self) -> str:
        return "".join(self._parts)

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        if tag == "strong" and not attrs:
            self._parts.append("<strong>")
            self._allowed_strong_depth += 1
            return

        self._parts.append(escape(self.get_starttag_text() or ""))

    def handle_endtag(self, tag: str) -> None:
        if tag == "strong" and self._allowed_strong_depth > 0:
            self._parts.append("</strong>")
            self._allowed_strong_depth -= 1
            return

        self._parts.append(escape(f"</{tag}>"))

    def handle_data(self, data: str) -> None:
        self._parts.append(escape(data))

    def handle_entityref(self, name: str) -> None:
        self._parts.append(escape(f"&{name};"))

    def handle_charref(self, name: str) -> None:
        self._parts.append(escape(f"&#{name};"))
