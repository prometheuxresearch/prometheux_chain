"""
Auth Management Module

Issue and revoke JarvisPy API tokens (``pmtx_token``).

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""

from ..client.jarvispy_client import JarvisPyClient


def _check(response, action="operation"):
    """Raise on error, return data on success."""
    if response.get('status') != 'success':
        raise Exception(f"Auth {action} failed: {response.get('message', 'Unknown error')}")
    return response.get('data')


def issue_token(name=None, expires_in_minutes=None):
    """Issue a new API token. The raw JWT is returned exactly once.

    ``expires_in_minutes`` of None (or <= 0) issues a non-expiring token.
    """
    return _check(JarvisPyClient.issue_token(
        name=name, expires_in_minutes=expires_in_minutes,
    ), "issue token")


def list_tokens():
    """List the caller's active API tokens (metadata only, no raw JWTs)."""
    return _check(JarvisPyClient.list_tokens(), "list tokens")


def revoke_token():
    """Revoke the caller's current Bearer token (logout)."""
    return _check(JarvisPyClient.revoke_token(), "revoke token")


def revoke_specific_token(jti):
    """Revoke a specific token by its ``jti``."""
    return _check(JarvisPyClient.revoke_specific_token(jti), "revoke token")


def revoke_all_tokens():
    """Revoke every token belonging to the caller (logout everywhere)."""
    return _check(JarvisPyClient.revoke_all_tokens(), "revoke all tokens")
