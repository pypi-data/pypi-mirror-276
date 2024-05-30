from __future__ import annotations
from rdkit import Chem
import rdkit.Chem.MolStandardize.standardize
from rdkit.Chem.MolStandardize.standardize import Standardizer
import unittest as unittest
__all__ = ['Chem', 'FakeStandardizer', 'Standardizer', 'TestCase', 'unittest']
class FakeStandardizer(rdkit.Chem.MolStandardize.standardize.Standardizer):
    def normalize(self):
        ...
class TestCase(unittest.case.TestCase):
    def testPreserveProps(self):
        ...
