import re
from instruction_encoder import encode_r_type, encode_i_type, encode_j_type

def parse_offset(operand):
    """Função utilitária para extrair offset e registrador de operandos como '0($sp)'"""
    match = re.match(r"(\d+)\((\$\w+)\)", operand)
    if match:
        return int(match.group(1)), match.group(2)
    raise ValueError(f"Formato de operando inválido para offset: {operand}")

# --- Handlers de Instruções ---
# Cada função handle simula a execução de uma instrução MIPS específica
# Elas recebem o estado atual do processador e a instrução decodificada

def handle_add(state, inst):
    """Simula a instrução ADD: rd = rs + rt"""
    rd, rs, rt = inst['rd'], inst['rs'], inst['rt']
    val_rs = state.get_register_value(rs)
    val_rt = state.get_register_value(rt)
    result = val_rs + val_rt
    state.set_register_value(rd, result)
    
    # Gera e armazena o código binário da instrução para exibição na GUI
    rd_num = state.get_register_number(rd)
    rs_num = state.get_register_number(rs)
    rt_num = state.get_register_number(rt)
    state.instruction_info[state.pc]['binary'] = encode_r_type(0x20, 0, rd_num, rs_num, rt_num)

def handle_addi(state, inst):
    """Simula a instrução ADDI: rt = rs + immediate"""
    rt, rs, imm = inst['rt'], inst['rs'], inst['imm']
    val_rs = state.get_register_value(rs)
    result = val_rs + imm
    state.set_register_value(rt, result)
    
    rs_num = state.get_register_number(rs)
    rt_num = state.get_register_number(rt)
    state.instruction_info[state.pc]['binary'] = encode_i_type(0x08, rs_num, rt_num, imm)

def handle_sub(state, inst):
    """Simula a instrução SUB: rd = rs - rt"""
    rd, rs, rt = inst['rd'], inst['rs'], inst['rt']
    val_rs = state.get_register_value(rs)
    val_rt = state.get_register_value(rt)
    result = val_rs - val_rt
    state.set_register_value(rd, result)
    
    rd_num = state.get_register_number(rd)
    rs_num = state.get_register_number(rs)
    rt_num = state.get_register_number(rt)
    state.instruction_info[state.pc]['binary'] = encode_r_type(0x22, 0, rd_num, rs_num, rt_num)

def handle_mult(state, inst):
    """Simula a instrução MULT: rd = rs * rt (versão simplificada)"""
    # Nota: MIPS real usa registradores especiais HI/LO. Aqui, simplificamos para um registrador de destino.
    rd, rs, rt = inst['rd'], inst['rs'], inst['rt']
    val_rs = state.get_register_value(rs)
    val_rt = state.get_register_value(rt)
    result = val_rs * val_rt
    state.set_register_value(rd, result)

    rd_num = state.get_register_number(rd)
    rs_num = state.get_register_number(rs)
    rt_num = state.get_register_number(rt)
    state.instruction_info[state.pc]['binary'] = encode_r_type(0x18, 0, rd_num, rs_num, rt_num)

def handle_and(state, inst):
    """Simula a instrução AND: rd = rs & rt"""
    rd, rs, rt = inst['rd'], inst['rs'], inst['rt']
    val_rs = state.get_register_value(rs)
    val_rt = state.get_register_value(rt)
    result = val_rs & val_rt
    state.set_register_value(rd, result)
    
    rd_num = state.get_register_number(rd)
    rs_num = state.get_register_number(rs)
    rt_num = state.get_register_number(rt)
    state.instruction_info[state.pc]['binary'] = encode_r_type(0x24, 0, rd_num, rs_num, rt_num)

def handle_or(state, inst):
    """Simula a instrução OR: rd = rs | rt"""
    rd, rs, rt = inst['rd'], inst['rs'], inst['rt']
    val_rs = state.get_register_value(rs)
    val_rt = state.get_register_value(rt)
    result = val_rs | val_rt
    state.set_register_value(rd, result)
    
    rd_num = state.get_register_number(rd)
    rs_num = state.get_register_number(rs)
    rt_num = state.get_register_number(rt)
    state.instruction_info[state.pc]['binary'] = encode_r_type(0x25, 0, rd_num, rs_num, rt_num)
    
