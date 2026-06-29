"""Custom CSS for the romantic Streamlit landing."""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@600;700&family=JetBrains+Mono:wght@500;700&family=Nunito:wght@400;600;700;800&family=Playfair+Display:wght@700;800&display=swap');

:root {
  --bg-main: #fff0f8;
  --bg-secondary: #ffd6ec;
  --bg-deep-pink: #ffc1e3;
  --pink-soft: #ffb3d9;
  --pink-mid: #ff5fb7;
  --fuchsia: #d41472;
  --fuchsia-strong: #a90058;
  --text-main: #3f2435;
  --text-muted: #8a5872;
  --card-bg: rgba(255, 255, 255, 0.58);
  --card-bg-strong: rgba(255, 240, 248, 0.78);
  --border-glow: rgba(212, 20, 114, 0.34);
  --card-radius: 24px;
  --card-shadow: 0 18px 50px rgba(212, 20, 114, 0.14);
  --card-shadow-hover: 0 24px 70px rgba(212, 20, 114, 0.22);
  --font-sans: Nunito, Inter, ui-sans-serif, system-ui, -apple-system,
    BlinkMacSystemFont, "Segoe UI", sans-serif;
  --font-serif: "Playfair Display", Georgia, serif;
  --font-script: "Dancing Script", cursive;
  --font-mono: "JetBrains Mono", "SFMono-Regular", Consolas, monospace;
}

body,
[data-testid="stAppViewContainer"],
.stApp {
  background:
    radial-gradient(circle at top left, rgba(255, 46, 151, 0.24), transparent 34%),
    radial-gradient(circle at top right, rgba(212, 20, 114, 0.20), transparent 36%),
    linear-gradient(135deg, #fff0f8 0%, #ffd6ec 42%, #fff5fa 100%);
  color: var(--text-main);
}

.block-container {
  max-width: min(1180px, calc(100vw - 2rem));
  padding-top: 2rem;
  padding-bottom: 4rem;
}

#MainMenu,
footer,
header {
  visibility: hidden;
}

h1,
h2,
h3,
p,
span,
div {
  font-family: var(--font-sans);
  letter-spacing: 0;
}

.romantic-hero {
  min-height: min(68vh, 46rem);
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: clamp(2rem, 5vw, 4.5rem);
  margin-bottom: 1.5rem;
  border: 1px solid var(--border-glow);
  border-radius: var(--card-radius);
  background:
    linear-gradient(135deg, rgba(255, 255, 255, 0.70), rgba(255, 193, 227, 0.52)),
    radial-gradient(circle at 82% 18%, rgba(212, 20, 114, 0.24), transparent 16rem);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  box-shadow:
    0 18px 55px rgba(212, 20, 114, 0.16),
    inset 0 1px 0 rgba(255, 255, 255, 0.72);
  overflow: hidden;
  position: relative;
}

.romantic-hero > :not(.hero-orb) {
  position: relative;
  z-index: 1;
}

.hero-orb {
  position: absolute;
  inset: auto 8% 12% auto;
  width: 9rem;
  height: 9rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(255, 45, 149, 0.18);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.32);
  filter: blur(0.4px);
  pointer-events: none;
}

.hero-strawberry {
  width: clamp(96px, 12vw, 160px);
  height: auto;
  object-fit: contain;
  image-rendering: pixelated;
  filter: drop-shadow(0 18px 28px rgba(212, 20, 114, 0.20));
}

.hero-kicker,
.section-kicker {
  color: var(--fuchsia-strong);
  font-size: 0.78rem;
  font-weight: 800;
  margin-bottom: 0.8rem;
  text-transform: uppercase;
}

.romantic-hero h1 {
  color: var(--text-main);
  font-family: var(--font-serif);
  font-size: clamp(3rem, 8vw, 6.6rem);
  font-weight: 800;
  line-height: 0.96;
  margin: 0 0 1rem;
}

.hero-subtitle {
  color: var(--text-muted);
  font-size: clamp(1.05rem, 2vw, 1.35rem);
  font-weight: 650;
  max-width: 46rem;
  margin: 0 0 1.4rem;
}

.hero-date,
.date-pill {
  width: fit-content;
  color: var(--fuchsia-strong);
  font-family: var(--font-mono);
  font-size: 0.85rem;
  font-weight: 800;
  padding: 0.55rem 0.85rem;
  border: 1px solid var(--border-glow);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.68);
}

.section-block {
  margin: 2.4rem 0 1.5rem;
}

