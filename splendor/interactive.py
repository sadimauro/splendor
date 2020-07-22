"""
interactive.py - helper functions for Splendor interactive mode.
"""

import sys
from typing import (
        Any, 
        Tuple,
        Type,
        )

import logging
logging.basicConfig(level=logging.INFO)

def prompt_yn(
        prompt: str="",
        out=sys.stdout,
        ) -> bool:
    """
    """
    if prompt != "":
        prompt += " (y/n): "
    while True:
        try:
            text_in = input(prompt)
        except EOFError as e:
            raise e
        text_in_cleaned = text_in.strip().upper()
        if text_in_cleaned == 'Y':
            return True
        elif text_in_cleaned == 'N':
            return False
        else:
            print("error: must enter 'y' or 'n'", file=out)
            continue

def prompt_number(
        prompt: str="",
        typ: Type=int,
        input_range: Tuple=None,
        out=sys.stdout,
        ) -> int:
    """
    Prompt the user for a number (int or float).  

    If range (e.g. (3, 6)) is specified, the user-inputted int must be between the specified min and max, inclusive.
    """
    if typ != int and typ != float:
        raise Exception("type must be int or float")

    if input_range != None:
        if type(input_range) != tuple:
            raise Exception("input range must be a tuple")
        if len(input_range) != 2:
            raise Exception("input range be in the form (min, max)")
        if type(input_range[0]) != typ or type(input_range[1]) != typ:
            raise Exception(f"input range values must be {typ.__name__}s")
        if input_range[0] > input_range[1]:
            raise Exception("input range min must be less than or equal to the max")

    if prompt != "":
        prompt += f" ({typ.__name__}" + \
            ((" in range " + str(input_range)) if input_range != None else "") + \
            "): "

    while True:
        try:
            text_in = input(prompt)
        except EOFError as e:
            raise e
        text_in_cleaned = text_in.strip()

        try:
            text_in_casted = typ(text_in_cleaned)
        except ValueError:
            print(f"'{text_in_cleaned}' is not an {typ.__name__}", file=out)
            continue
        if input_range != None:
            if text_in_casted < input_range[0] or text_in_casted > input_range[1]:
                print(f"error: input must be between {input_range[0]} and {input_range[1]}, inclusive", file=out)
                continue
        
        return text_in_casted

def prompt_string(
        prompt: str="",
        max_len: int=255,
        out=sys.stdout,
        ) -> int:
    """
    Prompt the user for a string.
    """
    if prompt != "":
        prompt += " (string): " 

    while True:
        try:
            text_in = input(prompt)
        except EOFError as e:
            raise e
        text_in_cleaned = text_in.strip()
        if text_in_cleaned == "":
            print("error: empty string", file=out)
            continue
        if len(text_in_cleaned) > max_len:
            print("error: too long", file=out)
            continue
        return text_in_cleaned
