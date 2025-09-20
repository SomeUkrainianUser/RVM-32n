import sys
from preprocessor import preprocessor

# ALU operations' opcode masks

ADD = 0b1
SUBTRACT = 0b10
MULTIPLY = 0b11
DIVIDE = 0b100
NEGATE = 0b101
SHL = 0b110
SHR = 0b111
AND = 0b1001
OR = 0b1010
NAND = 0b1011
NOR = 0b1100
NOT = 0b1101
XOR = 0b1110
XNOR = 0b1111

# src argument opcode masks

A_SRC = 0b0
B_SRC = 0b1 << 4
C_SRC = 0b10 << 4
D_SRC = 0b11 << 4
E_SRC = 0b100 << 4
F_SRC = 0b101 << 4
G_SRC = 0b110 << 4
H_SRC = 0b111 <<4
SP_SRC = 0b1000 << 4
IP_SRC = 0b1001 << 4
RAM_PTR_SRC = 0b1010 << 4
RAM_SRC = 0b1011 << 4
IO_SRC = 0b1100 << 4
X_SRC = 0b1101 << 4

# dest argument opcode masks

A_DEST = 0b0
B_DEST = 0b1 << 8
C_DEST = 0b10 << 8
D_DEST = 0b11 << 8
E_DEST = 0b100 << 8
F_DEST = 0b101 << 8
G_DEST = 0b110 << 8
H_DEST = 0b111 << 8
SP_DEST = 0b1000 << 8
IP_DEST = 0b1001 << 8
RAM_PTR_DEST = 0b1010 << 8
RAM_DEST = 0b1011 << 8
IO_DEST = 0b1100 << 8

# jump opcode masks

LESS = 0b1 << 12
EQUAL = 0b1 << 13
GREATER = 0b1 << 14
JMP = 0b1 << 15

# load instruction opcode mask

LDI = 0b1 << 16

# I/O instruction opcode masks

READ = 0b1 << 17
WRITE = 0b1 << 18

#  non-ALU instruction mask

NON_ALU = 0b1 << 31

# instruction sets

ALU_INSTRUCTIONS = ['CMP', 'ADD', 'SUB', 'MUL', 'DIV', 'NEG', 'SHL', 'SHR', 'AND', 'OR', 'NAND', 'NOR', 'NOT', 'XOR', 'XNOR']
JMP_INSTRUCTIONS = ['JMP', 'JE', 'JL', 'JG', 'JLE', 'JGE', 'JNE']