.reveal-on-scroll {
  opacity: 0;
  transform: translateY(28px);
  transition:
    opacity 760ms cubic-bezier(0.22, 1, 0.36, 1),
    transform 760ms cubic-bezier(0.22, 1, 0.36, 1);
  transition-delay: var(--reveal-delay, 0ms);
  will-change: opacity, transform;
}

.reveal-on-scroll.is-visible {
  opacity: 1;
  transform: translateY(0);
}

.romantic-title-glow,
.section-title,
.timeline-title,
.chart-title,
.closing-card h2 {
  text-shadow:
    0 0 10px rgba(212, 20, 114, 0.30),
    0 0 24px rgba(255, 95, 183, 0.20),
    0 4px 18px rgba(63, 36, 53, 0.10);
}

.section-title {
  color: var(--text-main);
  font-family: var(--font-serif);
  font-size: clamp(1.7rem, 3vw, 2.4rem);
  font-weight: 800 !important;
  line-height: 1.08;
  margin: 0 0 0.35rem;
}

.section-copy {
  color: var(--text-muted);
  font-weight: 650;
  max-width: 45rem;
  margin: 0 0 1.2rem;
}

.bento-grid {
  display: grid;
  grid-auto-flow: dense;
  grid-template-columns: repeat(12, 1fr);
  align-items: stretch;
  gap: 1rem;
  margin: 1.5rem 0;
}

.bento-card,
.timeline-card,
.quote-card,
.word-chip,
.chart-card,
.closing-card,
.special-message-card,
.quote-card-featured {
  background: var(--card-bg);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  border: 1px solid rgba(212, 20, 114, 0.25);
  border-radius: var(--card-radius);
  box-shadow:
    var(--card-shadow),
    inset 0 1px 0 rgba(255, 255, 255, 0.68);
  transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
}

.bento-card.reveal-on-scroll,
.timeline-card.reveal-on-scroll,
.quote-card.reveal-on-scroll,
.word-chip.reveal-on-scroll,
.chart-card.reveal-on-scroll,
.closing-card.reveal-on-scroll,
.special-message-card.reveal-on-scroll,
.quote-card-featured.reveal-on-scroll {
  transition:
    opacity 760ms cubic-bezier(0.22, 1, 0.36, 1),
    transform 760ms cubic-bezier(0.22, 1, 0.36, 1),
    box-shadow 180ms ease,
    border-color 180ms ease;
}

.bento-card:hover,
.timeline-card:hover,
.quote-card:hover,
.word-chip:hover,
.special-message-card:hover,
.quote-card-featured:hover {
  border-color: rgba(212, 20, 114, 0.72);
  box-shadow:
    var(--card-shadow-hover),
    0 0 0 1px rgba(255, 95, 183, 0.22);
  transform: translateY(-3px);
}

.bento-card {
  grid-column: span 4;
  min-height: 12rem;
  padding: 1.4rem;
}

.first-te-amo-card {
  position: relative;
  overflow: hidden;
}

.bento-card.first-te-amo-card,
.timeline-card.first-te-amo-card {
  padding-right: clamp(1.4rem, 10vw, 6rem);
}

.first-te-amo-card > :not(.first-te-amo-heart) {
  position: relative;
  z-index: 1;
}

.first-te-amo-heart {
  position: absolute;
  top: 0.9rem;
  right: 0.9rem;
  z-index: 0;
  width: clamp(42px, 6vw, 72px);
  height: auto;
  object-fit: contain;
  image-rendering: pixelated;
  background: transparent;
  mix-blend-mode: multiply;
  opacity: 0.92;
  filter:
    drop-shadow(0 10px 18px rgba(212, 20, 114, 0.22))
    drop-shadow(0 0 12px rgba(255, 95, 183, 0.24));
  pointer-events: none;
}

.bento-card.large {
  grid-column: span 8;
}

.bento-card.full {
  grid-column: 1 / -1;
}

.metric-label {
  color: var(--text-muted);
  font-size: 0.9rem;
  font-weight: 800 !important;
  margin-bottom: 0.8rem;
}

.metric-number,
.count-value {
  color: var(--fuchsia-strong);
  font-family: var(--font-mono);
  font-size: clamp(2.1rem, 5vw, 4.2rem);
  font-weight: 800 !important;
  line-height: 1;
  overflow-wrap: anywhere;
}

.metric-description {
  color: var(--text-muted);
  font-weight: 650;
  margin-top: 0.8rem;
}

