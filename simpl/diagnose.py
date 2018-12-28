# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 21:03:22 2017

Stolen from jasper

@author: mb
"""
import sys
import socket
import logging
if sys.version_info < (3, 3):
    from distutils.spawn import find_executable
else:
    from shutil import which as find_executable


def check_network_connection(server="www.google.com"):
    """
    Checks if jasper can connect a network server.
    Arguments:
        server -- (optional) the server to connect with (Default:
                  "www.google.com")
    Returns:
        True or False
    """
    logger = logging.getLogger(__name__)
    logger.debug("Checking network connection to server '%s'...", server)
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(server)
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection((host, 80), 2)
    except Exception:
        logger.debug("Network connection not working")
        return False
    else:
        logger.debug("Network connection working")
        return True


def check_executable(executable):
    """
    Checks if an executable exists in $PATH.
    Arguments:
        executable -- the name of the executable (e.g. "echo")
    Returns:
        True or False
    """
    logger = logging.getLogger(__name__)
    logger.debug("Checking executable '%s'...", executable)
    executable_path = find_executable(executable)
    found = executable_path is not None
    if found:
        logger.debug("Executable '%s' found: '%s'", executable,
                     executable_path)
    else:
        logger.debug("Executable '%s' not found", executable)
    return found
