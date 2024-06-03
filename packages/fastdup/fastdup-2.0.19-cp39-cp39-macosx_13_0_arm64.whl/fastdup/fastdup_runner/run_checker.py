import socket
from fastdup.fastdup_runner.utilities import ExplorationError, GETTING_STARTED_LINK

PORT_COLLISION_MSG = f"""
Could not launch the Visual Layer application on your machine because port 9999 is already taken.

Check if a previous .explore() is running or a different application is using it and try again.

For more information, use help(fastdup) or check our documentation {GETTING_STARTED_LINK}.
"""

def check_port_collision():
    """
    Check if 9999 port is in use
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(('localhost', 9999)) == 0:
            raise ExplorationError(PORT_COLLISION_MSG)


def check_run_problems():
    """
    Check for common problems in the run
    """
    check_port_collision()
