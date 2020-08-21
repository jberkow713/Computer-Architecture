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
        #set to 0xF4 when reset
        self.reg[7] = 0xF4
        self.fl = None 

    def load(self, file=None):
        """Load a program into memory."""

        address = 0

        #open the examples folder + filename 
        if file:
            with open('./examples/' + file) as f:
                address = 0
                #split the lines and take the integer before the #
                # plug that value into the program as the command, perform the command

                for line in f:
                    line = line.split("#")[0].strip()
                    if line == '':
                        continue
                    else:
                        #interprets command into binary, hence the 2
                        command = int(line, 2)  
                        self.ram[address] = command
                        address += 1     

        

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
        #multiplies a *b and returns it in a's value
        elif op == "AND":
            self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]

        elif op == "OR":
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
        elif op == "XOR":
            self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]    
        



        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]   
        elif op == "SUB": 
            if self.reg[reg_a] >= self.reg[reg_b]:
                self.reg[reg_a] -= self.reg[reg_b]  
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.reg[reg_a] = (self.reg[reg_b] - self.reg[reg_a]) * -1

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
            MUL = 0b10100010
            PUSH = 0b01000101
            POP = 0b01000110
            JMP = 0b01010100
            CMP = 0b10100111
            JNE = 0b01010110
            JEQ = 0b01010101
            MOD = 0b10100100

            #setting variables for incrementing commands
            ir = self.ram[self.pc]
            operation_a = self.ram[self.pc + 1] #next command
            operation_b = self.ram[self.pc + 2] #command after next command



            #if the register you are on has HLT on it, 
            #stop the emulator, and exit by incrementing by 1 

            if ir == HLT:
                running = False
                self.pc += 1


            # LDI, or Load Immediate; set specified register to specific value by setting the 
            # current register's value to the next one in the PC, and then jump over both of 
            # these operations by incrementing by 3, you're actually setting the index at operation
            # a in the register's value to equal operation b's register number

            elif ir == LDI:

                self.reg[operation_a] = operation_b
                
                self.pc += 3



            # PRN, or print register: prints the 1st register,
            #increment 2 steps

            elif ir == PRN:
                print(self.reg[operation_a])
                self.pc += 2   

            #if the command is MUL, take operation A's value, multiply it by operation B's value, 
            # store it as operation A's value
            elif ir == MUL:
                self.reg[operation_a] *= self.reg[operation_b]

                self.pc += 3    

            elif ir == PUSH:
                #decrement Stack
                self.reg[7] -= 1

                # Get value from register
                reg_num = self.ram[self.pc + 1]
                value = self.reg[reg_num]

                # Store it on the stack
                top_of_stack_addr = self.reg[7]
                self.ram[top_of_stack_addr] = value

                self.pc += 2

            elif ir == POP:
                #increment stack
                value = self.ram_read(self.reg[7])
                self.reg[operation_a] = value
                
                self.reg[7] +=1
                self.pc +=2
            #compare values in subsequent registers
            elif ir == CMP:
                #if even    
                if self.reg[operation_a] == self.reg[operation_b]:
                    self.fl = "E"
                    self.pc += 3    
                #if a < b set to less than
                elif self.reg[operation_a] < self.reg[operation_b]:
                    self.fl = "LT"
                    self.pc += 3
                #if a >b, set to greater than
                elif self.reg[operation_a] > self.reg[operation_b]:
                    self.fl = "GT"
                    self.pc += 3
                
                else:
                    self.fl = 0
                    self.pc += 3    
            #set pc command to value in next register
            elif ir == JMP:

                self.pc = self.reg[operation_a]
            #if fl is not E, set pc to value in next register
            elif ir == JNE:
                
                if self.fl != "E":
                    self.pc = self.reg[operation_a]
                #otherwise increment by 2, go to next command
                else:
                    self.pc += 2  
            # if flag = E, set pc address to value in next register 
            elif ir == JEQ:

                if self.fl == "E":
                    self.pc = self.reg[operation_a]

                else:
                    self.pc += 2      

            elif ir == "MOD":
                self.reg[operation_a] = self.reg[operation_a] % self.reg[operation_b]

                if self.reg[operation_b] == 0:
                    print("ERROR")
                    running = False               













             
