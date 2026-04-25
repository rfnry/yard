from __future__ import annotations

import re
from dataclasses import dataclass

from rfnry_chat_protocol import Identity

_MENTION_RE = re.compile(r"@([\w-]+)")


@dataclass(frozen=True)
class ParsedMentions:
    recipients: list[str]
    text_without_leading_mentions: str


def parse_member_mentions(text: str, members: list[Identity]) -> ParsedMentions:

    by_name = {m.name.lower(): m for m in members}

    seen: set[str] = set()
    recipients: list[str] = []
    for raw in _MENTION_RE.findall(text):
        token = raw.lower()
        hit = by_name.get(token)
        if hit is None:
            continue
        if hit.id in seen:
            continue
        seen.add(hit.id)
        recipients.append(hit.id)

    body = text.lstrip()
    while True:
        m = _MENTION_RE.match(body)
        if m is None:
            break
        candidate = m.group(1).lower()
        if candidate not in by_name:
            break
        body = body[m.end() :].lstrip()

    return ParsedMentions(recipients=recipients, text_without_leading_mentions=body or text)
