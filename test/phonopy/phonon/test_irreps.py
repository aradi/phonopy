import unittest
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import sys
import numpy as np
from phonopy import Phonopy
from phonopy.interface.vasp import read_vasp
from phonopy.file_IO import parse_FORCE_SETS
import os
data_dir=os.path.dirname(os.path.abspath(__file__))

chars_Pc = """ 1.  0. -1.  0.
 1.  0.  1.  0.
 1.  0.  1.  0.
 1.  0.  1.  0.
 1.  0. -1.  0.
 1.  0. -1.  0.
 1.  0. -1.  0.
 1.  0.  1.  0.
 1.  0. -1.  0.
 1.  0.  1.  0.
 1.  0.  1.  0.
 1.  0. -1.  0.
 1.  0.  1.  0.
 1.  0. -1.  0.
 1.  0. -1.  0.
 1.  0.  1.  0.
 1.  0. -1.  0.
 1.  0.  1.  0.
 1.  0. -1.  0.
 1.  0.  1.  0.
 1.  0. -1.  0.
 1.  0.  1.  0.
 1.  0.  1.  0.
 1.  0. -1.  0.
 1.  0.  1.  0.
 1.  0. -1.  0.
 1.  0.  1.  0.
 1.  0. -1.  0.
 1.  0.  1.  0.
 1.  0.  1.  0.
 1.  0. -1.  0.
 1.  0.  1.  0.
 1.  0. -1.  0.
 1.  0. -1.  0.
 1.  0.  1.  0.
 1.  0. -1.  0.
 1.  0.  1.  0.
 1.  0. -1.  0.
 1.  0.  1.  0.
 1.  0. -1.  0.
 1.  0.  1.  0.
 1.  0.  1.  0.
 1.  0. -1.  0.
 1.  0.  1.  0.
 1.  0. -1.  0.
 1.  0. -1.  0.
 1.  0.  1.  0.
 1.  0. -1.  0."""

chars_P222_1 = """ 1.  0.  1.  0. -1.  0. -1.  0.
 1.  0. -1.  0. -1.  0.  1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0. -1.  0. -1.  0.
 1.  0.  1.  0. -1.  0. -1.  0.
 1.  0. -1.  0. -1.  0.  1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0. -1.  0. -1.  0.
 1.  0.  1.  0. -1.  0. -1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0.  1.  0. -1.  0. -1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0. -1.  0. -1.  0.
 1.  0.  1.  0. -1.  0. -1.  0.
 1.  0. -1.  0. -1.  0.  1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0. -1.  0. -1.  0.
 1.  0. -1.  0. -1.  0.  1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0. -1.  0. -1.  0.  1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0. -1.  0. -1.  0.  1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0. -1.  0. -1.  0.
 1.  0.  1.  0. -1.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0. -1.  0. -1.  0.  1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0. -1.  0. -1.  0.  1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0.  1.  0. -1.  0. -1.  0.
 1.  0. -1.  0. -1.  0.  1.  0.
 1.  0.  1.  0. -1.  0. -1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0. -1.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0. -1.  0. -1.  0.  1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0. -1.  0. -1.  0.
 1.  0. -1.  0. -1.  0.  1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0.  1.  0. -1.  0. -1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0. -1.  0. -1.  0.  1.  0.
 1.  0. -1.  0. -1.  0.  1.  0.
 1.  0.  1.  0. -1.  0. -1.  0.
 1.  0.  1.  0. -1.  0. -1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0. -1.  0. -1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0. -1.  0. -1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0. -1.  0. -1.  0.  1.  0.
 1.  0. -1.  0. -1.  0.  1.  0.
 1.  0. -1.  0. -1.  0.  1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0. -1.  0. -1.  0.
 1.  0.  1.  0. -1.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0. -1.  0. -1.  0.  1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0. -1.  0. -1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0. -1.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0. -1.  0. -1.  0.  1.  0.
 1.  0. -1.  0. -1.  0.  1.  0.
 1.  0. -1.  0. -1.  0.  1.  0.
 1.  0.  1.  0.  1.  0.  1.  0."""

chars_Amm2 = """1. 0. -1. 0. -1. 0.  1. 0.
1. 0. -1. 0.  1. 0. -1. 0.
1. 0.  1. 0.  1. 0.  1. 0.
1. 0. -1. 0. -1. 0.  1. 0.
1. 0. -1. 0.  1. 0. -1. 0.
1. 0.  1. 0.  1. 0.  1. 0.
1. 0. -1. 0. -1. 0.  1. 0.
1. 0. -1. 0.  1. 0. -1. 0.
1. 0. -1. 0.  1. 0. -1. 0.
1. 0.  1. 0. -1. 0. -1. 0.
1. 0.  1. 0.  1. 0.  1. 0.
1. 0.  1. 0.  1. 0.  1. 0.
1. 0. -1. 0. -1. 0.  1. 0.
1. 0. -1. 0.  1. 0. -1. 0.
1. 0.  1. 0.  1. 0.  1. 0."""

