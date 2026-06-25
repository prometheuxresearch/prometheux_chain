"""
Compute Management Module

Check availability / reachability of compute resources (machines, Databricks).

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""

from ..client.jarvispy_client import JarvisPyClient


def check_compute_availability(machine_configs=None, databricks_configs=None):
    """Check whether the given compute resources are available and reachable.

    Provide at least one of ``machine_configs`` or ``databricks_configs``.
    Returns the parsed response data. Note the backend returns a non-success
    status when a resource is unavailable, so this returns the full response
    dict rather than raising in that case.
    """
    if not machine_configs and not databricks_configs:
        raise ValueError("Provide at least one of 'machine_configs' or 'databricks_configs'")
    return JarvisPyClient.check_compute_availability(
        machine_configs=machine_configs, databricks_configs=databricks_configs,
    )
