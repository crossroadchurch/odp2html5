# -*- coding: utf-8 -*-
# pylint: disable=C0103 # Snake-case naming convention
# pylint: disable=R0903 # Too few public methods

import re

ROMAN_C = ['', 'c', 'cc', 'ccc', 'cd', 'd', 'dc', 'dcc', 'dccc', 'cm']
ROMAN_X = ['', 'x', 'xx', 'xxx', 'xl', 'l', 'lx', 'lxx', 'lxxx', 'xc']
ROMAN_I = ['', 'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix']
LETTERS = "abcdefghijklmnopqrstuvwxyz"

def units_to_float(unit_str):
    return float(re.sub(r'[^0-9.\-]', '', unit_str))

def units_to_int(unit_str):
    return int(re.sub(r'[^0-9.\-]', '', unit_str))

def int_to_roman(val, uppercase):
    roman_str = "m" * int(val / 1000)
    val = val % 1000
    roman_str += ROMAN_C[int(val / 100)]
    val = val % 100
    roman_str += ROMAN_X[int(val / 10)]
    val = val % 10
    roman_str += ROMAN_I[val]
    if uppercase:
        roman_str = roman_str.upper()
    return roman_str

def int_to_alpha(val, uppercase):
    alpha_str = ""
    while val:
        alpha_str = LETTERS[(val-1) % 26] + alpha_str
        val = (val-1) // 26
    if uppercase:
        alpha_str = alpha_str.upper()
    return alpha_str

def int_to_format(val, format):
    if format == "a":
        output = int_to_alpha(val, False)
    elif format == "A":
        output = int_to_alpha(val, True)
    elif format == "i":
        output = int_to_roman(val, False)
    elif format == "I":
        output = int_to_roman(val, True)
    else:
        output = str(val)
    return output

class ODPFunctions():
    pass

if __name__ == "__main__":
    print(int_to_roman(1999, False))
    print(int_to_roman(2019, True))
    for i in range(1, 1000):
        print(str(i) + " " + int_to_alpha(i, True))
