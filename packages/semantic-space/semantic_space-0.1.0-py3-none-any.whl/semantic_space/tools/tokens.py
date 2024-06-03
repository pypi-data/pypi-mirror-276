"""
    Datatypes and functions to process any sort of tokens.
"""

from struct import pack, unpack
from zlib import compress, decompress
from dataclasses import dataclass
from typing import Union, List, Tuple
from os.path import abspath
import numpy as np
from ..utils.exceptions import *
from ..utils.types import *

@dataclass
class utoken16:
    """
        Unordered token type of size 16-bit. Holds the information
        for the amount that the token appears in a given text, and
        the id of the token.
    """
    count: uint16
    id: uint16

    def __add__(self, arg: int):
        self.count += arg

    def __radd__(self, arg: int):
        self.count += arg

    def __sub__(self, arg: int):
        self.count -= arg

    def __rsub__(self, arg: int):
        self.count -= arg

@dataclass
class utoken32:
    """
        Unordered token type of size 32-bit. Holds the information
        for the amount that the token appears in a given text, and
        the id of the token.
    """
    count: uint32
    id: uint32

    def __add__(self, arg: int):
        self.count += arg

    def __radd__(self, arg: int):
        self.count += arg

    def __sub__(self, arg: int):
        self.count -= arg

    def __rsub__(self, arg: int):
        self.count -= arg

class token16:  # 42 bytes in total
    """
        Ordered token type of size 16-bit. This is a data chunk that
        is 42 bytes long. First 40 bytes are 16-bit unsigned integers
        that each hold the order of a single appearance of the token
        in a given text. Rest 2 bytes are a 16-bit unsigned integer
        that holds the id of the token.

        If the first position of the order array is 0, it means that
        the given token appears at the position 0. Any 0 anywhere else
        does not carry any information. A formatter must recognize this
        and stop at 0 while index is not 0.

    """
    positions: uint16 * 20
    id: uint16

    def __init__(self, id: int):
        self.id = id
        self.positions = (uint16 * 20)()

    def __getitem__(self, item: int):
        return self.positions[item]

    def __setitem__(self, key: int, value: int):
        self.positions[key] = uint16(value)

class token32:  # 84 bytes in total
    """
        Ordered token type of size 32-bit. This is a data chunk that
        is 84 bytes long. First 80 bytes are 32-bit unsigned integers
        that each hold the order of a single appearance of the token
        in a given text. Rest 4 bytes are a 32-bit unsigned integer
        that holds the id of the token.

        If the first position of the order array is 0, it means that
        the given token appears at the position 0. Any 0 anywhere else
        does not carry any information. A formatter must recognize this
        and stop at 0 while index is not 0.

    """
    positions: uint32 * 20
    id: uint32

    def __init__(self, id: int):
        self.id = id
        self.positions = (uint32 * 20)()

    def __getitem__(self, item: int):
        return self.positions[item]

    def __setitem__(self, key: int, value: int):
        self.positions[key] = uint32(value)

TOKEN = Union[utoken16, utoken32, token16, token32]

def tokenify(array: Union[List[int], Tuple[int]], ordered: bool = False, size: int = 16) -> List[TOKEN]:
    """
        Creates a token-array from the given tokenid sequence. Uses token types that are
        defined in this library.

        Args:
            array: A list/tuple of integers. Integers are token ids from any tokenizer.
            ordered (bool): The choice for ordered or unordered token types to use.
            size (int): The choice to use 16-bit or 32-bit implementations.

        Returns:
            A token-array consisting of utoken16/utoken32/token16/token32 types.
    """
    if size != 16 and size != 32:
        raise ArgumentError("size argument must be either 16 or 32")

    if not ordered and size == 16:
        id_token_match = {}

        for ID in array:
            if ID in id_token_match:
                id_token_match[ID].count += 1
            else:
                id_token_match[ID] = utoken16(1, ID)
        return list(id_token_match.values())

    if not ordered and size == 32:
        id_token_match = {}

        for ID in array:
            if ID in id_token_match:
                id_token_match[ID].count += 1
            else:
                id_token_match[ID] = utoken32(1, ID)
        return list(id_token_match.values())

    if ordered and size == 16:
        id_token_match = {}
        id_index_match = {}

        for i, ID in enumerate(array):
            if ID in id_token_match:
                if id_index_match[ID] == 20:
                    token = token16(ID)
                    token[0] = i  # Orders start from 0
                    id_token_match[ID].append(token)
                    id_index_match[ID] = 1
                else:
                    id_token_match[ID][-1][id_index_match[ID]] = i
                    id_index_match[ID] += 1
            else:
                token = token16(ID)
                token[0] = i
                id_index_match[ID] = 1
                id_token_match[ID] = [token]

        all_tokens = []
        for token_list in id_token_match.values():
            for element in token_list:
                all_tokens.append(element)
        return all_tokens

    if ordered and size == 32:
        id_token_match = {}
        id_index_match = {}

        for i, ID in enumerate(array):
            if ID in id_token_match:
                if id_index_match[ID] == 20:
                    token = token32(ID)
                    token[0] = i
                    id_token_match[ID].append(token)
                    id_index_match[ID] = 1
                else:
                    id_token_match[ID][-1][id_index_match[ID]] = i
                    id_index_match[ID] += 1
            else:
                token = token32(ID)
                token[0] = i
                id_index_match[ID] = 1
                id_token_match[ID] = [token]

        all_tokens = []
        for token_list in id_token_match.values():
            for element in token_list:
                all_tokens.append(element)
        return all_tokens

    return []

