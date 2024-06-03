"""
    NGram class for n-gram models.
"""

from ..tools import tokens
from ..utils.exceptions import *
from ..utils.types import *
from typing import Union, List
from numpy import log, exp
from struct import pack, unpack
from zlib import compress, decompress

# Will only accept ordered tokens
class NGram:
    """
        Generic class for n-gram models. Support is from 2-gram
        to 255-gram. Higher n values require higher RAM on your
        system. "n" directly defines recursion depth in some
        functions. Usage of this class may generate random kill
        signals on your Python process, because, insufficient RAM.
    """
    n: uint8
    vocab_size: int
    dtype: numerical

    def __init__(self, n, vocab_size: int, dtype: numerical = uint16):
        """
            Initialize an N-Gram model.

            Args:
                n (int): The actual n-value of the model. Methods of the
                    class support values from 2 to 255.
                vocab_size (int): Vocabulary size of your text corpus of interest.
                dtype: Data type to store "gram" values as. Any ctype is accepted.
        """
        if n < 2:
            raise ArgumentError("Support for N-Gram models start from n=2.")

        self.n = n
        self.vocab_size = vocab_size
        self.dtype = dtype

        array_type = self.dtype
        for k in range(self.n):
            array_type *= self.vocab_size

        self.core = array_type()  # Initialized and defined here

    def feed(self, tokenlist: List[Union[tokens.token16, tokens.token32]]):
        """
            Feeds the model with some text-corpus. Inner appearance count
            tensor, self.core, is updated with this method.

            Args:
                tokenlist: A list of ordered tokens.

        """
        linear = tokens.unorder(tokenlist)
        for k in range(len(linear) - self.n):
            current = k
            axis = self.core[linear[current]]
            for l in range(self.n - 2):
                current += 1
                axis = axis[linear[current]]
            axis[linear[current + 1]] += 1

    def predict(self, tokenlist: List[Union[tokens.token16, tokens.token32]], dtype: numerical = float32):
        """
            Calculates the probability that a given token-string is generated
            with the modeled n-gram system. No normalization is applied yet.

            Args:
                tokenlist: A list of ordered tokens.
                dtype: Data type in numpy's datatypes to calculate the probability with.

            Returns:
                The probability that the given string is generated with the model.
        """
        linear = tokens.unorder(tokenlist)
        p: dtype = 0
        maxima = max(self.core)
        for k in range(len(linear) - self.n):
            current = k
            axis = self.core[linear[current]]
            for l in range(self.n - 2):
                current += 1
                axis = axis[linear[current]]
            p += log(axis[linear[current + 1]] / maxima)
        return exp(p)

    def save(self, destfile):
        """
            Save the model as a .ngram file.

            Args:
                destfile (str): Path to the destination file, with
                    extension .ngram.
        """
        with open(destfile, "wb") as file:
            file.write(pack("B", self.n) + pack("I", self.vocab_size))

            # I wish I had switch
            save_type: str
            if self.dtype == int8:
                file.write(pack("B", 0))
                save_type = "b"
            elif self.dtype == uint8:
                file.write(pack("B", 1))
                save_type = "B"
            elif self.dtype == int16:
                file.write(pack("B", 2))
                save_type = "h"
            elif self.dtype == uint16:
                file.write(pack("B", 3))
                save_type = "H"
            elif self.dtype == int32:
                file.write(pack("B", 4))
                save_type = "i"
            elif self.dtype == uint32:
                file.write(pack("B", 5))
                save_type = "I"
            elif self.dtype == int64:
                file.write(pack("B", 6))
                save_type = "q"
            elif self.dtype == uint64:
                file.write(pack("B", 7))
                save_type = "Q"
            elif self.dtype == float32:
                file.write(pack("B", 8))
                save_type = "f"
            elif self.dtype == float64:
                file.write(pack("B", 9))
                save_type = "d"
            else:
                raise FileCorruptedError(f"File building corrupted, invalid type entry.")

            data = flatten(self.core)
            data = compress(pack(f"{len(data)}{save_type}", data))
            file.write(data)

    def __reshape(self, array, shape):
        if len(shape) == 1:
            return (self.dtype * shape[0])(*array)

        sub_shape = shape[1:]
        size = shape[0]
        step = len(array) // size
        nested_array_type = (self.dtype * size) * (len(array) // size)

        nested_array = nested_array_type()

        for i in range(size):
            sub_array = self.__reshape(array[i * step: (i + 1) * step], sub_shape)
            nested_array[i] = sub_array

        return nested_array

    @staticmethod
    def load(path: str):
        """
            Load a model from a .ngram file.

            Args:
                path (str): Path to the model file.

            Returns:
                The loaded model as an NGram object.
        """
        with open(path, "rb") as file:
            n = unpack("B", file.read(1))
            vocab_size = unpack("I", file.read(4))
            identifier = unpack("B", file.read(1))

            save_type: str
            dtype: numerical
            if identifier == 0:
                save_type = "b"
                dtype = int8
            elif identifier == 1:
                save_type = "B"
                dtype = uint8
            elif identifier == 2:
                save_type = "h"
                dtype = int16
            elif identifier == 3:
                save_type = "H"
                dtype = uint16
            elif identifier == 4:
                save_type = "i"
                dtype = int32
            elif identifier == 5:
                save_type = "I"
                dtype = uint32
            elif identifier == 6:
                save_type = "q"
                dtype = int64
            elif identifier == 7:
                save_type = "Q"
                dtype = uint64
            elif identifier == 8:
                save_type = "f"
                dtype = float32
            elif identifier == 9:
                save_type = "d"
                dtype = float64

            data = decompress(file.read())

        model = NGram(n, vocab_size, dtype)
        model.core = model.__reshape(data, [vocab_size for k in range(n)])
        return model







