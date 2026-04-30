from __future__ import annotations

import asyncio
import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.legal_assistant.routes import router as legal_router
from src.marketplace_assistant.routes import router as marketplace_router
from src.support_assistant.routes import router as support_router

PORT = int(os.environ.get("PORT", "8200"))

app = FastAPI(title="rfnry-examples-backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(support_router, prefix="/support-assistant")
app.include_router(marketplace_router, prefix="/marketplace-assistant")
app.include_router(legal_router, prefix="/legal-assistant")


if __name__ == "__main__":
    print(f"rfnry-examples-backend listening on http://0.0.0.0:{PORT}")
    print("  /support-assistant/    car-parts factory CS data")
    print("  /marketplace-assistant/ electronics retailer sales/marketing data")
    print("  /legal-assistant/      litigation lookups")
    try:
        uvicorn.run(app, host="0.0.0.0", port=PORT)
    except asyncio.CancelledError:
        pass
