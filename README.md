# RVM-32n

This is a hobby project of creating a CPU architecture. Below you will see some specs and guide on how to program it.

This CPU operates in 32-bit words, as the name suggests, although the full instructions it takes are 64 bits, with bits 32-63 dedicated to immediate operand. It has 8 general purpose 32-bit registers named A through H and specialized registers as follows:
- SP for stack operations
- IP for counting instructions
- RAM_ptr for pointing to a RAM address
- RAM(not a physical register but is treated as such) for writing data to RAM. The data goes at address pointed to by RAM_ptr
- IO for working with I/O
- Flags(3-bit register) for conditionals

The CPU has 8 I/O ports for input and output each numbered 0-7. 

The instruction structure:

`00000000000000000000000000000000|0|0000000000000|0|0|0|000|0000|0000|0000`, where | separates different functional blocks which are as follows:

- bits 0-3 - ALU opcodes, set which operation the ALU shall perform. Available operations:

  - 0000 - cmp x, y
  - 0001 - x+y
  - 0010 - x-y
  - 0011 - xy
  - 0100 - x/y(no floating point)
  - 0101 - -x
  - 0110 - x<<y
  - 0111 - x>>y
  - 1000 - nop
  - 1001 - x and y
  - 1010 - x or y
  - 1011 - x nand y
  - 1100 - x nor y
  - 1101 - not x
  - 1110 - x xor y
  - 1111 - x xnor y

- bits 4-7 - src opcodes, denote where to take the data from usually, as implied by the name, but can also mean a place in the code if used with jmp or a port number if used with I/O instructions. In operations you have been presented with above, src is Y.
- bits 8-11 - dest opcodes, denote where the data goes, as implied by the name, and the primary operand. In operations you have been presented with above, dest is X. The opcodes are as follows:

  - General purpose registers A through H - 0000-0111 respectively in alphabetical order
  - Stack pointer SP - 1000
  - Instruction pointer IP - 1001
  - RAM pointer RAM_ptr - 1010
  - RAM value pseudoregister RAM - 1011
  - I/O register IO - 1100
  - Immediate operand X - 1101
  
  P.S. Immediate operand opcode can only be passed to src

- bits 12-14 - condition opcodes for jmp. The opcodes for conditions are as follows:
  - bit 12 - less than
  - bit 13 - equal to
  - bit 14 - greater than
 
  These can be combined in any combinations to create more complex conditions. Enabling all of them makes an unconditional jump.
- bit 15 - jmp instruction. Occurs unconditionally or if the conditions given in previous block match the results in flags register.
- bit 16 - ldi instruction. Loads data from one place into another.
- bit 17 - read instruction. Reads data into IO register from the specified port.
- bit 18 - write instruction. Writes data from IO register into a specified port.
- bits 19-30 - unused for now.
- bit 31 - instruction type opcode. 0 means an ALU instruction, such being all the arithmetic and logical operations together with cmp. 1 means a non-ALU instructions, such being ldi, jmp and all of its conditional variants, read and write.
- bits 32-63 - encode an immediate operand that is referenced as X when passed in place of src.

# Assembly mnemonics and directives

- `ldi [dest], [src]` - loads `[src]` into `[dest]`
- `read [port]` - reads into I/O register from port with specified number
- `write [port]` - writes from I/O register into port with specified number
- `jmp [label/line]` - changes IP to `[label/line]`. The conditional variants only jump if the flags register matches the condition, they are as follows:

  - je - jump if equal to
  - jl - jump if less than
  - jg - jump if greater than
  - jle - jump if less than or equal to
  - jge - jump if greater than or equal to
  - jne - jump if not equal

  P.S. Labels are unsupported as of right now. As soon as the preprocessor will be written, this line will be removed.
- `cmp [op1], [op2]` - compares the operands, sets the flags according to the value of `[op1]` in relation to `[op2]`
- `add [dest], [src]` - adds `[dest]` and `[src]` and writes the result to `[dest]`
- `sub [dest], [src]` - subtracts `[src]` from `[dest]` and writes the result to `[dest]`
- `mul [dest], [src]` - multiplies `[dest]` and `[src]` and writes the result to `[dest]`
- `div [dest], [src]` - divides `[dest]` by `[src]` and writes the result to `[dest]`
- `neg [dest]` - negates `[dest]`
- `shl [dest], [src]` - shifts `[dest]` logically left by `[src]` bits and writes it to `[dest]`
- `shr [dest], [src]` - shifts `[dest]` logically right by `[src]` bits and writes it to `[dest]`
- `and [dest], [src]` - performs logical AND on `[dest]` and `[src]` and writes result to `[dest]`
- `or [dest], [src]` - performs logical OR on `[dest]` and `[src]` and writes result to `[dest]`
- `xor [dest], [src]` - performs logical XOR on `[dest]`and `[src]` and writes result to `[dest]`
- `nand [dest], [src]` - performs logical NAND on `[dest]` and `[src]` and writes result to `[dest]`
- `nor [dest], [src]` - performs logical NOR on `[dest]` and `[src]` and writes result to `[dest]`
- `xnor [dest], [src]` - performs logical XNOR on `[dest]` and `[src]` and writes result to `[dest]`
- `not [dest]` - performs logical NOT on `[dest]`

- `$define [name] [value]` - creates a constant `[name]` and replaces all instances of it with `[value]`
- `$label [label_name]` - creates a label to ease work with jump instructions

Assembler usage: `python3 assembler.py [code_file]`