.timeline-list,
.quote-grid,
.word-cloud,
.chart-grid {
  display: grid;
  gap: 1rem;
}

.timeline-list {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.timeline-card {
  padding: 1.15rem;
}

.timeline-title,
.quote-sender {
  color: var(--text-main);
  font-weight: 800 !important;
}

.timeline-detail,
.quote-date {
  color: var(--text-muted);
  font-weight: 650;
  margin-top: 0.5rem;
}

.quote-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.quote-card {
  padding: 1.3rem;
}

.scroll-quote-card {
  position: relative;
  min-height: 12rem;
  padding: 2.65rem 2rem;
  overflow: hidden;
  background-color: transparent;
  background-image: none;
  border: 0;
  border-radius: 0;
  box-shadow: none;
  filter:
    drop-shadow(0 18px 42px rgba(212, 20, 114, 0.16))
    drop-shadow(0 8px 18px rgba(63, 36, 53, 0.06));
  -webkit-backdrop-filter: none;
  backdrop-filter: none;
}

.scroll-quote-card::before,
.scroll-quote-card::after {
  content: "";
  position: absolute;
  pointer-events: none;
  -webkit-mask-image: var(--scroll-bg-image, none);
  mask-image: var(--scroll-bg-image, none);
  -webkit-mask-position: center;
  mask-position: center;
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
  -webkit-mask-size: 100% 100%;
  mask-size: 100% 100%;
}

.scroll-quote-card::before {
  inset: 0;
  z-index: 0;
  background:
    linear-gradient(135deg, rgba(255, 95, 183, 0.98), rgba(169, 0, 88, 0.88)),
    radial-gradient(circle at 18% 12%, rgba(255, 255, 255, 0.54), transparent 36%);
}

.scroll-quote-card::after {
  inset: 4px;
  z-index: 0;
  background:
    linear-gradient(135deg, rgba(255, 255, 255, 0.52), rgba(255, 240, 248, 0.48)),
    radial-gradient(circle at 24% 20%, rgba(255, 255, 255, 0.54), transparent 34%),
    radial-gradient(circle at 82% 78%, rgba(255, 95, 183, 0.20), transparent 38%),
    linear-gradient(135deg, rgba(255, 246, 251, 0.54), rgba(255, 214, 236, 0.42));
  -webkit-backdrop-filter: blur(18px);
  backdrop-filter: blur(18px);
}

.scroll-quote-card:hover {
  border-color: transparent;
  box-shadow: none;
  filter:
    drop-shadow(0 24px 58px rgba(212, 20, 114, 0.22))
    drop-shadow(0 0 0 rgba(255, 95, 183, 0.22));
}

.scroll-quote-card .quote-text,
.scroll-quote-card .quote-sender,
.scroll-quote-card .quote-date {
  position: relative;
  z-index: 1;
}

.quote-text {
  color: var(--text-main);
  font-size: 1.02rem;
  font-weight: 650;
  line-height: 1.55;
  text-shadow:
    0 0 8px rgba(255, 95, 183, 0.12),
    0 2px 12px rgba(63, 36, 53, 0.06);
}

.scroll-quote-card .quote-sender {
  color: var(--fuchsia-strong);
  text-shadow:
    0 0 10px rgba(212, 20, 114, 0.22),
    0 0 18px rgba(255, 95, 183, 0.16);
}

.word-cloud {
  grid-template-columns: repeat(auto-fit, minmax(8rem, 1fr));
}

.word-chip {
  padding: 1rem;
  text-align: center;
}

.word-chip strong {
  color: var(--fuchsia-strong);
  display: block;
  font-size: 1.1rem;
  font-weight: 800;
}

.word-chip span {
  color: var(--text-muted);
  font-family: var(--font-mono);
  font-size: 0.82rem;
  font-weight: 800;
}

.chart-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.chart-card {
  padding: 1rem;
  margin-bottom: 1rem;
}

.chart-title {
  color: var(--fuchsia-strong);
  font-family: var(--font-serif);
  font-size: 1.05rem;
  font-weight: 800 !important;
  line-height: 1.25;
  margin: 0 0 0.8rem;
}

.chart-card svg text,
.chart-card canvas + div text {
  font-weight: 700 !important;
}

.closing-card {
  padding: clamp(2rem, 4vw, 3rem);
  margin-top: 2.5rem;
  background: var(--card-bg-strong);
  text-align: center;
}

.closing-card h2 {
  color: var(--text-main);
  font-family: var(--font-serif);
  font-size: clamp(1.8rem, 4vw, 3rem);
  font-weight: 800;
  margin: 0 0 0.8rem;
}

.closing-card p {
  color: var(--text-muted);
  font-weight: 650;
  margin: 0 auto;
  max-width: 40rem;
}

.stAlert {
  border-radius: 18px;
}

.safe-error-card {
  max-width: 680px;
  margin: 6rem auto;
  padding: 2rem;
  border: 1px solid rgba(212, 20, 114, 0.28);
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.72);
  box-shadow: 0 24px 70px rgba(212, 20, 114, 0.18);
  text-align: center;
}

