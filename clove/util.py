"""
Shared utility functions for the clove module
"""

import os

def schema_dir():
    schema_dir = os.path.normpath(os.path.join(
        os.path.dirname(__file__), "../schema"
    ))
    return schema_dir