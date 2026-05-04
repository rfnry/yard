# /// script
# requires-python = ">=3.12"
# dependencies = ["fpdf2>=2.8.0"]
# ///
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from fpdf import FPDF
from fpdf.enums import XPos, YPos

_HERE = Path(__file__).resolve().parent

_LATIN1_REPLACEMENTS = {
    "—": "-",
    "–": "-",
    "•": "*",
    "“": '"',
    "”": '"',
    "‘": "'",
    "’": "'",
    "…": "...",
    "→": "->",
    "≤": "<=",
    "≥": ">=",
    "×": "x",
    "°": " deg",
    "µ": "u",
}


def _to_latin1(text: str) -> str:
    for src, repl in _LATIN1_REPLACEMENTS.items():
        text = text.replace(src, repl)
    return text.encode("latin-1", errors="replace").decode("latin-1")


class _Renderer(FPDF):
    def header(self) -> None:
        pass

    def footer(self) -> None:
        self.set_y(-12)
        self.set_font("Helvetica", size=8)
        self.set_text_color(120)
        self.cell(0, 8, f"page {self.page_no()}", align="C")


def _render_paragraph(pdf: _Renderer, line: str) -> None:
    parts: list[tuple[str, str]] = []
    cursor = 0
    for match in re.finditer(r"\*\*(.+?)\*\*", line):
        if match.start() > cursor:
            parts.append(("regular", line[cursor : match.start()]))
        parts.append(("bold", match.group(1)))
        cursor = match.end()
    if cursor < len(line):
        parts.append(("regular", line[cursor:]))

    for style, text in parts:
        pdf.set_font("Helvetica", style="B" if style == "bold" else "", size=11)
        pdf.write(6, text)
    pdf.ln(8)


def render_markdown(md: str) -> bytes:
    pdf = _Renderer(format="A4", unit="mm")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()
    pdf.set_margins(18, 18, 18)

    for raw in md.splitlines():
        line = _to_latin1(raw.rstrip())
        if not line:
            pdf.ln(4)
            continue

        if line.startswith("# "):
            pdf.set_font("Helvetica", style="B", size=18)
            pdf.cell(0, 10, line[2:], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(2)
        elif line.startswith("## "):
            pdf.set_font("Helvetica", style="B", size=14)
            pdf.cell(0, 8, line[3:], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(1)
        elif line.startswith("### "):
            pdf.set_font("Helvetica", style="B", size=12)
            pdf.cell(0, 7, line[4:], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        elif line.startswith("- ") or line.startswith("* "):
            pdf.set_font("Helvetica", size=11)
            pdf.cell(6)
            pdf.cell(4, 6, "*")
            _render_paragraph(pdf, line[2:])
        elif re.match(r"^\d+\.\s", line):
            pdf.set_font("Helvetica", size=11)
            num, _, rest = line.partition(" ")
            pdf.cell(8, 6, num)
            _render_paragraph(pdf, rest)
        else:
            _render_paragraph(pdf, line)

    return bytes(pdf.output())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render markdown files to PDF (defaults to every *.md alongside this script).",
    )
    parser.add_argument(
        "inputs",
        nargs="*",
        type=Path,
        help="markdown files to render",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=_HERE,
        help=f"output directory (default: {_HERE})",
    )
    args = parser.parse_args(argv)

    inputs: list[Path] = args.inputs or sorted(_HERE.glob("*.md"))
    if not inputs:
        print("no markdown files found", file=sys.stderr)
        return 1

    args.output_dir.mkdir(parents=True, exist_ok=True)

    for src in inputs:
        if not src.exists():
            print(f"missing: {src}", file=sys.stderr)
            return 1
        out = args.output_dir / (src.stem + ".pdf")
        out.write_bytes(render_markdown(src.read_text(encoding="utf-8")))
        print(f"{src} -> {out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
