"""
    Helper functions and definitions to perform preprocessing
    on text corpa.
"""

from tokenizers import Tokenizer
from os import walk
from os.path import join
from re import search
from zlib import compress, decompress
from typing import List, Union
from ..utils.exceptions import *


DELIMITER = "\x00\x11\x22\x33\x44\x55".encode("utf-8")
PATTERN = r'^[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{4} [0-9]{,2}:[0-9]{,2} - ([^:]*): '  # Yes.
DATE_FORMAT = "%d.%m.%Y %H:%M"

def tokenize(textfile: str, tokenizer: Tokenizer, ids: bool = False) -> List[Union[str, int]]:
    """
        Tokenizes the given textfile with the given tokenizer.

        Args:
            textfile (str): Path to the textfile that will be tokenized.
            tokenizer (Tokenizer): The tokenizer from Hugging Face's tokenizers
                library to tokenize the text corpus.
            ids (bool): The choice to return the ids or tokens.
    """
    with open(textfile, "r") as file:
        text = file.read()
    if ids:
        return tokenizer.encode(text).ids
    return tokenizer.encode(text).tokens

def create_bulk_text(textfile: str, destfile: str, *args):
    """
        A specialized function to process exported text data from WhatsApp.
        Removes usernames from the text corpus. Connects messages that are
        in itself includes "\n" separator. Saves the processed corpus in
        the destination file.

        Args:
            textfile (str): Source WhatsApp exported text data.
            destfile (str): Destination file in .txt to save the processed text.
            args: Usernames to separate the text by. Must in the in the format
                that is given by " - username: ". Replace the "username" with
                the username(s) in your text file.

    """
    with open(textfile, "r") as file:
        text_data = file.read()
        lines = text_data.split("\n")

    total = [lines[0]]

    last_user = ""
    for user in args:
        if user in lines[0]:
            last_user = user

    for line in lines[1:]:
        if last_user in line:
            total[-1] += line
        else:
            for user in args:
                if user in lines[0]:
                    last_user = user
            total.append(line)

    with open(destfile, "w") as file:
        for line in lines:
            file.write(line[16:] + "\n")

def create_token_file(textfile: str, destfile: str, tokenizer: Tokenizer, ids: bool = False):
    """
        Old utility. Suitable with primitive tokenizers. Formerly used with
        tokenizers from Zemberek library.

        Tokenizes the given text file, saves the tokenized text in a token file in .txt.
        The idea is, there are duplicate tokens in the file.

        Args:
            textfile (str): Source text file.
            destfile (str): Destination to save the token-text file, in .txt.
            tokenizer: Your tokenizer of choice.
            ids (bool): Parameter for the "tokenize" function.

    """
    with open(textfile, "r") as file:
        text = file.read()
    tokens = tokenize(text, tokenizer, ids)
    with open(destfile, "w") as file:
        file.write(",".join(tokens))

def create_reduced_token_file(tokenfile: str, destfile: str):
    """
        Old utility. Suitable with primitive tokenizers. Formerly used with
        tokenizers from Zemberek library.

        Reduces the duplicate tokens in a primitively structured
        token file, in .txt.


    """
    with open(tokenfile, "r") as file:
        full_tokens = file.read().split(",")

    reduced_tokens = list(set(full_tokens))

    with open(destfile, "w") as file:
        file.write(",".join(reduced_tokens))

def list_subdirectories(base_path: str):
    """
        List subdirectories of a given "parent" directory.

        Args:
            base_path (str): Path for the base directory.

        Returns:
            A list of subdirectories.
    """
    subdirectories = []
    for dirpath, dirnames, filenames in walk(base_path):
        subdirectories.extend([join(dirpath, d) for d in dirnames])
        dirnames[:] = []
    return subdirectories

