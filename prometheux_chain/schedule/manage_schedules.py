"""
Schedule Management Module

Manage concept evaluation policies (cron / data-change triggers), trigger them
manually, and view run history.

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""

from ..client.jarvispy_client import JarvisPyClient


def _check(response, action="operation"):
    """Raise on error, return data on success."""
    if response.get('status') != 'success':
        raise Exception(f"Schedule {action} failed: {response.get('message', 'Unknown error')}")
    return response.get('data')


def create_policy(ontology_id, concept_name, trigger_type="cron", trigger_config=None,
                  enabled=True):
    """Create an evaluation policy.

    For ``trigger_type='cron'`` provide ``trigger_config={'cron_expression': '...'}``.
    For ``trigger_type='data_change'`` provide
    ``trigger_config={'check_interval_minutes': <int>}``.
    """
    return _check(JarvisPyClient.create_policy(
        ontology_id=ontology_id, concept_name=concept_name, trigger_type=trigger_type,
        trigger_config=trigger_config, enabled=enabled,
    ), "create policy")


def list_policies(ontology_id, concept_name=None):
    """List evaluation policies for a project."""
    return _check(JarvisPyClient.list_policies(
        ontology_id=ontology_id, concept_name=concept_name,
    ), "list policies")


def get_policy(ontology_id, policy_id):
    """Get a single evaluation policy."""
    return _check(JarvisPyClient.get_policy(
        ontology_id=ontology_id, policy_id=policy_id,
    ), "get policy")


def update_policy(ontology_id, policy_id, trigger_config=None, enabled=None):
    """Update an evaluation policy (cron expression, enable/disable)."""
    return _check(JarvisPyClient.update_policy(
        ontology_id=ontology_id, policy_id=policy_id,
        trigger_config=trigger_config, enabled=enabled,
    ), "update policy")


def delete_policy(ontology_id, policy_id):
    """Delete an evaluation policy and its scheduled job."""
    response = JarvisPyClient.delete_policy(
        ontology_id=ontology_id, policy_id=policy_id,
    )
    if response.get('status') != 'success':
        raise Exception(f"Schedule delete policy failed: {response.get('message', 'Unknown error')}")


def trigger_policy(ontology_id, policy_id):
    """Manually trigger a scheduled concept run now."""
    return _check(JarvisPyClient.trigger_policy(
        ontology_id=ontology_id, policy_id=policy_id,
    ), "trigger policy")


def get_run_history(ontology_id, policy_id, limit=50, offset=0):
    """Retrieve execution history for an evaluation policy."""
    return _check(JarvisPyClient.get_run_history(
        ontology_id=ontology_id, policy_id=policy_id, limit=limit, offset=offset,
    ), "run history")
