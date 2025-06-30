import re

class Parser:
    """
    Responsável por ler um arquivo de código Assembly MIPS (.asm) e traduzi-lo
    para uma estrutura de dados que o simulador possa entender e executar
    """
    def __init__(self, mips_state):
        self.state = mips_state
        self.current_section = None # Controla se estamos na seção .data ou .text
        self.data_address = 0     # Ponteiro para o próximo endereço livre na memória de dados

    def load_program(self, filepath):
        """Abre e processa o arquivo .asm linha por linha"""
        with open(filepath, 'r') as f:
            for line in f:
                # Etapa de limpeza: Remove comentários (#) e espaços em branco desnecessários
                line = line.split('#', 1)[0].strip()

                # Se a linha ficou vazia após a limpeza, ignora e vai para a próxima
                if not line:
                    continue
                
                # Detecta as diretivas de seção para saber como processar as linhas seguintes
                if line == '.data':
                    self.current_section = 'data'
                    continue
                elif line == '.text':
                    self.current_section = 'text'
                    continue
                
                # Encaminha a linha para a função de processamento correta baseada na seção atual
                if self.current_section == 'data':
                    self.parse_data_line(line)
                elif self.current_section == 'text':
                    self.parse_text_line(line)

    def parse_data_line(self, line):
        """Processa uma linha da seção .data (declaração de variáveis)"""
        # Separa a label (ex: 'my_message') do resto da linha (ex: '.asciiz "Hello"')
        parts = re.split(r':\s*', line, 1)
        label = parts[0]
        
        # Separa a diretiva (ex: '.word') do valor (ex: '42')
        directive_part = parts[1].strip()
        directive, value = re.split(r'\s+', directive_part, 1)

        # Garante o alinhamento de dados para a diretiva .word.
        # Words (4 bytes) devem começar em endereços de memória múltiplos de 4
        if directive == '.word':
            while self.data_address % 4 != 0:
                self.data_address += 1 # Adiciona bytes de preenchimento (padding)

        # Armazena o endereço da label para que instruções como `la` possam encontrá-lo
        self.state.data_labels[label] = self.data_address

        # Processa cada tipo de diretiva de dados
        if directive == '.word':
            values = [int(v.strip()) for v in value.split(',')]
            for val in values:
                # Converte o número para 4 bytes (Big Endian) e armazena na memória
                self.state.memory[self.data_address:self.data_address+4] = val.to_bytes(4, 'big')
                self.data_address += 4
        elif directive == '.asciiz':
            string = value.strip('"')
            encoded_string = string.encode('utf-8')
            # Copia os bytes da string para a memória e avança o ponteiro
            self.state.memory[self.data_address:self.data_address + len(encoded_string)] = encoded_string
            self.data_address += len(encoded_string)
            # Adiciona o caractere nulo (0x00) no final, como exige o .asciiz
            self.state.memory[self.data_address] = 0
            self.data_address += 1

    def parse_text_line(self, line):
        """Processa uma linha da seção .text (instruções de máquina)"""
        # Se a linha contém ':', é uma label de código (alvo de um salto)
        if ':' in line:
            label, instruction_part = line.split(':', 1)
            # Armazena o nome da label e o índice da instrução atual
            self.state.labels[label.strip()] = len(self.state.instructions)
            line = instruction_part.strip()

        if not line: return # Ignora linhas que continham apenas uma label

        # Separa o opcode (ex: 'add') dos operandos (ex: '$t0, $t1, $t2')
        parts = re.split(r'[\s,]+', line, 1)
        opcode = parts[0].lower()
        
        operands_str = parts[1] if len(parts) > 1 else ""
        operands = [op.strip() for op in operands_str.split(',')]
        
        # Cria um dicionário para representar a instrução e seus operandos
        instruction = {'opcode': opcode}

        # Analisa os operandos com base no formato esperado para cada instrução
        if opcode in ['add', 'sub', 'mult', 'and', 'or', 'slt']:
            instruction.update({'rd': operands[0], 'rs': operands[1], 'rt': operands[2]})
        elif opcode in ['addi', 'slti']:
            instruction.update({'rt': operands[0], 'rs': operands[1], 'imm': int(operands[2])})
        elif opcode in ['sll']:
            instruction.update({'rd': operands[0], 'rt': operands[1], 'shamt': int(operands[2])})
        elif opcode in ['lw', 'sw']:
            instruction.update({'rt': operands[0], 'operand2': operands[1]})
        elif opcode in ['lui']:
            instruction.update({'rt': operands[0], 'imm': int(operands[1], 0)})
        elif opcode in ['la', 'li']:
            instruction.update({'rt': operands[0], 'label' if opcode == 'la' else 'imm': (operands[1]) if opcode == 'la' else int(operands[1])})
        elif opcode in ['j', 'jal']:
            instruction.update({'label': operands[0]})
        elif opcode == 'jr':
            instruction.update({'rs': operands[0]})
        elif opcode == 'syscall':
            pass # Syscall não tem operandos visíveis no assembly
        
        # Adiciona a instrução processada à lista de instruções do programa
        self.state.instructions.append(instruction)