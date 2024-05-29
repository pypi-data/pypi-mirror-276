"""Implements several machine learning algorithms based on FCA.

Currently, this version of the library only implements the outlier detection
algorithms introduced
`here <https://www.sciencedirect.com/science/article/pii/S0167923624000290>`_.
"""


# start delvewheel patch
def _delvewheel_patch_1_6_0():
    import os
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'mlconcepts.libs'))
    if os.path.isdir(libs_dir):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_6_0()
del _delvewheel_patch_1_6_0
# end delvewheel patch

from .SODModel import SODModel # noqa: F401
from .UODModel import UODModel # noqa: F401
from mlconcepts.data import load # noqa: F401