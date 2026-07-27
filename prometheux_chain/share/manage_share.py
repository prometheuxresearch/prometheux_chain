"""
Project Sharing Management Module

Sharer-side (create / revoke / update-role / list) and recipient-side
(inbox / accept / leave / sync) project sharing.

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""

from ..client.jarvispy_client import JarvisPyClient


def _check(response, action="operation"):
    """Raise on error, return data on success."""
    if response.get('status') != 'success':
        raise Exception(f"Share {action} failed: {response.get('message', 'Unknown error')}")
    return response.get('data')


def create_share(ontology_id, recipient, share_role, expires_in_minutes=None):
    """Share a project with another user.

    ``recipient`` is a dict identifying the target by ``sub``, ``email``, or
    ``username`` + ``organization``. ``share_role`` is 'viewer' or 'editor'.
    """
    return _check(JarvisPyClient.create_share(
        ontology_id=ontology_id, recipient=recipient, share_role=share_role,
        expires_in_minutes=expires_in_minutes,
    ), "create")


def revoke_share(share_id=None, ontology_id=None, recipient_sub=None):
    """Revoke a share, by ``share_id`` or by ``project_id`` + ``recipient_sub``."""
    return _check(JarvisPyClient.revoke_share(
        share_id=share_id, ontology_id=ontology_id, recipient_sub=recipient_sub,
    ), "revoke")


def update_share_role(share_id, share_role):
    """Change an existing share's role (viewer <-> editor)."""
    return _check(JarvisPyClient.update_share_role(
        share_id=share_id, share_role=share_role,
    ), "update role")


def list_shares(ontology_id=None):
    """List shares created by the caller (optionally filtered by project)."""
    return _check(JarvisPyClient.list_shares(ontology_id=ontology_id), "list")


def list_inbox():
    """List shares visible to the caller as a recipient (pending + accepted)."""
    return _check(JarvisPyClient.list_inbox(), "inbox")


def accept_share(share_id):
    """Accept a pending share and vault its scoped token locally."""
    return _check(JarvisPyClient.accept_share(share_id), "accept")


def leave_share(share_id):
    """Detach the recipient from an accepted (or pending) share."""
    return _check(JarvisPyClient.leave_share(share_id), "leave")


def sync_inbox():
    """Reconcile the recipient's local share vault against the source of truth."""
    return _check(JarvisPyClient.sync_inbox(), "sync")
