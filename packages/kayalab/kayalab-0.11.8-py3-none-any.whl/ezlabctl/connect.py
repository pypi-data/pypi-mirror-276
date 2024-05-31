from .common import fail, target_classes, target_names
from . import pve


def connect_to_target(target, host, username, password):
    """Create connection to target API

    Args:
        target (enum): pve
        host (string): API host/IP to connect
        username (str): API user, required permissions ...
        password (str): API user password

    Returns:
        class: API connection class
    """
    connection = None
    if target == target_names.pve:
        connection = pve.get_connection(host, username, password)

    else:
        fail("Unknown target")

    return connection


def select_vms(connection):
    """Returns all VMs from connection

    Args:
        connection (class<API>): connection class returned by the API connection

    Returns:
        list<class>: List of all VMs returned by API call
    """
    connection_type = connection.__class__.__name__
    if connection_type == target_classes.pve.value:
        return pve.select_vms(connection)
    else:
        fail("Unknown connection type")
    return None