.safe-error-card h1 {
  color: var(--text-main);
  font-family: var(--font-serif);
  font-size: clamp(1.8rem, 4vw, 3rem);
  font-weight: 800;
  margin: 0 0 0.8rem;
}

.safe-error-card p {
  color: var(--text-muted);
  font-weight: 650;
  margin: 0;
}

button[kind="primary"],
.stButton > button {
  background: linear-gradient(135deg, var(--pink-mid), var(--fuchsia));
  border: 1px solid rgba(212, 20, 114, 0.48);
  border-radius: 999px;
  color: #ffffff;
  font-family: var(--font-sans);
  font-weight: 800;
  box-shadow: 0 12px 28px rgba(212, 20, 114, 0.28);
}

button[kind="primary"]:hover,
.stButton > button:hover {
  border-color: rgba(212, 20, 114, 0.84);
  box-shadow: 0 16px 36px rgba(212, 20, 114, 0.34);
}

.special-message-card,
.quote-card-featured {
  padding: clamp(1.6rem, 4vw, 2.4rem);
  margin: 0 0 1.2rem;
  background:
    linear-gradient(135deg, rgba(255, 240, 248, 0.82), rgba(255, 193, 227, 0.62)),
    rgba(255, 255, 255, 0.58);
  border-color: rgba(212, 20, 114, 0.42);
  box-shadow:
    0 24px 75px rgba(212, 20, 114, 0.28),
    0 0 0 1px rgba(255, 95, 183, 0.20);
}

.glitter-accent {
  position: relative;
  overflow: hidden;
}

.glitter-accent > * {
  position: relative;
  z-index: 1;
}

.glitter-accent::after {
  content: "";
  position: absolute;
  inset: -40%;
  background:
    radial-gradient(circle, rgba(255, 255, 255, 0.85) 0 1px, transparent 2px),
    linear-gradient(
      110deg,
      transparent 0%,
      transparent 38%,
      rgba(255, 255, 255, 0.55) 48%,
      transparent 58%,
      transparent 100%
    );
  background-size: 28px 28px, 220% 100%;
  opacity: 0.28;
  transform: translateX(-40%);
  animation: romantic-glitter-sweep 4.8s ease-in-out infinite;
  pointer-events: none;
}

.glossy-fuchsia-text {
  display: inline-block;
  background: linear-gradient(
    180deg,
    #fff6fb 0%,
    #ff8ccc 22%,
    #ff2f9b 48%,
    #b80061 78%,
    #fff0fa 100%
  );
  background-clip: text;
  color: transparent;
  -webkit-background-clip: text;
  text-shadow:
    0 1px 0 rgba(255, 255, 255, 0.75),
    0 8px 24px rgba(212, 20, 114, 0.30),
    0 0 28px rgba(255, 95, 183, 0.34);
}

@keyframes romantic-glitter-sweep {
  0% {
    transform: translateX(-45%) rotate(8deg);
    opacity: 0;
  }

  35% {
    opacity: 0.18;
  }

  55% {
    opacity: 0.38;
  }

  100% {
    transform: translateX(45%) rotate(8deg);
    opacity: 0;
  }
}

.special-message-kicker {
  color: var(--fuchsia-strong);
  font-family: var(--font-script);
  font-size: clamp(1.8rem, 4vw, 2.7rem);
  font-weight: 800 !important;
  line-height: 1.05;
  margin-bottom: 1rem;
}

.special-message-subtitle {
  color: var(--text-muted);
  font-size: 1rem;
  font-weight: 650;
  margin: 0 0 1rem;
}

.special-message-text {
  color: var(--text-main);
  font-family: var(--font-serif);
  font-size: clamp(1.45rem, 3vw, 2.35rem);
  font-weight: 700;
  line-height: 1.32;
  margin: 0 0 1.2rem;
}

