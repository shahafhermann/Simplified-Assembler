# This file is in charge of the parsing process of files written
# in HACK Assembley.
# Written by Ido Porat and Shahaf Hermann

from translator import Translator


class ParseFile:

    HACK_SUFFIX = ".hack"
    LABEL_START = "("
    LABEL_END = ")"
    COMMENT_START = "/"
    A_INST_START = "@"
    EMPTY_VALUE = "null"
    EQUAL_DELIMITER = "="
    JMP_DELIMITER = ";"
    VAR_START_VALUE = 16
    SUFFIX_DELIMITER = "."
    END_LINE = "\n"

    def __init__(self, file_path, symbol_table):
        """
        Initialize the ParseFile class
        :param file_path: The file to parse
        :param symbol_table: A pre defined dictionary of symbols.
        """
        self.__symbol_table = symbol_table
        self.__file_path = file_path
        self.__translator = Translator()

    def __find_labels(self, file):
        """
        Locate all labels in the file. Labels are lines in the format:( LABEL )
        Spaces are ignored.
        :param file: The file to parse
        """
        line_count = -1
        for line in file:
            line_copy = "".join(line.split())  # Remove all white spaces
            if not line_copy.strip() or line[0] == self.COMMENT_START:
                continue
            elif line_copy[0] == self.LABEL_START in line:
                right_slice = line_copy.split(self.LABEL_START, 1)
                label = right_slice[1].rsplit(self.LABEL_END, 1)[0]
                self.__symbol_table[label] = line_count + 1
                continue
            line_count += 1

    def __a_instruction(self, line, var_count):
        """
        Analyze an A-Instruction and send it for translation.
        :param line: The line to parse
        :param var_count: A counter that keeps track of how many new variables
                           we declared
        :return: A tuple of the binary translation of the line and the new
                  variable count (+1 if it's really new)
        """
        right_slice = line.split(self.A_INST_START, 1)[1].rstrip()
        if self.COMMENT_START in right_slice:  # If there's a trailing comment
            var = right_slice.split(self.COMMENT_START)[0]
        else:
            var = right_slice
        if var.isdigit():  # If it's already a decimal number
            code = self.__translator.translate(int(var),
                                               self.__translator.A_INSTRUCTION)
        elif var in self.__symbol_table:  # If the variable already exists
            code = self.__translator.translate(self.__symbol_table[var],
                                               self.__translator.A_INSTRUCTION)
        else:  # If it's a new variable
            self.__symbol_table[var] = var_count
            code = self.__translator.translate(self.__symbol_table[var],
                                               self.__translator.A_INSTRUCTION)
            var_count += 1

        return code, var_count

    def __c_instruction(self, line):
        """
        Analyze a C-Instruction and send it for translation.
        :param line: The line to parse
        :return: The binary translation of the line
        """
        left_slice = line.split(self.COMMENT_START, 1)[0].rstrip()
        dest, comp, jmp = self.EMPTY_VALUE, self.EMPTY_VALUE, self.EMPTY_VALUE
        if self.EQUAL_DELIMITER in left_slice and self.JMP_DELIMITER in \
                left_slice:  # dest = comp ; jmp
            dest = left_slice.split(self.EQUAL_DELIMITER)[0]
            split_line = left_slice.split(self.JMP_DELIMITER)
            comp = split_line[0]
            jmp = split_line[1]

        elif self.EQUAL_DELIMITER in left_slice:  # dest = comp
            split_line = left_slice.split(self.EQUAL_DELIMITER)
            dest = split_line[0]
            comp = split_line[1]

        else:  # comp ; jmp
            split_line = left_slice.split(self.JMP_DELIMITER)
            comp = split_line[0]
            jmp = split_line[1]

        c_inst = [comp, dest, jmp]
        return self.__translator.translate(c_inst,
                                           self.__translator.C_INSTRUCTION)

    def __write_instructions(self, file, output):
        """
        Analyze the line and decide what's the kind of instruction or if it
        should be ignored.
        At the end write to the output file (if there's anything to write).
        :param file: The file to parse
        :param output: The output file to write to
        """
        var_count = self.VAR_START_VALUE
        for line in file:
            line_copy = "".join(line.split())
            if not line_copy.strip() or line_copy[0] == self.COMMENT_START \
                    or line_copy[0] == self.LABEL_START:
                continue  # Ignore this line

            elif line_copy[0] == self.A_INST_START:  # It's an A-Instruction
                code, var_count = self.__a_instruction(line_copy, var_count)

            else:  # If it's a C_instruction
                code = self.__c_instruction(line_copy)

            output.write(code + self.END_LINE)

    def parse_file(self):
        """
        Manage the parsing process.
        """
        with open(self.__file_path, "r") as file:

            # Create the output file
            file_name = self.__file_path.rsplit(self.SUFFIX_DELIMITER, 1)[0]
            file_name += self.HACK_SUFFIX
            output = open(file_name, "w+")

            # Detect labels
            self.__find_labels(file)

            file.seek(0)  # Rewind the file

            self.__write_instructions(file, output)