def save_tokens(array: Union[List[TOKEN], Tuple[TOKEN]],
                destfile: str) -> None:
    """
        Saves the given token array as a file. Infers the proper type from the first element
        of the array.

        Args:
            array: A token array of utoken16/utoken32/token16/token32 types.
            destfile (str): Destination as a path to save the tokens. Exclude any
                extension from the string. It will be inferred by the function.
    """
    if isinstance(array[0], utoken16):
        filename = abspath(f"{destfile}.utoken_16")
        with open(filename, "wb") as file:
            data = pack("I", len(array))  # Always uint_32
            for token in array:
                data += pack("H", token.count) + pack("H", token.id)
            file.write(compress(data))
    elif isinstance(array[0], utoken32):
        filename = abspath(f"{destfile}.utoken_32")
        with open(filename, "wb") as file:
            data = pack("I", len(array))
            for token in array:
                data += pack("I", token.count) + pack("I", token.id)
            file.write(compress(data))
    elif isinstance(array[0], token16):
        filename = abspath(f"{destfile}.token_16")
        with open(filename, "wb") as file:
            data = pack("I", len(array))
            for token in array:
                data += pack("20H", *token.positions) + pack("H", token.id)
            file.write(compress(data))
    elif isinstance(array[0], token32):
        filename = abspath(f"{destfile}.token_32")
        with open(filename, "wb") as file:
            data = pack("I", len(array))
            for token in array:
                data += pack("20I", *token.positions) + pack("I", token.id)
            file.write(compress(data))

def load_tokens(tokenfile: str) -> List[TOKEN]:
    """
        Loads tokens from a token file.

        Args:
            tokenfile (str): A path that includes the full name and the extension
                of the token file.

        Returns:
            A token array of utoken16/utoken32/token16/token32 types.
    """
    if tokenfile.endswith(".utoken_16"):
        tokens = []
        with open(tokenfile, "rb") as file:
            data = file.read()
        data = decompress(data)
        length = unpack("I", data[:4])
        for i in range(1, length + 1):
            subdata = data[4 * i:4 * (i + 1)]
            tokens.append(utoken16(unpack("H", subdata[:2]), unpack("H", subdata[2:])))
        return tokens

    if tokenfile.endswith(".utoken_32"):
        tokens = []
        with open(tokenfile, "rb") as file:
            data = file.read()
        data = decompress(data)
        length = unpack("I", data[:4])
        for i in range(length):
            subdata = data[4 + 8 * i:4 + 8 * (i + 1)]
            tokens.append(utoken16(unpack("I", subdata[:4]), unpack("I", subdata[4:])))
        return tokens

    if tokenfile.endswith(".token_16"):
        tokens = []
        with open(tokenfile, "rb") as file:
            data = file.read()
        data = decompress(data)
        length = unpack("I", data[:4])
        for i in range(length):
            subdata = data[4 + 42 * i:4 + 42 * (i + 1)]
            positions = unpack("20H", subdata[:-2])
            id = unpack("H", subdata[-2:])
            token = token16(id)
            token.positions = positions
            tokens.append(token)
        return tokens

    if tokenfile.endswith(".token_32"):
        tokens = []
        with open(tokenfile, "rb") as file:
            data = file.read()
        data = decompress(data)
        length = unpack("I", data[:4])
        for i in range(length):
            subdata = data[4 + 84 * i:4 + 84 * (i + 1)]
            positions = unpack("20I", subdata[:-4])
            id = unpack("I", subdata[-4:])
            token = token16(id)
            token.positions = positions
            tokens.append(token)
        return tokens

    return []

