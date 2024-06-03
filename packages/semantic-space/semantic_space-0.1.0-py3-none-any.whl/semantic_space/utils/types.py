"""
    Definitions for used c-types and functions related to processing
    c-types.
"""

from ctypes import (c_uint8, c_int8,
                    c_uint16, c_int16,
                    c_uint32, c_int32,
                    c_uint64, c_int64,
                    c_float, c_double,
                    Array)

numerical = c_uint8.__bases__[0]

uint8 = c_uint8
int8 = c_int8
uint16 = c_uint16
int16 = c_int16
uint32 = c_uint32
int32 = c_int32
uint64 = c_uint64
int64 = c_int64
float32 = c_float  # Probably true on most OS'.
float64 = c_double

def flatten(array):
    """
        Linearizes an n-dimensional c-type array. Analogous
        to "numpy.ndarray.ravel()" in numpy.

        Args:
             array: A c-type n-dimensional array to be flattened.

        Returns:
            A flattened 1-dimensional c-type array.
    """
    if isinstance(array, Array):
        return [element for subarray in array for element in flatten(subarray)]
    else:
        return [array]
