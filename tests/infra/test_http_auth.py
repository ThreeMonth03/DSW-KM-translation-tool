"""Tests for shared HTTP authentication helpers."""

from __future__ import annotations

from dsw_km_translation_tool.http_auth import bearer_authorization_header


def test_bearer_authorization_header_adds_scheme() -> None:
    """Verify bare tokens are sent as bearer tokens."""

    assert bearer_authorization_header(" secret-token ") == "Bearer secret-token"


def test_bearer_authorization_header_preserves_explicit_scheme() -> None:
    """Verify callers can pass an explicit Authorization scheme."""

    assert bearer_authorization_header("Token abc") == "Token abc"
    assert bearer_authorization_header("Bearer abc") == "Bearer abc"