def parse(instruction: str) -> int:
        INSTRUCTION = 0
    
        instruction = instruction.split(' ', 1)
        mnemonic = instruction[0]
        args = instruction[1]
        args = args.replace(' ', '')
        args = args.split(',')

        if mnemonic not in ALU_INSTRUCTIONS: 
                INSTRUCTION |= NON_ALU
                
                match mnemonic:
                        case 'LDI': INSTRUCTION |= LDI
                        case 'READ': INSTRUCTION |= READ
                        case 'WRITE': INSTRUCTION |= WRITE

                if mnemonic in JMP_INSTRUCTIONS:
                        match mnemonic:
                                case 'JMP':
                                        INSTRUCTION |= EQUAL
                                        INSTRUCTION |= LESS
                                        INSTRUCTION |= GREATER
                                case 'JE': INSTRUCTION |= EQUAL
                                case 'JL': INSTRUCTION |= LESS
                                case 'JG': INSTRUCTION |= GREATER
                                case 'JLE':
                                        INSTRUCTION |= EQUAL
                                        INSTRUCTION |= LESS
                                case 'JGE':
                                        INSTRUCTION |= EQUAL
                                        INSTRUCTION |= GREATER
                                case 'JNE':
                                        INSTRUCTION |= LESS
                                        INSTRUCTION |= GREATER

        else:
                match mnemonic:
                        case 'CMP': pass
                        case 'ADD': INSTRUCTION |= ADD
                        case 'SUB': INSTRUCTION |= SUBTRACT
                        case 'MUL': INSTRUCTION |= MULTIPLY
                        case 'DIV': INSTRUCTION |= DIVIDE
                        case 'NEG': INSTRUCTION |= NEGATE
                        case 'SHL': INSTRUCTION |= SHL
                        case 'SHR': INSTRUCTION |= SHR
                    
                        case 'AND': INSTRUCTION |= AND
                        case 'OR': INSTRUCTION |= AND
                        case 'XOR': INSTRUCTION |= XOR
                        case 'NAND': INSTRUCTION |= NAND
                        case 'NOR': INSTRUCTION |= NOR
                        case 'XNOR': INSTRUCTION |= XNOR
                        case 'NOT': INSTRUCTION |= NOT

        if len(args) == 2:
                match args[0]:
                        case 'A':       INSTRUCTION |= A_DEST
                        case 'B':       INSTRUCTION |= B_DEST
                        case 'C':       INSTRUCTION |= C_DEST
                        case 'D':       INSTRUCTION |= D_DEST
                        case 'E':       INSTRUCTION |= E_DEST
                        case 'F':       INSTRUCTION |= F_DEST
                        case 'G':       INSTRUCTION |= G_DEST
                        case 'H':       INSTRUCTION |= H_DEST
                        case 'SP':      INSTRUCTION |= SP_DEST
                        case 'IP':      INSTRUCTION |= IP_DEST
                        case 'RAM_PTR': INSTRUCTION |= RAM_PTR_DEST
                        case 'RAM':     INSTRUCTION |= RAM_DEST
                        case 'IO':      INSTRUCTION |= IO_DEST

                match args[1]:
                        case 'A':       INSTRUCTION |= A_SRC
                        case 'B':       INSTRUCTION |= B_SRC
                        case 'C':       INSTRUCTION |= C_SRC
                        case 'D':       INSTRUCTION |= D_SRC
                        case 'E':       INSTRUCTION |= E_SRC
                        case 'F':       INSTRUCTION |= F_SRC
                        case 'G':       INSTRUCTION |= G_SRC
                        case 'H':       INSTRUCTION |= H_SRC
                        case 'SP':      INSTRUCTION |= SP_SRC
                        case 'IP':      INSTRUCTION |= IP_SRC
                        case 'RAM_PTR': INSTRUCTION |= RAM_PTR_SRC
                        case 'RAM':     INSTRUCTION |= RAM_SRC
                        case 'IO':      INSTRUCTION |= IO_SRC
                
                if args[1].replace('-', '').isnumeric() and not args[1].startswith('0X'):
                        INSTRUCTION |= X_SRC
                        INSTRUCTION |= int(args[1]) << 32
                elif args[1].startswith('0X') and all(c in '0123456789ABCDEF' for c in args[1][2:]):
                        INSTRUCTION |= X_SRC
                        INSTRUCTION |= (int(args[1], 16)) << 32
        else:
                match args[0]:
                        case 'A':       INSTRUCTION |= A_SRC
                        case 'B':       INSTRUCTION |= B_SRC
                        case 'C':       INSTRUCTION |= C_SRC
                        case 'D':       INSTRUCTION |= D_SRC
                        case 'E':       INSTRUCTION |= E_SRC
                        case 'F':       INSTRUCTION |= F_SRC
                        case 'G':       INSTRUCTION |= G_SRC
                        case 'H':       INSTRUCTION |= H_SRC
                        case 'SP':      INSTRUCTION |= SP_SRC
                        case 'IP':      INSTRUCTION |= IP_SRC
                        case 'RAM_PTR': INSTRUCTION |= RAM_PTR_SRC
                        case 'RAM':     INSTRUCTION |= RAM_SRC
                        case 'IO':      INSTRUCTION |= IO_SRC

                if args[0].replace('-', '').isnumeric():
                        INSTRUCTION |= X_SRC
                        INSTRUCTION |= (int(args[0])) << 32
                elif args[1].startswith('0X') and all(c in '0123456789ABCDEF' for c in args[1][2:]):
                        INSTRUCTION |= X_SRC
                        INSTRUCTION |= (int(args[1], 16)) << 32

        
        
        

        return INSTRUCTION

def main():
        with open(sys.argv[1], 'r') as file:
                code = file.read()

        code = preprocessor(code)
        for line in code:
                instruction = parse(line)
                print(str(hex(instruction)).replace('0x', ''))

if __name__ == '__main__':
        main()
