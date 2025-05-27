from enum import Enum
from typing import TypeVar, Union, Sequence

# Define a type variable for numeric types
T = TypeVar('T', bound=Union[int, float])

class BisectTypeEnum(Enum):
    LEFT = "left"
    RIGHT = "right"

def binary_search(arr: Sequence[T], target: T, bisect_type: BisectTypeEnum = BisectTypeEnum.LEFT) -> int:
    """
    Find the insertion point for target in arr using binary search.
    
    Args:
        arr: A sorted list
        target: The value to find the insertion point for
        bisect_type: The type of bisection (LEFT or RIGHT)
        
    Returns:
        The index where target should be inserted to maintain sorted order
    """
    left = 0
    right = len(arr)  # Note: Python convention uses len(arr) rather than arr.length - 1
    
    while left < right:
        mid = (left + right) // 2  # Python uses // for integer division
        
        if bisect_type == BisectTypeEnum.LEFT:
            if arr[mid] >= target:
                right = mid
            else:
                left = mid + 1
        else:  # RIGHT
            if arr[mid] > target:
                right = mid
            else:
                left = mid + 1
                
    return left
