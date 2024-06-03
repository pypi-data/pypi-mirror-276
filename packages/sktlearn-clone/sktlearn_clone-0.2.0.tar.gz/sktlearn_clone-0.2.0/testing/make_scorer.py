# Testing/test_makescorer.py

import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
import unittest
import numpy as np
from model_selection.make_scorer import make_scorer

class TestMakeScorer(unittest.TestCase):
    pass

if __name__ == "__main__":
    unittest.main()

