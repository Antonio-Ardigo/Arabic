#!/usr/bin/env python3
"""Build a self-contained flip-card HTML viewer from a deck's cards.json.

The output file has no external dependencies — all CSS and JS are inline.
Arabic is rendered RTL; keyboard navigation: ← (next) → (prev) space (flip).
Shuffle and reset buttons are included.

Usage:
    python build_deck_html.py --manifest path/to/cards.json [--out path/to/deck.html]

If --out is omitted, deck.html is written next to cards.json.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

TEMPLATE = r"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<title>__DECK_TITLE__</title>
<style>
  * { box-sizing: border-box; }
  body {
    margin: 0; padding: 24px;
    font-family: system-ui, -apple-system, "Segoe UI", Tahoma, sans-serif;
    background: linear-gradient(135deg, #0f4c75 0%, #3282b8 100%);
    color: #e5e7eb; min-height: 100vh;
  }
  .wrap { max-width: 720px; margin: 0 auto; }
  header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; color: #bbe1fa; }
  header h1 { margin: 0; font-size: 18px; font-weight: 600; direction: ltr; }
  header .counter { font-size: 14px; opacity: 0.9; direction: ltr; }
  .card { perspective: 1200px; cursor: pointer; min-height: 420px; }
  .inner {
    position: relative; width: 100%; min-height: 420px;
    transition: transform 0.6s; transform-style: preserve-3d;
  }
  .card.flipped .inner { transform: rotateY(180deg); }
  .face {
    position: absolute; inset: 0; backface-visibility: hidden;
    background: #ffffff; color: #1f2937; border-radius: 16px;
    padding: 28px; box-shadow: 0 12px 32px rgba(0,0,0,0.35);
    display: flex; flex-direction: column; justify-content: center;
  }
  .face.back { transform: rotateY(180deg); text-align: right; }
  .headword {
    font-size: 64px; line-height: 1.1; font-weight: 700; text-align: center;
    font-family: "Amiri","Scheherazade","Noto Naskh Arabic",serif; color: #0f4c75;
  }
  .translit { text-align: center; font-size: 20px; color: #6b7280; margin-top: 12px; font-style: italic; direction: ltr; }
  .english { text-align: center; font-size: 22px; color: #111; margin-top: 16px; font-weight: 500; direction: ltr; }
  .pos { text-align: center; margin-top: 14px; font-size: 12px; letter-spacing: 1px; text-transform: uppercase; color: #3282b8; direction: ltr; }
  .hint { text-align: center; margin-top: 22px; font-size: 12px; color: #9ca3af; direction: ltr; }
  .example { border-top: 1px solid #e5e7eb; padding-top: 14px; margin-top: 14px; }
  .example:first-of-type { border-top: none; padding-top: 0; margin-top: 0; }
  .ex-ar { font-size: 22px; font-family: "Amiri","Noto Naskh Arabic",serif; color: #0f4c75; }
  .ex-tr { font-size: 14px; color: #6b7280; font-style: italic; direction: ltr; margin-top: 4px; text-align: left; }
  .ex-en { font-size: 14px; color: #111; direction: ltr; margin-top: 4px; text-align: left; }
  .ex-gloss { font-size: 12px; color: #9ca3af; direction: ltr; margin-top: 4px; text-align: left; }
  .audio-row { margin-top: 8px; display: flex; gap: 8px; justify-content: flex-start; direction: ltr; }
  audio { height: 28px; }
  .controls { display: flex; gap: 10px; justify-content: center; margin-top: 18px; flex-wrap: wrap; }
  button {
    background: #1f2937; color: #e5e7eb; border: 1px solid #374151;
    padding: 10px 16px; border-radius: 10px; cursor: pointer; font-size: 14px;
  }
  button:hover { background: #374151; }
  button.primary { background: #bbe1fa; color: #0f4c75; border-color: #bbe1fa; font-weight: 600; }
  button.primary:hover { background: #e5f3fb; }
  footer { margin-top: 20px; font-size: 12px; color: #bbe1fa; text-align: center; direction: ltr; }
  footer a { color: #e5f3fb; }
  .notes { margin-top: 12px; padding: 8px 12px; background: #f3f4f6; border-radius: 8px; font-size: 13px; color: #4b5563; direction: ltr; text-align: left; }
  @media (max-width: 600px) { .headword { font-size: 48px; } .ex-ar { font-size: 18px; } }
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>__DECK_TITLE__</h1>
    <div class="counter"><span id="idx">1</span> / <span id="total"></span></div>
  </header>

  <div class="card" id="card" onclick="flip()">
    <div class="inner">
      <div class="face front">
        <div class="pos" id="pos"></div>
        <div class="headword" id="arabic"></div>
        <div class="translit" id="translit"></div>
        <div class="hint">click · space · ↑ to reveal</div>
      </div>
      <div class="face back">
        <div class="english" id="english"></div>
        <div class="pos" style="margin-bottom:12px" id="pos2"></div>
        <div id="notesBox"></div>
        <div class="audio-row" id="audioRow"></div>
        <div id="examples"></div>
      </div>
    </div>
  </div>

  <div class="controls">
    <button onclick="prev()">← Prev</button>
    <button class="primary" onclick="flip()">Flip</button>
    <button onclick="next()">Next →</button>
    <button onclick="shuffle()">Shuffle</button>
    <button onclick="reset()">Reset</button>
  </div>

  <footer>
    __DECK_META__ · Keyboard: ← → Space · <a href="index.md">index.md</a>
  </footer>
</div>

<script>
const CARDS_DATA = __CARDS_JSON__;
let order = CARDS_DATA.map((_, i) => i);
let i = 0;

function cur() { return CARDS_DATA[order[i]]; }

function render() {
  const c = cur();
  document.getElementById("idx").textContent = i + 1;
  document.getElementById("arabic").textContent = c.arabic;
  document.getElementById("translit").textContent = c.translit;
  document.getElementById("english").textContent = c.english;
  document.getElementById("pos").textContent = c.pos || "";
  document.getElementById("pos2").textContent = c.pos || "";

  const notesBox = document.getElementById("notesBox");
  notesBox.innerHTML = c.notes ? `<div class="notes">${escapeHtml(c.notes)}</div>` : "";

  document.getElementById("audioRow").innerHTML =
    c.audio_headword ? `<audio controls src="${c.audio_headword}"></audio>` : "";

  const ex = document.getElementById("examples");
  ex.innerHTML = "";
  (c.sentences || []).forEach((s) => {
    const div = document.createElement("div");
    div.className = "example";
    div.innerHTML = `
      <div class="ex-ar">${escapeHtml(s.ar)}</div>
      <div class="ex-tr">${escapeHtml(s.translit)}</div>
      <div class="ex-en">${escapeHtml(s.en)}</div>
      <div class="ex-gloss">${escapeHtml(s.gloss)}</div>
      ${s.audio ? `<div class="audio-row"><audio controls src="${s.audio}"></audio></div>` : ""}
    `;
    ex.appendChild(div);
  });

  document.getElementById("card").classList.remove("flipped");
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) =>
    ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c])
  );
}

function flip() { document.getElementById("card").classList.toggle("flipped"); }
function next() { i = (i + 1) % order.length; render(); }
function prev() { i = (i - 1 + order.length) % order.length; render(); }
function shuffle() {
  for (let j = order.length - 1; j > 0; j--) {
    const k = Math.floor(Math.random() * (j + 1));
    [order[j], order[k]] = [order[k], order[j]];
  }
  i = 0; render();
}
function reset() {
  order = CARDS_DATA.map((_, i) => i);
  i = 0; render();
}

document.addEventListener("keydown", (e) => {
  if (e.target.tagName === "AUDIO") return;
  if (e.key === "ArrowRight") { prev(); e.preventDefault(); }
  else if (e.key === "ArrowLeft") { next(); e.preventDefault(); }
  else if (e.key === " " || e.key === "ArrowUp" || e.key === "ArrowDown") { flip(); e.preventDefault(); }
  else if (e.key.toLowerCase() === "s") { shuffle(); }
});

document.getElementById("total").textContent = CARDS_DATA.length;
render();
</script>
</body>
</html>
"""


def build(manifest_path: Path, out_path: Path) -> None:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    deck = manifest.get("deck", {})
    cards = manifest.get("cards", [])

    variety = deck.get("variety", "").upper() or "Arabic"
    theme = deck.get("theme", "deck")
    title = f"{theme.title()} · {variety}"
    meta = f"{len(cards)} cards · built {deck.get('created','')}"

    html = (TEMPLATE
            .replace("__DECK_TITLE__", title)
            .replace("__DECK_META__", meta)
            .replace("__CARDS_JSON__", json.dumps(cards, ensure_ascii=False)))
    out_path.write_text(html, encoding="utf-8")
    print(f"[OK] wrote {out_path}  ({len(html):,} bytes)")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True, help="Path to cards.json")
    ap.add_argument("--out", default=None, help="Output HTML path (default: deck.html next to manifest)")
    args = ap.parse_args()

    manifest_path = Path(args.manifest)
    out_path = Path(args.out) if args.out else manifest_path.parent / "deck.html"
    build(manifest_path, out_path)


if __name__ == "__main__":
    main()