chars_P4_1 = """ 1.  0.  1.  0.  1.  0.  1.  0.
 2.  0.  0.  0. -2.  0.  0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 2.  0. -0.  0. -2.  0.  0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 2.  0. -0.  0. -2.  0. -0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 2.  0. -0.  0. -2.  0.  0.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 2.  0. -0.  0. -2.  0. -0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 2.  0. -0.  0. -2.  0.  0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 2.  0.  0.  0. -2.  0. -0.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 2.  0.  0.  0. -2.  0.  0.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 2.  0.  0.  0. -2.  0.  0.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 2.  0. -0.  0. -2.  0.  0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 2.  0.  0.  0. -2.  0.  0.  0.
 2.  0. -0.  0. -2.  0. -0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 2.  0. -0.  0. -2.  0.  0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 2.  0. -0.  0. -2.  0. -0.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 2.  0. -0.  0. -2.  0.  0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 2.  0.  0.  0. -2.  0.  0.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 2.  0.  0.  0. -2.  0.  0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 2.  0. -0.  0. -2.  0. -0.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 2.  0.  0.  0. -2.  0.  0.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 2.  0.  0.  0. -2.  0.  0.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 2.  0.  0.  0. -2.  0.  0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 2.  0. -0.  0. -2.  0. -0.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 2.  0. -0.  0. -2.  0.  0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 2.  0.  0.  0. -2.  0.  0.  0."""

chars_Pbar4 = """ 1.  0. -1.  0.  1.  0. -1.  0.
 2.  0. -0.  0. -2.  0. -0.  0.
 2.  0. -0.  0. -2.  0. -0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 2.  0. -0.  0. -2.  0.  0.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 2.  0. -0.  0. -2.  0.  0.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 2.  0.  0.  0. -2.  0. -0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 2.  0.  0.  0. -2.  0. -0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 2.  0.  0.  0. -2.  0. -0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 2.  0.  0.  0. -2.  0. -0.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 2.  0.  0.  0. -2.  0. -0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 2.  0.  0.  0. -2.  0.  0.  0.
 2.  0.  0.  0. -2.  0.  0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 2.  0. -0.  0. -2.  0. -0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 2.  0. -0.  0. -2.  0. -0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 2.  0.  0.  0. -2.  0.  0.  0.
 2.  0. -0.  0. -2.  0. -0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 2.  0. -0.  0. -2.  0.  0.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 2.  0.  0.  0. -2.  0.  0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 2.  0.  0.  0. -2.  0.  0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.
 2.  0. -0.  0. -2.  0.  0.  0.
 1.  0. -1.  0.  1.  0. -1.  0."""

chars_I4_1a = """ 1.  0.  1.  0.  1.  0.  1.  0. -1.  0. -1.  0. -1.  0. -1.  0.
 2.  0. -0.  0. -2.  0.  0.  0. -2.  0.  0.  0.  2.  0. -0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0.
 2.  0.  0.  0. -2.  0. -0.  0.  2.  0.  0.  0. -2.  0. -0.  0.
 1.  0.  1.  0.  1.  0.  1.  0. -1.  0. -1.  0. -1.  0. -1.  0.
 2.  0.  0.  0. -2.  0. -0.  0. -2.  0. -0.  0.  2.  0.  0.  0.
 2.  0.  0.  0. -2.  0. -0.  0.  2.  0.  0.  0. -2.  0. -0.  0.
 1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.
 1.  0.  1.  0.  1.  0.  1.  0. -1.  0. -1.  0. -1.  0. -1.  0.
 2.  0. -0.  0. -2.  0.  0.  0. -2.  0.  0.  0.  2.  0. -0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0.
 1.  0. -1.  0.  1.  0. -1.  0. -1.  0.  1.  0. -1.  0.  1.  0.
 2.  0. -0.  0. -2.  0. -0.  0.  2.  0.  0.  0. -2.  0. -0.  0.
 1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0.
 2.  0. -0.  0. -2.  0.  0.  0. -2.  0.  0.  0.  2.  0. -0.  0.
 2.  0.  0.  0. -2.  0. -0.  0.  2.  0.  0.  0. -2.  0. -0.  0.
 1.  0.  1.  0.  1.  0.  1.  0. -1.  0. -1.  0. -1.  0. -1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0.
 1.  0. -1.  0.  1.  0. -1.  0. -1.  0.  1.  0. -1.  0.  1.  0.
 2.  0.  0.  0. -2.  0.  0.  0. -2.  0.  0.  0.  2.  0. -0.  0.
 1.  0.  1.  0.  1.  0.  1.  0. -1.  0. -1.  0. -1.  0. -1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0.
 1.  0. -1.  0.  1.  0. -1.  0. -1.  0.  1.  0. -1.  0.  1.  0.
 2.  0. -0.  0. -2.  0.  0.  0.  2.  0. -0.  0. -2.  0.  0.  0.
 1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0."""

