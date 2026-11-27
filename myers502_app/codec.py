from __future__ import annotations

import base64
from typing import Literal

CodecMode = Literal["auto", "utf8", "ps"]


def normalize_b64(raw_text: str) -> str:
    """Remove extra whitespace/line breaks and restore missing Base64 '=' padding."""
    cleaned = "".join(raw_text.strip().split())
    remainder = len(cleaned) % 4
    if remainder:
        cleaned += "=" * (4 - remainder)
    return cleaned


def decode_base64(text: str, mode: CodecMode = "auto") -> str:
    """Decode Base64 using UTF-8, PowerShell UTF-16LE, or automatic detection."""
    normalized = normalize_b64(text)
    raw_bytes = base64.b64decode(normalized, validate=False)

    if mode == "utf8":
        return raw_bytes.decode("utf-8", errors="replace")
    if mode == "ps":
        return raw_bytes.decode("utf-16-le", errors="replace")

    if len(raw_bytes) % 2 == 0 and len(raw_bytes) > 0:
        try:
            ps_candidate = raw_bytes.decode("utf-16-le")
            printable = sum(ch.isprintable() or ch in "\r\n\t" for ch in ps_candidate)
            if (printable / len(ps_candidate)) > 0.85 and "\x00" not in ps_candidate:
                return ps_candidate
        except UnicodeDecodeError:
            pass

    return raw_bytes.decode("utf-8", errors="replace")


def encode_base64(text: str, mode: Literal["utf8", "ps"] = "utf8") -> str:
    """Encode text to Base64 using UTF-8 or PowerShell (-EncodedCommand) UTF-16LE."""
    payload = text.encode("utf-16-le") if mode == "ps" else text.encode("utf-8")
    return base64.b64encode(payload).decode("ascii")