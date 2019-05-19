# This file is in charge of the translation process from decimal to binary of
# commands written in HACK Assembley.
# Written by Ido Porat and Shahaf Hermann


class Translator:

    A_INSTRUCTION = 0
    C_INSTRUCTION = 1

    # Pre defined binary sequences for allowed operation.
    COMP_TABLE = {"0": "1110101010", "1": "1110111111", "-1":
                  "1110111010", "D": "1110001100", "A": "1110110000",
                  "!D": "1110001101", "!A": "1110110001", "-D":
                  "1110001111", "-A": "1110110011", "D+1": "1110011111",
                  "A+1": "1110110111", "D-1": "1110001110", "A-1":
                  "1110110010", "D+A": "1110000010", "D-A":
                  "1110010011", "A-D": "1110000111", "D&A":
                  "1110000000", "D|A": "1110010101", "M": "1111110000",
                  "!M": "1111110001", "-M": "1111110011", "M+1":
                  "1111110111", "M-1": "1111110010", "D+M":
                  "1111000010", "D-M": "1111010011", "M-D":
                  "1111000111", "D&M": "1111000000", "D|M":
                  "1111010101", "D*A": "1100000000", "D*M":
                  "1101000000", "D<<": "1010110000", "A<<":
                  "1010100000", "M<<": "1011100000", "D>>":
                  "1010010000", "A>>": "1010000000",  "M>>":
                  "1011000000"}
    DEST_TABLE = {"null": "000", "M": "001", "D": "010", "MD": "011",
                  "A": "100", "AM": "101",
                  "AD": "110", "AMD": "111"}
    JMP_TABLE = {"null": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
                 "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}

    DEC_TO_BIN = '{0:016b}'  # Translation format

    def translate(self, parameters, instruction):
        """
        Translate the given parameters to binary.
        :param parameters: The given command
        :param instruction: Used to decide if it should be an A or C
                            instruction.
        :return:
        """
        if instruction == self.A_INSTRUCTION:
            return self.DEC_TO_BIN.format(parameters)  # Convert to binary
        else:
            code = self.COMP_TABLE[parameters[0]] + \
                   self.DEST_TABLE[parameters[1]] + \
                   self.JMP_TABLE[parameters[2]]
            return code