chars_P4mm = """ 2.  0.  0.  0. -2.  0.  0.  0. -0.  0.  0.  0.  0.  0. -0.  0.
 1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.
 2.  0.  0.  0. -2.  0.  0.  0.  0.  0. -0.  0. -0.  0.  0.  0.
 1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.
 2.  0.  0.  0. -2.  0.  0.  0.  0.  0. -0.  0. -0.  0.  0.  0.
 2.  0.  0.  0. -2.  0.  0.  0. -0.  0. -0.  0.  0.  0.  0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.
 2.  0.  0.  0. -2.  0.  0.  0.  0.  0. -0.  0. -0.  0.  0.  0.
 1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0."""

chars_Pbar42_1m = """ 1.  0. -1.  0.  1.  0. -1.  0. -1.  0.  1.  0. -1.  0.  1.  0.
 2.  0.  0.  0. -2.  0.  0.  0.  0.  0.  0.  0. -0.  0. -0.  0.
 2.  0. -0.  0. -2.  0.  0.  0.  0.  0.  0.  0. -0.  0. -0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.
 2.  0. -0.  0. -2.  0.  0.  0. -0.  0. -0.  0.  0.  0.  0.  0.
 1.  0. -1.  0.  1.  0. -1.  0. -1.  0.  1.  0. -1.  0.  1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0.
 2.  0.  0.  0. -2.  0. -0.  0.  0.  0. -0.  0.  0.  0.  0.  0.
 1.  0.  1.  0.  1.  0.  1.  0. -1.  0. -1.  0. -1.  0. -1.  0.
 2.  0.  0.  0. -2.  0. -0.  0. -0.  0. -0.  0.  0.  0.  0.  0.
 1.  0. -1.  0.  1.  0. -1.  0. -1.  0.  1.  0. -1.  0.  1.  0.
 2.  0.  0.  0. -2.  0.  0.  0.  0.  0.  0.  0. -0.  0. -0.  0.
 1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.
 2.  0.  0.  0. -2.  0.  0.  0. -0.  0.  0.  0.  0.  0. -0.  0.
 1.  0. -1.  0.  1.  0. -1.  0. -1.  0.  1.  0. -1.  0.  1.  0."""

chars_Pbar3m1 = """ 2.  0. -2.  0. -1.  0.  1.  0. -1.  0.  1.  0. -0.  0.  0.  0.  0.  0. -0.  0.  0.  0. -0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0.  1.  0.
 2.  0.  2.  0. -1.  0. -1.  0. -1.  0. -1.  0. -0.  0. -0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
 2.  0. -2.  0. -1.  0.  1.  0. -1.  0.  1.  0.  0.  0. -0.  0.  0.  0. -0.  0. -0.  0.  0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0.  1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.
 2.  0. -2.  0. -1.  0.  1.  0. -1.  0.  1.  0.  0.  0. -0.  0.  0.  0. -0.  0. -0.  0.  0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0.  1.  0.
 2.  0.  2.  0. -1.  0. -1.  0. -1.  0. -1.  0. -0.  0. -0.  0. -0.  0. -0.  0.  0.  0.  0.  0."""

chars_Pbar6m2 = """ 2.  0. -1.  0. -1.  0.  2.  0. -1.  0. -1.  0.  0.  0.  0.  0. -0.  0.  0.  0.  0.  0. -0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0.  1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0. -1.  0. -1.  0. -1.  0. -1.  0. -1.  0. -1.  0.
 2.  0. -1.  0. -1.  0.  2.  0. -1.  0. -1.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.
 2.  0.  1.  0. -1.  0. -2.  0. -1.  0.  1.  0. -0.  0. -0.  0. -0.  0.  0.  0.  0.  0.  0.  0.
 2.  0. -1.  0. -1.  0.  2.  0. -1.  0. -1.  0.  0.  0. -0.  0. -0.  0.  0.  0. -0.  0. -0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0.  1.  0.
 2.  0. -1.  0. -1.  0.  2.  0. -1.  0. -1.  0.  0.  0.  0.  0. -0.  0.  0.  0.  0.  0. -0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0.  1.  0.
 1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0.  1.  0.
 2.  0. -1.  0. -1.  0.  2.  0. -1.  0. -1.  0. -0.  0. -0.  0.  0.  0. -0.  0. -0.  0.  0.  0.
 1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -1.  0.  1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.
 2.  0. -1.  0. -1.  0.  2.  0. -1.  0. -1.  0. -0.  0. -0.  0.  0.  0. -0.  0. -0.  0.  0.  0."""

