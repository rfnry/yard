from __future__ import annotations

from collections.abc import AsyncIterator
from typing import TYPE_CHECKING

from rfnry_voice_protocol import Tool, VoiceEvent

from src.data import (
    UnknownAccount,
    UnknownRental,
    get_account,
    list_rentals_for_account,
    refund_rental,
)

if TYPE_CHECKING:
    from rfnry_voice_server.session import VoiceSession
    from rfnry_voice_server.session.handler import EventSender, HandlerContext


TOOLS: list[Tool] = [
    Tool(
        name="lookup_account",
        description="Look up a customer account by id (e.g. A-001).",
        parameters={
            "type": "object",
            "properties": {"account_id": {"type": "string"}},
            "required": ["account_id"],
        },
        quarantined=False,
    ),
    Tool(
        name="list_rentals",
        description="List all rentals associated with a customer account.",
        parameters={
            "type": "object",
            "properties": {"account_id": {"type": "string"}},
            "required": ["account_id"],
        },
        quarantined=False,
    ),
    Tool(
        name="refund_rental",
        description=(
            "Mark a rental as refunded with a brief reason. Confirm with the caller "
            "before invoking."
        ),
        parameters={
            "type": "object",
            "properties": {
                "rental_id": {"type": "string"},
                "reason": {"type": "string"},
            },
            "required": ["rental_id", "reason"],
        },
        quarantined=False,
    ),
    Tool(
        name="escalate_to_human",
        description="Hand off the call to a human agent (logs the request).",
        parameters={
            "type": "object",
            "properties": {"summary": {"type": "string"}},
            "required": ["summary"],
        },
        quarantined=False,
    ),
]


def register_tool_handlers(session: VoiceSession) -> None:
    @session.on_tool_call("lookup_account")
    async def _lookup_account(
        ctx: HandlerContext, send: EventSender
    ) -> AsyncIterator[VoiceEvent]:
        account_id = str(ctx.args.get("account_id", ""))
        try:
            account = get_account(account_id)
            value = {"id": account.id, "name": account.name, "email": account.email}
        except UnknownAccount as exc:
            value = {"error": str(exc)}
        yield send.tool_result(value=value, correlation_id=ctx.event.correlation_id)  # type: ignore[union-attr]

    @session.on_tool_call("list_rentals")
    async def _list_rentals(
        ctx: HandlerContext, send: EventSender
    ) -> AsyncIterator[VoiceEvent]:
        account_id = str(ctx.args.get("account_id", ""))
        rentals = list_rentals_for_account(account_id)
        value = {
            "rentals": [
                {
                    "id": r.id,
                    "vehicle": r.vehicle,
                    "pickup_date": r.pickup_date,
                    "return_date": r.return_date,
                    "status": r.status,
                    "daily_rate_usd": r.daily_rate_usd,
                }
                for r in rentals
            ]
        }
        yield send.tool_result(value=value, correlation_id=ctx.event.correlation_id)  # type: ignore[union-attr]

    @session.on_tool_call("refund_rental")
    async def _refund_rental(
        ctx: HandlerContext, send: EventSender
    ) -> AsyncIterator[VoiceEvent]:
        rental_id = str(ctx.args.get("rental_id", ""))
        reason = str(ctx.args.get("reason", ""))
        try:
            rental = refund_rental(rental_id, reason=reason)
            value = {"id": rental.id, "status": rental.status, "reason": reason}
        except UnknownRental as exc:
            value = {"error": str(exc)}
        yield send.tool_result(value=value, correlation_id=ctx.event.correlation_id)  # type: ignore[union-attr]

    @session.on_tool_call("escalate_to_human")
    async def _escalate(
        ctx: HandlerContext, send: EventSender
    ) -> AsyncIterator[VoiceEvent]:
        summary = str(ctx.args.get("summary", ""))
        # Real impl would page a human queue; here we just log + ack.
        value = {"status": "queued", "summary": summary}
        yield send.tool_result(value=value, correlation_id=ctx.event.correlation_id)  # type: ignore[union-attr]