def vectorize(tokenlist: List[TOKEN], vocab_size: int, dtype: np.number = np.uint16) -> np.ndarray:
    """
        Vectorizes and turns given tokens to vector-semantic structure.

        Args:
            tokenlist: A token array of utoken16/utoken32/token16/token32 types.
            vocab_size (int): Vocabulary size. This will be the length of each vector.
            dtype (numpy.number): Data type for the numpy.ndarray's that will be created.
                This is not the data type for tokens.

        Returns:
            A numpy.ndarray matrix that consists of vector-semantics.
    """
    if isinstance(tokenlist[0], utoken16):
        if dtype == np.uint8 or dtype == np.int8:
            dtype = np.uint16

        v = np.zeros((vocab_size,), dtype=dtype)
        for token in tokenlist:
            # It is not an assignment but an addition, in case the same token id appears more than once in the file.
            v[token.id] += token.count
        return v

    if isinstance(tokenlist[0], utoken32):
        # dtype is at least np.uint32, since the inner integer type in tokens are 32-bit.
        # The dtype option of the function call is ignored here.
        if dtype == np.uint16 or dtype == np.uint8 or dtype == np.int16 or dtype == np.int8:
            dtype = np.uint32

        v = np.zeros((vocab_size,), dtype=dtype)
        for token in tokenlist:
            v[token.id] += token.count
        return v

    if isinstance(tokenlist[0], token16):
        if dtype == np.uint8 or dtype == np.int8:
            dtype = np.uint16

        vectors = []
        for token in tokenlist:
            for position in token.positions:
                while len(vectors) <= position:
                    vectors.append(np.zeros((vocab_size,), dtype=dtype))
                vectors[position][token.id] += 1
        return np.asarray(vectors)

    if isinstance(tokenlist[0], token32):
        if dtype == np.uint16 or dtype == np.uint8 or dtype == np.int16 or dtype == np.int8:
            dtype = np.uint32

        vectors = []
        for token in tokenlist:
            for position in token.positions:
                while len(vectors) <= position:
                    vectors.append(np.zeros((vocab_size,), dtype=dtype))
                vectors[position][token.id] += 1
        return np.asarray(vectors)

    return np.array([])  # Default case

def chunkify(vectors: np.ndarray, start: int, stop: int, remove_special_tokens: bool = True) -> np.ndarray:
    """
        Divides the given vectors into chunks by the [start]-[stop] tokens. Tokens can be anything
        from [BOS]-[EOS] to some custom implementation. It is required that the chunks would start
        via token-a, and would end with token-b.

        Args:
            vectors (numpy.ndarray): Vector-semantic matrix of the text corpus.
            start (int): ID of the starting token.
            stop (int): ID of the ending token.
            remove_special_tokens (bool): The choice to include or exclude the [start]-[stop] tokens.

        Returns:
            A numpy.ndarray matrix of summed vectors that forms a chunk. A chunk would start from [start]
            and end at [stop].
    """
    collected = []
    if remove_special_tokens:
        for vector in vectors:
            if vector[start] != 0:
                v = np.zeros_like(vector)
                vector = next(vectors)  # In case stop token comes immediately after the start token
                while vector[stop] != 0:
                    vector = next(vectors)
                    v += vector
                collected.append(v)
        # Ignores the tokens at the start that are before a [start].
        # Assumes there is a [stop] at the end always
    else:
        for vector in vectors:
            if vector[start] != 0:
                v = np.zeros_like(vector) + vector  # Include the start token
                vector = next(vectors)
                while vector[stop] != 0:
                    vector = next(vectors)
                    v += vector
                v += vector  # Include the stop token
                collected.append(v)
            # If there is no [stop] at the end, it will not be included and collected
            # list will be formed as if it were there.
    return np.asarray(collected)

def unorder(tokenlist: List[Union[token16, token32]]) -> Union[uint16 * numerical, uint32 * numerical]:
    """
        Turns an ordered set of tokens, to an unordered set of tokens.

        Args:
            tokenlist: A token array of token16/token32 types that will be "unordered".

        Returns:
            A token array of utoken16/utoken32 types that is, unordered.
    """
    maxima = -1
    id_token_match = {}
    for token in tokenlist:
        id = token.id
        if id not in id_token_match:
            id_token_match[id] = []

        for i, position in enumerate(token.positions):
            if position == 0 and i != 0:
                break
            if position > maxima:
                maxima = position
            id_token_match[id].append(position)
    if isinstance(tokenlist[0], token16):
        linear = (uint16 * maxima)()
        for id in id_token_match:
            for position in id_token_match[id]:
                linear[position] = id
        return linear
    if isinstance(tokenlist[0], token32):
        linear = (uint32 * maxima)()
        for id in id_token_match:
            for position in id_token_match[id]:
                linear[position] = id
        return linear