def defense(textfile: str, destfile: str, name: str) -> None:
    """
        Structure the text file in "defense" format. This function is created
        for the WhatsApp message export data format.

        For details on the "defense" format, refer https://github.com/ahmeterdem1/ahmetgpt

        Args:
            textfile (str): Source WhatsApp message export file in .txt.
            destfile (str): The destination as a block-file, in .block.
            name (str): Your WhatsApp username as it appears in the source file.
                Should be in the format " - username: ".
    """
    with open(textfile, "r") as file:
        data = file.read()

    lines = data.split("\n")
    total = [lines[0]]

    found: bool  # This definition is so that, we don't regenerate the same variable again and again.

    for line in lines[1:]:
        found = search(PATTERN, line)

        if found:
            total.append(line)
        else:
            total[-1] += " " + line  # Separator here is not a linebreak, but a space.

    # Ignore the first lines where the first conversator is "self".
    while name in total[0]:
        total.pop(0)

    blocks = []

    index = 0
    line_count = len(total)
    found = False

    while True:
        subblock = []

        if index >= line_count:
            break
        last_index = index
        while True:
            if index >= line_count:
                break
            # Collect others messages
            if name not in total[index]:
                subblock.append(total[index])
                index += 1
            else:
                break

        while True:
            if index >= line_count:
                break
            # Collect self messages
            if name in total[index]:
                subblock.append(total[index])
            else:
                break
            index += 1

        if index == last_index:
            index += 1
            continue
        blocks.append(subblock)

    with open(destfile, "wb") as file:  # Write bytes
        for block in blocks:
            file.write(compress("\n".join(block).encode("utf-8")))
            file.write(DELIMITER)
        file.write(DELIMITER)  # Two delimiters sign that the file is ended.

def attack(textfile: str, destfile: str, name: str, *others) -> None:
    """
        Structure the text file in "attack" format. This function is created
        for the WhatsApp message export data format.

        For details on the "attack" format, refer https://github.com/ahmeterdem1/ahmetgpt

        Args:
            textfile (str): Source WhatsApp message export file in .txt.
            destfile (str): The destination as a block-file, in .block.
            name (str): Your WhatsApp username as it appears in the source file.
                Should be in the format " - username: ".
        """
    with open(textfile, "r") as file:
        data = file.read()

    lines = data.split("\n")
    users = [*others, name]
    total = [lines[0]]

    found: bool
    blocks = []

    for line in lines[1:]:
        found = False
        for user in users:
            if user in users:
                found = True
                break

        if found:
            total.append(line)
        else:
            total[-1] += " " + line

    for other in others:
        while other in total[0]:
            total.pop(0)

    index = 0
    line_count = len(total)
    while True:
        subblock = []

        if index >= line_count:
            break
        last_index = index

        while True:
            if index >= line_count:
                break
            # Collect self messages
            if name in total[index]:
                subblock.append(total[index])
            else:
                break
            index += 1

        while True:
            if index >= line_count:
                break
            # Collect others messages
            if name not in total[index]:
                subblock.append(total[index])
                index += 1
            else:
                break
        if index == last_index:
            index += 1
            continue
        blocks.append(subblock)

    with open(destfile, "wb") as file:
        for block in blocks:
            file.write(compress("\n".join(block).encode("utf-8")))
            file.write(DELIMITER)
        file.write(DELIMITER)

def read_blockfile(blockfile: str) -> List[str]:
    """
        Read and return data from a blockfile, in .block.

        Args:
            blockfile (str): Path to the blockfile to be read.

        Returns:
            A list of conversation blocks read from the blockfile.
    """
    with open(blockfile, "rb") as file:  # Read bytes
        data = file.read()

    if not data.endswith(DELIMITER + DELIMITER):
        raise FileCorruptedError()

    data.replace(DELIMITER + DELIMITER, "".encode("utf-8"))
    compressed_blocks = data.split(DELIMITER)
    blocks = []

    for block in compressed_blocks:
        if block:
            blocks.append(str(decompress(block), "utf-8"))

    return blocks
