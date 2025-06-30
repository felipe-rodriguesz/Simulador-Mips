from instruction_set import INSTRUCTION_HANDLERS

class Simulator:
    def __init__(self, mips_state):
        self.state = mips_state

    def execute_instruction(self):
        """
        Executa uma única instrução baseada no PC atual
        """
        # Verifica se o PC ultrapassou o final do programa
        if self.state.pc >= len(self.state.instructions):
            return None # Retorna None para sinalizar o fim da execução

        # --- Etapa de FETCH ---
        # Busca a instrução a ser executada usando o PC
        pc_before_exec = self.state.pc
        instruction = self.state.instructions[pc_before_exec]
        opcode = instruction['opcode']

        # --- Etapa de DECODE & EXECUTE ---
        # Busca o handler (função) correspondente ao opcode no dicionário
        handler = INSTRUCTION_HANDLERS.get(opcode)
        if handler:
            # Se encontrou, executa a função, passando o estado atual
            handler(self.state, instruction)
        else:
            raise ValueError(f"Instrução não suportada: {opcode}")

        # --- Atualização do PC ---
        # Se o PC não foi alterado por uma instrução de salto (j, jal, jr),
        # avança para a próxima instrução sequencial
        if self.state.pc == pc_before_exec:
            self.state.pc += 1
            
        # Retorna o PC da instrução que foi executada, para a GUI saber o que exibir
        return pc_before_exec