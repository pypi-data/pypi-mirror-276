"""
Init
"""

import os

__version__ = "0.37.9"

# allow multiple OpenMP instances
os.environ["KMP_DUPLICATE_LIB_OK"] = "True"
