import sys

sys.path.append("..app")
from app.services.binary_search import binary_search
from app.services.binary_search.binary_search import BisectTypeEnum
import pytest


class Testbinary_search:
    """Test cases for the binary_search utility function"""

    def test_binary_search_left_regular(self):
        """Should return correct index with binary_search left on regular array"""
        arr = [1, 2, 3, 4, 5]
        target = 3.5
        res = binary_search.binary_search(arr, target, BisectTypeEnum.LEFT)
        assert res == 3

    def test_binary_search_left_with_duplicates(self):
        """Should return correct index with binary_search left on array with duplicates"""
        arr = [1, 2, 2, 3, 3, 4, 5]
        target = 3
        res = binary_search.binary_search(arr, target, BisectTypeEnum.LEFT)
        assert res == 3

    def test_binary_search_right_regular(self):
        """Should return correct index with binary_search right on regular array"""
        arr = [1, 2, 3, 4, 5]
        target = 3.5
        res = binary_search.binary_search(arr, target, BisectTypeEnum.RIGHT)
        assert res == 3

    def test_binary_search_right_with_duplicates(self):
        """Should return correct index with binary_search right on array with duplicates"""
        arr = [1, 2, 2, 3, 3, 4, 5]
        target = 3
        res = binary_search.binary_search(arr, target, BisectTypeEnum.RIGHT)
        assert res == 5