chars_Pbar43m = """ 3.  0. -1.  0. -1.  0. -1.  0. -1.  0.  1.  0. -1.  0.  1.  0.  0.  0.  1.  0. -0.  0. -1.  0. -0.  0.  1.  0.  0.  0. -1.  0.  0.  0. -1.  0.  0.  0.  1.  0. -0.  0.  1.  0. -0.  0. -1.  0.
 3.  0.  1.  0. -1.  0.  1.  0. -1.  0. -1.  0. -1.  0. -1.  0.  0.  0. -1.  0.  0.  0.  1.  0.  0.  0. -1.  0. -0.  0.  1.  0. -0.  0.  1.  0. -0.  0. -1.  0.  0.  0. -1.  0.  0.  0.  1.  0.
 3.  0. -1.  0. -1.  0. -1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -0.  0.  1.  0.  0.  0. -1.  0.  0.  0.  1.  0. -0.  0. -1.  0.  0.  0. -1.  0. -0.  0.  1.  0.  0.  0.  1.  0.  0.  0. -1.  0.
 2.  0. -0.  0.  2.  0. -0.  0.  2.  0. -0.  0.  2.  0. -0.  0. -1.  0.  0.  0. -1.  0.  0.  0. -1.  0.  0.  0. -1.  0.  0.  0. -1.  0. -0.  0. -1.  0. -0.  0. -1.  0. -0.  0. -1.  0. -0.  0.
 3.  0. -1.  0. -1.  0. -1.  0. -1.  0.  1.  0. -1.  0.  1.  0.  0.  0.  1.  0. -0.  0. -1.  0. -0.  0.  1.  0.  0.  0. -1.  0.  0.  0. -1.  0.  0.  0.  1.  0. -0.  0.  1.  0. -0.  0. -1.  0.
 3.  0.  1.  0. -1.  0.  1.  0. -1.  0. -1.  0. -1.  0. -1.  0.  0.  0. -1.  0.  0.  0.  1.  0.  0.  0. -1.  0. -0.  0.  1.  0.  0.  0.  1.  0. -0.  0. -1.  0.  0.  0. -1.  0.  0.  0.  1.  0.
 3.  0. -1.  0. -1.  0. -1.  0. -1.  0.  1.  0. -1.  0.  1.  0.  0.  0.  1.  0. -0.  0. -1.  0. -0.  0.  1.  0.  0.  0. -1.  0.  0.  0. -1.  0.  0.  0.  1.  0. -0.  0.  1.  0. -0.  0. -1.  0.
 1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.  1.  0.
 3.  0. -1.  0. -1.  0. -1.  0. -1.  0.  1.  0. -1.  0.  1.  0. -0.  0.  1.  0.  0.  0. -1.  0.  0.  0.  1.  0. -0.  0. -1.  0. -0.  0. -1.  0. -0.  0.  1.  0.  0.  0.  1.  0.  0.  0. -1.  0."""

