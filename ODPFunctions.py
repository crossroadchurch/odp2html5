# -*- coding: utf-8 -*-
# pylint: disable=C0103 # Snake-case naming convention
# pylint: disable=R0903 # Too few public methods

import re

def units_to_float(unit_str):
    return float(re.sub(r'[^0-9.\-]', '', unit_str))

def units_to_int(unit_str):
    return int(re.sub(r'[^0-9.\-]', '', unit_str))

class ODPFunctions():
    pass
