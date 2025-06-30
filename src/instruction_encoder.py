def encode_r_type(funct, shamt, rd, rs, rt):
    """Codifica uma instrução do tipo R."""
    rd &= 0x1F
    rs &= 0x1F
    rt &= 0x1F
    shamt &= 0x1F
    funct &= 0x3F
    return (0 << 26) | (rs << 21) | (rt << 16) | (rd << 11) | (shamt << 6) | funct

def encode_i_type(opcode, rs, rt, immediate):
    """Codifica uma instrução do tipo I."""
    opcode &= 0x3F
    rs &= 0x1F
    rt &= 0x1F
    immediate &= 0xFFFF  # Garante que o imediato tenha 16 bits
    return (opcode << 26) | (rs << 21) | (rt << 16) | immediate

def encode_j_type(opcode, target_address):
    """Codifica uma instrução do tipo J."""
    opcode &= 0x3F
    # O endereço é deslocado 2 bits para a direita, pois os endereços das instruções são sempre múltiplos de 4
    address = (target_address >> 2) & 0x03FFFFFF
    return (opcode << 26) | address