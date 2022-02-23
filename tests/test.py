
import sys
import unittest

# logging
if __name__ == "__main__":
    import logging
    logging.basicConfig(filename="test.log", level = logging.INFO)

sys.path.append(".")

# === unit tests ===
from test_dct import *
from test_flags import *
from test_interface import *
from test_shapes import *
from test_spatial import *
from test_performance import *
from test_version import *
# ==================


# run unittests
if __name__ == "__main__":
    unittest.main()
