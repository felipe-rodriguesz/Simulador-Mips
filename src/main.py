import sys
from mips_state import MIPSState
from parser import Parser
from simulator import Simulator
from gui import SimulatorGUI

def main():
    """
    Função principal que serve como ponto de entrada para o simulador
    Responsável por orquestrar a inicialização e execução de todos os componentes
    """
    
    # Validação dos Argumentos da Linha de Comando
    # O programa espera exatamente um argumento: o caminho para o arquivo .asm
    # sys.argv é uma lista que contém os argumentos; sys.argv[0] é o nome do script
    if len(sys.argv) != 2:
        print(f"Uso: python {sys.argv[0]} <arquivo.asm>")
        return # Encerra o programa se o uso for incorreto

    filepath = sys.argv[1]

    # Inicialização dos Componentes Principais
    # A ordem de inicialização é importante para garantir que as dependências
    # entre os módulos sejam satisfeitas

    # Cria a instância do estado do processador, que funcionará como a "memória central" do simulador
    state = MIPSState()
    # Cria o parser, passando o objeto de estado para que ele possa preenchê-lo
    parser = Parser(state)
    
    # Carregamento e Parsing do Programa Assembly
    # O bloco try...except é usado para capturar erros que podem ocorrer durante a
    # leitura ou análise do arquivo, como um arquivo não encontrado ou um erro de sintaxe
    try:
        parser.load_program(filepath)
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filepath}' não encontrado.")
        return
    except Exception as e:
        print(f"Erro fatal ao analisar o arquivo: {e}")
        return

    # Preparação dos Dados para a Interface Gráfica
    # Este loop pré-formata o texto de cada instrução para que a GUI não precise
    # fazer esse trabalho repetidamente, melhorando a performance
    for i, inst in enumerate(state.instructions):
        state.instruction_info[i]['text'] = f"{inst['opcode']} " + ", ".join(
            str(v) for k, v in inst.items() if k != 'opcode'
        )

    # Com o estado já preenchido pelo parser, criamos as instâncias do simulador e da GUI
    simulator = Simulator(state)
    gui = SimulatorGUI(simulator)

    # Inicia a interface gráfica e o loop de eventos. O programa ficará aqui
    # até que o usuário feche a janela.
    gui.run()

# O código dentro deste 'if' só será executado se o script for chamado diretamente (ex: python main.py)
if __name__ == "__main__":
    main()