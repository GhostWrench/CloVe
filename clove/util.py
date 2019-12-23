"""
Shared utility functions for the clove module
"""

import os

def schema_dir():
    """Get the path to the directory where schemas are stored

    Returns
    -------
    str
        Path to the schema directory
    """
    schema_dir = os.path.normpath(os.path.join(
        os.path.dirname(__file__), "../schema"
    ))
    return schema_dir
