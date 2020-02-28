"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.SP = 128

    def load(self, file):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            # 0b10000010, # LDI R0,8
            # 0b00000000,
            # 0b00001000,
            # 0b01000111, # PRN R0
            # 0b00000000,
            # 0b00000001, # HLT
        ]

        # open file
        with open(str(file)) as x:
            # check that the file exists
            if not file:
                print('Sorry! Could not find that file')
                sys.exit(1)
            # loop through each row of the file
            for row in x:
                # split each "word" apart and ignore comments/spaces
                row = row.split(' ')[0].rstrip('#')
                if row == '':
                    continue
                # convert binary string to integer
                row = int(row, 2)
                # append each "word" to the updated program list
                program.append(row)

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""

        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001

        while True:
            # HLT
            if self.ram[self.pc] == HLT:
                sys.exit(0)

            # LDI
            elif self.ram[self.pc] == LDI:
                self.reg[self.ram_read(self.pc + 1)] = self.ram_read(self.pc + 2)
                self.pc += 3

            # PRN
            elif self.ram[self.pc] == PRN:
                print(self.reg[self.ram_read(self.pc + 1)])
                self.pc += 2

            # MUL
            elif self.ram[self.pc] == MUL:
                print(self.reg[self.ram[self.pc + 1]] * self.reg[self.ram[self.pc + 2]])
                self.pc += 3

            # PUSH
            elif self.ram[self.pc] == PUSH:
                self.SP -= 1
                self.ram[self.SP] = self.reg[self.ram[self.pc + 1]]
                self.pc += 2

            # POP
            elif self.ram[self.pc] == POP:
                self.reg[self.ram[self.pc + 1]] = self.ram[self.SP]
                self.SP += 1
                self.pc += 2

            # CALL
            elif self.ram[self.pc] == CALL:
                self.SP -= 1
                self.ram[self.SP] = self.pc + 2
                self.pc = self.reg[self.ram[self.pc + 1]]

            # RET
            elif self.ram[self.pc] == RET:
                self.pc = self.ram[self.SP]
                self.SP += 1

            # else break the while loop
            else:
                print(f"I did not understand that command: {self.ram[self.pc]}")
                sys.exit(1)
