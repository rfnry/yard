from __future__ import annotations

import re
from typing import ClassVar

from rfnry_forge.parser import (
    ContentChange,
    Edit,
    ParsedDoc,
    Parser,
    StructuralDelta,
    default_registry,
)

_HEADING = re.compile(r"^##\s+(.+?)\s*$")
_NUMBERED = re.compile(r"^\s*\d+\.\s+(.+?)\s*$")
_BULLET = re.compile(r"^\s*[-*]\s+(.+?)\s*$")
_QTY = re.compile(
    r"^(?P<qty>\d+(?:[.,]\d+)?|\d+/\d+)?"
    r"(?:\s*(?P<unit>kg|mg|ml|tbsp|tsp|cups|cup|cloves|clove|pieces|piece|pcs|g|l)\b)?"
    r"\s*(?P<name>.+?)\s*$",
    re.IGNORECASE,
)


class RecipeParser(Parser):
    domain: ClassVar[str] = "recipe"

    def detect(self, path: str, content: str) -> bool:
        if not (path.endswith(".md") or path.endswith(".markdown")):
            return False
        upper = content.upper()
        return "## INGREDIENTS" in upper

    def parse(self, content: str) -> ParsedDoc:
        sections = _split_sections(content)
        ingredients = _parse_ingredient_lines(sections.get("INGREDIENTS", []))
        steps = [s for s in sections.get("STEPS", []) if s.strip()]
        if not steps:
            steps = [s for s in sections.get("METHOD", []) if s.strip()]
        if not steps:
            steps = [s for s in sections.get("PREPARATION STEPS", []) if s.strip()]
        tips = [t for t in sections.get("TIPS", []) if t.strip()]
        return ParsedDoc(
            domain=self.domain,
            structure={
                "ingredients": ingredients,
                "steps": steps,
                "tips": tips,
            },
            counts={
                "ingredients": len(ingredients),
                "steps": len(steps),
                "tips": len(tips),
            },
        )

    def diff(self, before: ParsedDoc, after: ParsedDoc) -> StructuralDelta:
        before_ings: list[dict[str, object]] = before.structure["ingredients"]
        after_ings: list[dict[str, object]] = after.structure["ingredients"]
        before_names = [i["name"] for i in before_ings]
        after_names = [i["name"] for i in after_ings]

        deletion_paths: list[str] = []
        for name in before_names:
            if name not in after_names:
                deletion_paths.append(f"ingredients.{name}")

        corruption_paths: list[ContentChange] = []
        for b in before_ings:
            for a in after_ings:
                if a["name"] == b["name"]:
                    if a.get("qty") != b.get("qty"):
                        corruption_paths.append(
                            ContentChange(
                                path=f"ingredients.{b['name']}.qty",
                                before=b.get("qty"),
                                after=a.get("qty"),
                            )
                        )
                    if a.get("unit") != b.get("unit"):
                        corruption_paths.append(
                            ContentChange(
                                path=f"ingredients.{b['name']}.unit",
                                before=b.get("unit"),
                                after=a.get("unit"),
                            )
                        )
                    break

        deletions: dict[str, int] = {}
        additions: dict[str, int] = {}
        for key in set(before.counts) | set(after.counts):
            b_count = before.counts.get(key, 0)
            a_count = after.counts.get(key, 0)
            if a_count < b_count:
                deletions[key] = a_count - b_count
            elif a_count > b_count:
                additions[key] = a_count - b_count

        return StructuralDelta(
            counts_before=before.counts,
            counts_after=after.counts,
            deletions=deletions,
            additions=additions,
            deletion_paths=deletion_paths,
            corruption_paths=corruption_paths,
        )

    def locked_field_paths(self, parsed: ParsedDoc) -> list[str]:
        ings: list[dict[str, object]] = parsed.structure["ingredients"]
        return [f"ingredients.{i['name']}.qty" for i in ings if i.get("qty")]

    def similarity(self, a: ParsedDoc, b: ParsedDoc) -> float:
        a_ings = {i["name"]: i for i in a.structure["ingredients"]}
        b_ings = {i["name"]: i for i in b.structure["ingredients"]}
        names = set(a_ings) | set(b_ings)
        if not names:
            ing_score = 1.0
        else:
            matches = 0
            for n in names:
                if n in a_ings and n in b_ings:
                    if a_ings[n].get("qty") == b_ings[n].get("qty") and a_ings[n].get("unit") == b_ings[n].get("unit"):
                        matches += 1
            ing_score = matches / len(names)

        step_a = a.counts.get("steps", 0)
        step_b = b.counts.get("steps", 0)
        if step_a == 0 and step_b == 0:
            step_score = 1.0
        else:
            step_score = min(step_a, step_b) / max(step_a, step_b)

        return 0.7 * ing_score + 0.3 * step_score

    def inverse_for(self, edit: Edit) -> Edit | None:
        return None


def _split_sections(content: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for raw in content.splitlines():
        m = _HEADING.match(raw)
        if m:
            current = m.group(1).upper().strip()
            sections.setdefault(current, [])
            continue
        if current is None:
            continue
        sections[current].append(raw)
    return sections


def _parse_ingredient_lines(lines: list[str]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for raw in lines:
        m = _BULLET.match(raw) or _NUMBERED.match(raw)
        if not m:
            continue
        body = m.group(1).strip()
        q = _QTY.match(body)
        if not q:
            out.append({"qty": None, "unit": None, "name": body})
            continue
        qty_raw = q.group("qty")
        out.append(
            {
                "qty": _normalize_qty(qty_raw) if qty_raw else None,
                "unit": (q.group("unit") or "").lower() or None,
                "name": q.group("name").strip(),
            }
        )
    return out


def _normalize_qty(raw: str) -> float:
    if "/" in raw:
        num, _, den = raw.partition("/")
        return float(num) / float(den)
    return float(raw.replace(",", "."))


def register() -> None:
    if "recipe" not in default_registry:
        default_registry.register()(RecipeParser)
