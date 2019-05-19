# The main file of the assembler.
# Written by Ido Porat and Shahaf Hermann

############################################################
# Imports
############################################################
import sys
import os
import copy
import platform
from parse import ParseFile

############################################################
# Constants
############################################################

# --------     Pre-defined Symbols      --------- #
R0 = 0
R1 = 1
R2 = 2
R3 = 3
R4 = 4
R5 = 5
R6 = 6
R7 = 7
R8 = 8
R9 = 9
R10 = 10
R11 = 11
R12 = 12
R13 = 13
R14 = 14
R15 = 15
SCREEN = 16384
KBD = 24576
SP = 0
LCL = 1
ARG = 2
THIS = 3
THAT = 4
SYMBOL_TABLE = {"R0": R0, "R1": R1, "R2": R2, "R3": R3, "R4": R4, "R5": R5,
                "R6": R6, "R7": R7, "R8": R8, "R9": R9, "R10": R10, "R11":
                    R11, "R12": R12, "R13": R13, "R14": R14, "R15": R15,
                "SCREEN": SCREEN, "KBD": KBD, "SP": SP, "LCL": LCL, "ARG":
                    ARG, "THIS": THIS, "THAT": THAT}
WIN_PATH_DEL = "\\"  # Delimiter in Windows based directory path
OTHER_PATH_DEL = "/"  # Delimiter in Other OS's directory path
APPROVED_SUFFIX = ".asm"


def process_file(path):
    """
    Process the given file for parsing.
    :param path: The path of the file to parse
    """
    symbol_table = copy.deepcopy(SYMBOL_TABLE)
    file = ParseFile(path, symbol_table)
    file.parse_file()
    symbol_table.clear()


if __name__ == '__main__':
    for i in range(1, len(sys.argv)):
        if os.path.isdir(sys.argv[i]):  # It's a directory
            for file_name in os.listdir(sys.argv[i]):
                if file_name.endswith(APPROVED_SUFFIX):
                    # Cross platform support:
                    if platform.system() == "Windows":
                        process_file(sys.argv[i] + WIN_PATH_DEL + file_name)
                    else:
                        process_file(sys.argv[i] + OTHER_PATH_DEL + file_name)

        elif os.path.isfile(sys.argv[i]):  # It's a file
            process_file(sys.argv[i])