.special-message-meta {
  color: var(--text-muted);
  display: flex;
  flex-wrap: wrap;
  gap: 0.7rem;
  justify-content: space-between;
  font-family: var(--font-mono);
  font-size: 0.88rem;
  font-weight: 800;
}

.ig-chat-card {
  width: 100%;
  padding: clamp(1.25rem, 3vw, 1.7rem);
  background:
    linear-gradient(145deg, rgba(255, 255, 255, 0.72), rgba(255, 218, 238, 0.72)),
    rgba(255, 255, 255, 0.58);
  margin: 1rem 0 1.2rem;
}

.ig-chat-header {
  margin-bottom: 1rem;
}

.ig-chat-title {
  margin-bottom: 0.45rem;
}

.manual-subtitle {
  max-width: 42rem;
}

.ig-message-list {
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.special-message-block {
  margin-top: 1rem;
  padding: 1rem;
  border: 1px solid rgba(212, 20, 114, 0.22);
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.38);
}

.special-message-block + .special-message-block {
  margin-top: 1.1rem;
}

.special-message-block-title {
  color: var(--fuchsia-strong);
  font-family: var(--font-script);
  font-size: calc(clamp(1.8rem, 4vw, 2.7rem) - 2px);
  font-style: italic;
  font-weight: 800 !important;
  line-height: 1.05;
  margin-bottom: 0.8rem;
  text-shadow:
    0 0 10px rgba(212, 20, 114, 0.34),
    0 0 24px rgba(255, 95, 183, 0.24),
    0 4px 18px rgba(63, 36, 53, 0.10);
}

.ig-bubble {
  max-width: min(78%, 620px);
  padding: 0.9rem 1rem;
  border-radius: 24px;
  box-shadow: 0 12px 28px rgba(80, 30, 60, 0.10);
  font-weight: 650;
  line-height: 1.45;
}

.ig-bubble p {
  margin: 0;
  font-weight: 650;
}

.ig-bubble-her {
  align-self: flex-start;
  background: rgba(255, 255, 255, 0.84);
  border: 1px solid rgba(255, 95, 183, 0.30);
  border-bottom-left-radius: 8px;
  color: var(--text-main);
}

.ig-bubble-me {
  align-self: flex-end;
  background: linear-gradient(135deg, #ff5fb7 0%, #d41472 48%, #a90058 100%);
  border: 1px solid rgba(255, 255, 255, 0.30);
  border-bottom-right-radius: 8px;
  box-shadow: 0 18px 36px rgba(212, 20, 114, 0.28);
  color: #ffffff;
}

.ig-bubble-meta {
  display: block;
  margin-top: 0.45rem;
  font-family: var(--font-mono);
  font-size: 0.78rem;
  font-weight: 800;
  opacity: 0.76;
}

.message-meta-separator {
  padding: 0 0.25rem;
}

.ig-bubble-me .ig-bubble-meta {
  color: rgba(255, 255, 255, 0.88);
}

.ig-bubble-her .ig-bubble-meta {
  color: var(--text-muted);
}

@media (max-width: 768px) {
  .block-container {
    padding-left: 1rem;
    padding-right: 1rem;
  }

  .romantic-hero {
    min-height: 58vh;
    padding: 2rem;
  }

  .hero-orb {
    width: 6rem;
    height: 6rem;
    inset: auto 1rem 1rem auto;
  }

  .hero-strawberry {
    width: clamp(78px, 24vw, 112px);
  }

  .bento-grid,
  .timeline-list,
  .quote-grid,
  .chart-grid {
    grid-template-columns: 1fr;
  }

  .bento-card,
  .bento-card.large,
  .bento-card.full {
    grid-column: 1 / -1;
  }

  .bento-card.first-te-amo-card,
  .timeline-card.first-te-amo-card {
    padding-right: 1.4rem;
  }

  .first-te-amo-heart {
    top: 0.75rem;
    right: 0.75rem;
    width: 44px;
    opacity: 0.82;
  }

  .scroll-quote-card {
    padding: 2.2rem 1.35rem;
  }

  .ig-bubble {
    max-width: 92%;
  }
}

@media (prefers-reduced-motion: reduce) {
  .reveal-on-scroll {
    opacity: 1;
    transform: none;
    transition: none;
  }

  .glitter-accent::after {
    animation: none;
    opacity: 0.16;
  }
}
</style>
"""
