# Organização e fluxo interno

O código está separado em módulos pequenos, cada um responsável por uma etapa
do simulador:

| Módulo | Responsabilidade |
| --- | --- |
| `src/main.py` | Valida o argumento, cria o estado, carrega o programa e inicia a interface. |
| `src/parser.py` | Lê `.data` e `.text`, registra labels, dados e instruções. |
| `src/mips_state.py` | Mantém registradores, memória, labels, instruções e PC. |
| `src/simulator.py` | Busca a instrução apontada pelo PC, chama seu handler e avança o PC. |
| `src/instruction_set.py` | Implementa os efeitos das instruções e suas representações codificadas. |
| `src/instruction_encoder.py` | Monta campos dos formatos R, I e J em uma palavra de 32 bits. |
| `src/gui.py` | Exibe o estado e conecta os controles visuais à execução. |

## Caminho de um programa

1. `main.py` recebe o caminho do arquivo `.asm` pela linha de comando.
2. `Parser` percorre o arquivo e preenche o objeto `MIPSState`. Dados e labels
   são armazenados durante a leitura; cada instrução da seção `.text` vira um
   dicionário de opcode e operandos.
3. `Simulator` consulta a instrução no índice atual do PC e procura seu handler
   em `INSTRUCTION_HANDLERS`.
4. O handler atualiza registradores, memória ou PC e guarda a representação
   binária destinada à interface.
5. A GUI atualiza os painéis após cada passo. O modo de execução completa
   agenda repetidamente os mesmos passos no loop de eventos GTK.

Labels de código apontam para índices da lista de instruções. Endereços de
memória são índices em uma área de 4096 bytes; dados `.word` e operações `lw` e
`sw` usam quatro bytes em big-endian. Os detalhes do subconjunto e das
simplificações estão descritos no [README](../README.md#o-que-é-simulado).
