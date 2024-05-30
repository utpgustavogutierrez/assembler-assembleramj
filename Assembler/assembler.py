import re

# Expresiones regulares para comentarios, directivas e instrucciones
commentRe = re.compile(r'\s*#.*$')
directiveRe = re.compile(r'\.\w+')
instructionRe = re.compile(r'\s*(\w+)\s+([^#]+)')

# Códigos de operación instrucciones de RISCV
opcodeMap = {
    'addi': '0010011',
    'add': '0110011',
    'lw': '0000011',
    'sw': '0100011',
    'beq': '1100011',
}

registerMap = {
    'zero': '00000', 
    'ra': '00001', 
    'sp': '00010', 
    'gp': '00011',
    'tp': '00100', 
    't0': '00101', 
    't1': '00110', 
    't2': '00111',
    's0': '01000', 
    'fp': '01000', 
    's1': '01001', 
    'a0': '01010',
    'a1': '01011', 
    'a2': '01100', 
    'a3': '01101', 
    'a4': '01110',
    'a5': '01111', 
    'a6': '10000', 
    'a7': '10001', 
    's2': '10010',
    's3': '10011', 
    's4': '10100', 
    's5': '10101', 
    's6': '10110',
    's7': '10111', 
    's8': '11000', 
    's9': '11001', 
    's10': '11010',
    's11': '11011', 
    't3': '11100', 
    't4': '11101', 
    't5': '11110',
    't6': '11111', 
    'x0': '00000', 
    'x1': '00001', 
    'x2': '00010', 
    'x3': '00011',
    'x4': '00100', 
    'x5': '00101', 
    'x6': '00110', 
    'x7': '00111',
    'x8': '01000', 
    'x9': '01001', 
    'x10': '01010', 
    'x11': '01011',
    'x12': '01100', 
    'x13': '01101', 
    'x14': '01110', 
    'x15': '01111',
    'x16': '10000', 
    'x17': '10001', 
    'x18': '10010', 
    'x19': '10011',
    'x20': '10100', 
    'x21': '10101', 
    'x22': '10110', 
    'x23': '10111',
    'x24': '11000', 
    'x25': '11001', 
    'x26': '11010', 
    'x27': '11011',
    'x28': '11100', 
    'x29': '11101', 
    'x30': '11110', 
    'x31': '11111',
}

def parseImmediate(imm, bits):
    onlyNumericImm = imm.split()[0]
    value = int(onlyNumericImm)
    if value < 0:
        value = (1 << bits) + value
    binValue = format(value, f'0{bits}b')
    return binValue

def parseInstruction(instruction, args):
    opcode = opcodeMap[instruction]

    if instruction == 'addi':
        rd, rs1, imm = map(str.strip, args.split(','))
        rd = registerMap[rd]
        rs1 = registerMap[rs1]
        imm = parseImmediate(imm, 12)
        funct3 = '000'
        return imm + rs1 + funct3 + rd + opcode

    if instruction == 'add':
        rd, rs1, rs2 = map(str.strip, args.split(','))
        rd = registerMap[rd]
        rs1 = registerMap[rs1]
        rs2 = registerMap[rs2]
        funct3 = '000'
        funct7 = '0000000'
        return funct7 + rs2 + rs1 + funct3 + rd + opcode

    if instruction == 'lw' or instruction == 'sw':
        rd, offset_rs1 = map(str.strip, args.split(','))
        offset, rs1 = map(str.strip, offset_rs1.split('('))
        rs1 = registerMap[rs1.strip(')')]
        rd = registerMap[rd]
        imm = parseImmediate(offset, 12)
        funct3 = '010' if instruction == 'lw' else '010'
        return imm + rs1 + funct3 + rd + opcode

    if instruction == 'beq':
        rs1, rs2, label = map(str.strip, args.split(','))
        rs1 = registerMap[rs1]
        rs2 = registerMap[rs2]
        imm = parseImmediate('0', 12)  # Se puede reemplazar el '0' con el label offset actual
        return imm[0] + imm[2:8] + rs2 + rs1 + '000' + imm[8:12] + opcode


    return '0' * 32 

def assemble(inputFile, outputFile):
    with open(inputFile, 'r') as infile, open(outputFile, 'wb') as outfile:
        for line in infile:
            line = line.strip()
            if not line or commentRe.match(line) or directiveRe.match(line):
                continue

            match = instructionRe.match(line)
            if match:
                instruction = match.group(1)
                args = match.group(2)
                binaryInstruction = parseInstruction(instruction, args)
                bytecode = int(binaryInstruction, 2).to_bytes(4, byteorder='little')
                outfile.write(bytecode)

assemble('input.asm', 'output.bin')

with open('output.bin','rb') as f:
    bytecode = f.read()
    hexadecimalString = ""
    binaryString = ""
    for i,byte in enumerate(bytecode,1):
        hexadecimalString += hex(byte)[2:].zfill(2)
        binaryString += bin(byte)[2:].zfill(8)

        if i % 4 == 0:
            print("Hexadecimal:",hexadecimalString)
            hexadecimalString = ""
            print("Binary:", binaryString)
            binaryString = ""
            print("\n")

        elif i == len(bytecode):
            print("Hexadecimal:",hexadecimalString)
            print("Binary:", binaryString)