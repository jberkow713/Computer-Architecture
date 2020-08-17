"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        #starting registers
        self.reg = [0] * 8
        #starting pc command
        self.pc = 0
        #256 bits memory in binary
        self.ram = [0b0] * 256
       
        self.reg[7] = 0xF4

    def load(self):
        """Load a program into memory."""

        address = 0
        registers = [0] * 8

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1
    
    def ram_read(self, address):

        # return address you are looking to read information from

       

        """prints what's stored in that specified address in RAM"""

        return self.ram[address]

        #return specific value at specific index in program[]

    def ram_write(self, value, address):

        #take in specific value put in program[address]


        self.ram[address] = value




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

    def run(self):
        """Run the CPU."""
        running = True

        while running:
                        
            HLT = 0b00000001

            LDI = 0b10000010

            PRN = 0b01000111
            
            
            #setting variables for register 1 and 2
            ir = self.ram[self.pc]
            operation_a = self.ram[self.pc + 1] # register 1
            operation_b = self.ram[self.pc + 2] # register 2



            #if the register you are on has HLT on it, 
            #stop the emulator, and exit by incrementing by 1 

            if ir == HLT:
                running = False
                self.pc += 1


            # LDI, or Load Immediate; set specified register to specific value by setting the 
            # current register's value to the next one in the PC, and then jump over both of 
            # these operations by incrementing by 3

            elif ir == LDI:

                self.reg[operation_a] = operation_b
                
                self.pc += 3



            # PRN, or print register: prints the 1st register,
            #increment 2 steps

            elif ir == PRN:
                print(self.reg[operation_a])
                self.pc += 2    
