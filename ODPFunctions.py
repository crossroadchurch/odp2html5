import re

def units_to_float(unit_str):
    return float(re.sub(r'[^0-9.\-]', '', unit_str))

class ODPFunctions():
    pass
