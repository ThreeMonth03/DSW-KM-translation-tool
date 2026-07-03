"""Deterministic ordering helpers for KM entity events."""

from __future__ import annotations


def event_type_priority(event_type: str) -> int:
    """Return the effective apply-order priority for one KM event type."""

    if event_type.startswith("Add"):
        return 0
    if event_type.startswith("Edit"):
        return 1
    if event_type.startswith("Move"):
        return 2
    if event_type.startswith("Delete"):
        return 3
    return 1