def handle_sll(state, inst):
    """Simula a instrução SLL (Shift Left Logical): rd = rt << shamt"""
    rd, rt, shamt = inst['rd'], inst['rt'], inst['shamt']
    val_rt = state.get_register_value(rt)
    result = val_rt << shamt
    state.set_register_value(rd, result)

    rd_num = state.get_register_number(rd)
    rt_num = state.get_register_number(rt)
    state.instruction_info[state.pc]['binary'] = encode_r_type(0x00, shamt, rd_num, 0, rt_num)

def handle_slt(state, inst):
    """Simula a instrução SLT (Set on Less Than): rd = (rs < rt) ? 1 : 0"""
    rd, rs, rt = inst['rd'], inst['rs'], inst['rt']
    val_rs = state.get_register_value(rs)
    val_rt = state.get_register_value(rt)
    result = 1 if val_rs < val_rt else 0
    state.set_register_value(rd, result)

    rd_num = state.get_register_number(rd)
    rs_num = state.get_register_number(rs)
    rt_num = state.get_register_number(rt)
    state.instruction_info[state.pc]['binary'] = encode_r_type(0x2A, 0, rd_num, rs_num, rt_num)

def handle_slti(state, inst):
    """Simula a instrução SLTI (Set on Less Than Immediate): rt = (rs < immediate) ? 1 : 0"""
    rt, rs, imm = inst['rt'], inst['rs'], inst['imm']
    val_rs = state.get_register_value(rs)
    result = 1 if val_rs < imm else 0
    state.set_register_value(rt, result)
    
    rs_num = state.get_register_number(rs)
    rt_num = state.get_register_number(rt)
    state.instruction_info[state.pc]['binary'] = encode_i_type(0x0A, rs_num, rt_num, imm)

def handle_lui(state, inst):
    """Simula a instrução LUI (Load Upper Immediate): rt = immediate << 16"""
    rt, imm = inst['rt'], inst['imm']
    result = imm << 16
    state.set_register_value(rt, result)

    rt_num = state.get_register_number(rt)
    state.instruction_info[state.pc]['binary'] = encode_i_type(0x0F, 0, rt_num, imm)

def handle_lw(state, inst):
    """Simula a instrução LW (Load Word): rt = Memory[rs + offset]"""
    rt, operand2 = inst['rt'], inst['operand2']
    offset, base_reg = parse_offset(operand2)
    
    eff_addr = state.get_register_value(base_reg) + offset
    if eff_addr % 4 != 0:
        raise ValueError(f"Endereço não alinhado para lw: {eff_addr}")

    # Lê 4 bytes da memória (big-endian) e converte para um inteiro
    val = int.from_bytes(state.memory[eff_addr:eff_addr+4], 'big')
    state.set_register_value(rt, val)

    rs_num = state.get_register_number(base_reg)
    rt_num = state.get_register_number(rt)
    state.instruction_info[state.pc]['binary'] = encode_i_type(0x23, rs_num, rt_num, offset)

def handle_sw(state, inst):
    """Simula a instrução SW (Store Word): Memory[rs + offset] = rt"""
    rt, operand2 = inst['rt'], inst['operand2']
    offset, base_reg = parse_offset(operand2)

    eff_addr = state.get_register_value(base_reg) + offset
    if eff_addr % 4 != 0:
        raise ValueError(f"Endereço não alinhado para sw: {eff_addr}")

    # Converte o valor do registrador para 4 bytes (big-endian) e escreve na memória
    val = state.get_register_value(rt)
    state.memory[eff_addr:eff_addr+4] = val.to_bytes(4, 'big')
    
    rs_num = state.get_register_number(base_reg)
    rt_num = state.get_register_number(rt)
    state.instruction_info[state.pc]['binary'] = encode_i_type(0x2B, rs_num, rt_num, offset)
    
