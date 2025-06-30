import collections

# Constantes Globais da Arquitetura MIPS Simulada
NUM_REGISTERS = 32
MEMORY_SIZE = 4096
MAX_INSTRUCTIONS = 100

# Nomes dos registradores MIPS
REGISTER_NAMES = [
    "$zero", "$at", "$v0", "$v1", "$a0", "$a1", "$a2", "$a3",
    "$t0", "$t1", "$t2", "$t3", "$t4", "$t5", "$t6", "$t7",
    "$s0", "$s1", "$s2", "$s3", "$s4", "$s5", "$s6", "$s7",
    "$t8", "$t9", "$k0", "$k1", "$gp", "$sp", "$fp", "$ra"
]

# Cria um dicionário para mapear o nome de um registrador ao seu número (índice)
# Ex: REGISTER_MAP['$t0'] retornará 8
REGISTER_MAP = {name: i for i, name in enumerate(REGISTER_NAMES)}

class MIPSState:
    """
    Representa o estado completo do processador MIPS em um dado momento
    Funciona como o "hardware" virtual, contendo os registradores, a memória e o PC
    """
    def __init__(self):
        # Array para simular os 32 registradores MIPS, todos inicializados com 0
        self.registers = [0] * NUM_REGISTERS
        # Array de bytes para simular a memória principal, inicializada com 0
        self.memory = bytearray(MEMORY_SIZE)
        # Dicionário para mapear labels de código (ex: 'main', 'loop') para seus endereços de instrução
        self.labels = {}
        # Dicionário para mapear labels de dados (ex: 'my_message') para seus endereços na memória
        self.data_labels = {}
        # Lista onde as instruções do programa serão armazenadas após o parsing
        self.instructions = []
        # Contador de Programa, armazena o índice da próxima instrução a ser executada
        self.pc = 0

        # Dicionário especial para guardar informações extras sobre cada instrução para a GUI,
        # como o texto formatado, o código binário e a saída de syscalls
        # defaultdict(dict) cria um dicionário vazio para qualquer chave que ainda não exista
        self.instruction_info = collections.defaultdict(dict)

    def get_register_number(self, reg_name):
        """Retorna o número de um registrador a partir do seu nome"""
        return REGISTER_MAP.get(reg_name, -1)

    def get_register_value(self, reg_name_or_num):
        """Retorna o valor de um registrador a partir do nome ou número"""
        if isinstance(reg_name_or_num, str):
            reg_num = self.get_register_number(reg_name_or_num)
        else:
            reg_num = reg_name_or_num
        
        if 0 <= reg_num < NUM_REGISTERS:
            return self.registers[reg_num]
        raise ValueError(f"Registrador inválido: {reg_name_or_num}")

    def set_register_value(self, reg_name_or_num, value):
        """Define o valor de um registrador, garantindo que seja um inteiro de 32 bits"""
        if isinstance(reg_name_or_num, str):
            reg_num = self.get_register_number(reg_name_or_num)
        else:
            reg_num = reg_name_or_num

        if reg_num == 0: # Registrador $zero é sempre 0
            return

        if 0 < reg_num < NUM_REGISTERS:
            # A máscara `& 0xFFFFFFFF` garante que o valor seja truncado para 32 bits
            self.registers[reg_num] = value & 0xFFFFFFFF
        else:
            raise ValueError(f"Registrador inválido: {reg_name_or_num}")