class TestIrreps(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_pt04_Pc(self):
        data = np.loadtxt(StringIO(chars_Pc)).view(dtype='complex128')
        phonon = self._get_phonon("Pc", 
                                  [2, 2, 2],
                                  np.eye(3))
        phonon.set_irreps([0, 0, 0])
        chars = phonon.get_irreps().get_characters()
        np.testing.assert_allclose(chars,data,atol=1e-5)

    def test_pt06_P222_1(self):
        data = np.loadtxt(StringIO(chars_P222_1)).view(dtype='complex128')
        phonon = self._get_phonon("P222_1", 
                                  [2, 2, 1],
                                  np.eye(3))
        phonon.set_irreps([0, 0, 0])
        chars = phonon.get_irreps().get_characters()
        np.testing.assert_allclose(chars,data,atol=1e-5)

    def test_pt07_Amm2(self):
        data = np.loadtxt(StringIO(chars_Amm2)).view(dtype='complex128')
        phonon = self._get_phonon("Amm2", 
                                  [3, 2, 2],
                                  [[1, 0, 0],
                                   [0, 0.5, -0.5],
                                   [0, 0.5, 0.5]])
        phonon.set_irreps([0, 0, 0])
        chars = phonon.get_irreps().get_characters()
        np.testing.assert_allclose(chars,data,atol=1e-5)

    def test_pt09_P4_1(self):
        data = np.loadtxt(StringIO(chars_P4_1)).view(dtype='complex128')
        phonon = self._get_phonon("P4_1", 
                                  [2, 2, 1],
                                  np.eye(3))
        phonon.set_irreps([0, 0, 0])
        chars = phonon.get_irreps().get_characters()
        np.testing.assert_allclose(chars,data,atol=1e-5)

    def test_pt10_Pbar4(self):
        data = np.loadtxt(StringIO(chars_Pbar4)).view(dtype='complex128')
        phonon = self._get_phonon("P-4", 
                                  [1, 1, 2],
                                  np.eye(3))
        phonon.set_irreps([0, 0, 0])
        chars = phonon.get_irreps().get_characters()
        np.testing.assert_allclose(chars,data,atol=1e-5)

    def test_pt11_I4_1a(self):
        data = np.loadtxt(StringIO(chars_I4_1a)).view(dtype='complex128')
        phonon = self._get_phonon("I4_1a", 
                                  [2, 2, 1],
                                  np.array([[-1, 1, 1],
                                            [1, -1, 1],
                                            [1, 1, -1]]) * 0.5)
        phonon.set_irreps([0, 0, 0])
        chars = phonon.get_irreps().get_characters()
        np.testing.assert_allclose(chars,data,atol=1e-5)

    def test_pt13_P4mm(self):
        data = np.loadtxt(StringIO(chars_P4mm)).view(dtype='complex128')
        phonon = self._get_phonon("P4mm", 
                                  [3, 3, 2],
                                  np.eye(3))
        phonon.set_irreps([0, 0, 0])
        chars = phonon.get_irreps().get_characters()
        np.testing.assert_allclose(chars,data,atol=1e-5)

    def test_pt14_Pbar42_1m(self):
        data = np.loadtxt(StringIO(chars_Pbar42_1m)).view(dtype='complex128')
        phonon = self._get_phonon("P-42_1m", 
                                  [2, 2, 3],
                                  np.eye(3))
        phonon.set_irreps([0, 0, 0])
        chars = phonon.get_irreps().get_characters()
        np.testing.assert_allclose(chars,data,atol=1e-5)

    def test_pt20_Pbar3m1(self):
        data = np.loadtxt(StringIO(chars_Pbar3m1)).view(dtype='complex128')
        phonon = self._get_phonon("P-3m1", 
                                  [3, 3, 2],
                                  np.eye(3))
        phonon.set_irreps([0, 0, 0])
        chars = phonon.get_irreps().get_characters()
        np.testing.assert_allclose(chars,data,atol=1e-5)

    def test_pt26_Pbar6m2(self):
        data = np.loadtxt(StringIO(chars_Pbar6m2)).view(dtype='complex128')
        phonon = self._get_phonon("P-6m2", 
                                  [2, 2, 3],
                                  np.eye(3))
        phonon.set_irreps([0, 0, 0])
        chars = phonon.get_irreps().get_characters()
        np.testing.assert_allclose(chars,data,atol=1e-5)

    def test_pt31_Pbar43m(self):
        data = np.loadtxt(StringIO(chars_Pbar43m)).view(dtype='complex128')
        phonon = self._get_phonon("P-43m", 
                                  [2, 2, 2],
                                  np.eye(3))
        phonon.set_irreps([0, 0, 0])
        chars = phonon.get_irreps().get_characters()
        np.testing.assert_allclose(chars,data,atol=1e-5)

    def _get_phonon(self, spgtype, dim, pmat):
        cell = read_vasp(os.path.join(data_dir,"POSCAR_%s" % spgtype))
        phonon = Phonopy(cell,
                         np.diag(dim),
                         primitive_matrix=pmat)
        force_sets = parse_FORCE_SETS(filename=os.path.join(data_dir,"FORCE_SETS_%s" % spgtype))
        phonon.set_displacement_dataset(force_sets)
        phonon.produce_force_constants()
        print(phonon.get_symmetry().get_pointgroup())
        return phonon

    def _show_chars(self, chars):
        for line in chars:
            line_str = str(line.view(dtype='double').round(decimals=1))
            print(line_str.replace("[", '').replace("]", ''))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIrreps)
    unittest.TextTestRunner(verbosity=2).run(suite)