def handle_j(state, inst):
    """Simula a instrução J (Jump): PC = target_address"""
    pc_before_exec = state.pc
    label = inst['label']
    target_pc = state.labels[label]
    state.pc = target_pc # Altera o fluxo de execução para o endereço da label.
    state.instruction_info[pc_before_exec]['binary'] = encode_j_type(0x02, target_pc * 4)

def handle_jal(state, inst):
    """Simula a instrução JAL (Jump And Link): $ra = PC+4; PC = target_address"""
    pc_before_exec = state.pc
    label = inst['label']
    # Salva o endereço da instrução *seguinte* no registrador de retorno ($ra)
    state.set_register_value('$ra', (pc_before_exec + 1) * 4)
    target_pc = state.labels[label]
    state.pc = target_pc # Salta para o endereço da função
    state.instruction_info[pc_before_exec]['binary'] = encode_j_type(0x03, target_pc * 4)

def handle_jr(state, inst):
    """Simula a instrução JR (Jump Register): PC = value(rs)"""
    pc_before_exec = state.pc
    rs = inst['rs']
    target_addr = state.get_register_value(rs)
    target_pc = target_addr // 4 # Converte endereço de byte para índice de instrução.
    state.pc = target_pc # Salta para o endereço contido no registrador (geralmente $ra)
    rs_num = state.get_register_number(rs)
    state.instruction_info[pc_before_exec]['binary'] = encode_r_type(0x08, 0, 0, rs_num, 0)

def handle_syscall(state, inst):
    """Simula uma chamada de sistema (interação com o 'sistema operacional')."""
    v0 = state.get_register_value('$v0')
    output = ""
    if v0 == 1: # Código para imprimir inteiro
        a0 = state.get_register_value('$a0')
        output = str(a0)
    elif v0 == 4: # Código para imprimir string
        addr = state.get_register_value('$a0')
        end = state.memory.find(b'\0', addr) # Encontra o final da string
        output = state.memory[addr:end].decode()
    elif v0 == 10: # Código para finalizar o programa
        state.pc = len(state.instructions)
    
    # Armazena a saída da syscall para ser exibida na GUI.
    state.instruction_info[state.pc]['output'] = output
    state.instruction_info[state.pc]['binary'] = encode_r_type(0x0C, 0, 0, 0, 0)
    
# --- Handlers de Pseudo-Instruções ---
# Estas não são instruções reais da máquina, mas o assembler as traduz
# Nosso simulador as trata diretamente para simplificar.

def handle_la(state, inst):
    """Simula a pseudo-instrução LA (Load Address): rt = address_of_label"""
    rt, label = inst['rt'], inst['label']
    addr = state.data_labels[label]
    state.set_register_value(rt, addr)
    rt_num = state.get_register_number(rt)
    # la é geralmente traduzida para lui e ori. Simplificamos para uma representação.
    state.instruction_info[state.pc]['binary'] = encode_i_type(0x0D, 0, rt_num, addr)

def handle_li(state, inst):
    """Simula a pseudo-instrução LI (Load Immediate): rt = immediate"""
    rt, imm = inst['rt'], inst['imm']
    state.set_register_value(rt, imm)
    # li pode ser traduzida de várias formas. Usamos uma representação com addi.
    rt_num = state.get_register_number(rt)
    state.instruction_info[state.pc]['binary'] = encode_i_type(0x08, 0, rt_num, imm)


# Dicionário que mapeia o opcode (string) para a função Python que o executa.
INSTRUCTION_HANDLERS = {
    'add': handle_add, 'addi': handle_addi, 'sub': handle_sub, 'mult': handle_mult,
    'and': handle_and, 'or': handle_or, 'sll': handle_sll,
    'slt': handle_slt, 'slti': handle_slti,
    'lui': handle_lui, 'lw': handle_lw, 'sw': handle_sw,
    'j': handle_j, 'jal': handle_jal,
    'jr': handle_jr,
    'syscall': handle_syscall,
    # Pseudo-instruções
    'la': handle_la, 'li': handle_li
}