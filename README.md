# Simulador MIPS em Python

Simulador didático de um subconjunto da arquitetura MIPS de 32 bits. Ele lê um
arquivo Assembly simplificado, representa o estado do processador e permite
acompanhar a execução instrução por instrução em uma interface gráfica GTK 3.
O projeto foi desenvolvido para demonstrar conceitos básicos de arquitetura de
computadores; não é um assembler nem um emulador MIPS completo.

## O que é simulado

- 32 registradores nomeados conforme o MIPS, com valores armazenados em 32 bits
  e `$zero` mantido em zero.
- Contador de programa (PC), representado internamente pelo índice da instrução.
- Memória de 4 KiB, organizada como bytes; palavras são lidas e gravadas em
  big-endian e devem estar alinhadas a quatro bytes.
- Labels de código e de dados, desvios e chamadas/retornos simples.
- Codificação de 32 bits exibida para a instrução executada. No caso das
  pseudo-instruções, essa codificação é uma representação simplificada, não a
  expansão real feita por um assembler.

### Instruções aceitas

O parser reconhece as seguintes instruções:

| Grupo | Instruções |
| --- | --- |
| Aritmética e lógica | `add`, `addi`, `sub`, `mult`, `and`, `or` |
| Deslocamento e comparação | `sll`, `slt`, `slti` |
| Memória e constantes | `lui`, `lw`, `sw` |
| Fluxo de execução | `j`, `jal`, `jr` |
| Pseudo-instruções | `la`, `li` |
| Chamada de sistema | `syscall` |

`mult` grava o produto diretamente em um registrador de destino. Isso simplifica
o comportamento MIPS, que normalmente usa os registradores especiais HI e LO.
`la` e `li` também são tratadas diretamente, sem expansão para instruções
reais.

O parser entende as seções `.data` e `.text`; na seção de dados aceita `.word`
e `.asciiz`. As syscalls implementadas são: código `1` para imprimir o inteiro
em `$a0`, código `4` para imprimir a string terminada em nulo apontada por `$a0`
e código `10` para encerrar a execução.

### Limites conhecidos

Este projeto cobre somente os itens listados acima. Não implementa o conjunto
completo MIPS, assembler externo, pipeline, exceções, entrada interativa,
syscalls adicionais ou interface de depuração reversa. A sintaxe do parser é
restrita: por exemplo, operações aritméticas esperam registradores nomeados e
`lw`/`sw` esperam operandos no formato `offset($registrador)`. Entradas fora do
formato esperado podem causar erro durante a análise ou execução.

## Interface e execução

A janela GTK apresenta os 32 registradores com valores hexadecimal e decimal,
uma lista das instruções já executadas, a representação binária da última
instrução e a saída produzida por syscalls de impressão. **Próxima Instrução**
avança uma instrução; **Executar Tudo** agenda a execução sequencial até o
programa terminar; **Sair** fecha a janela. Saltos alteram a sequência normal.

O PC mostrado na lista é o índice da instrução no programa, começando em zero,
e não um endereço de byte. A execução termina ao alcançar o fim do programa ou
ao executar a syscall de código 10.

## Conceitos de arquitetura demonstrados

- Estado de processador: registradores, memória e contador de programa.
- Ciclo simplificado de busca, decodificação e execução de instruções.
- Operações aritméticas, lógicas, deslocamentos e comparações entre registradores.
- Acesso à memória por endereço efetivo, alinhamento e representação big-endian.
- Mudanças no fluxo de controle por saltos, chamada e retorno.
- Convenção simples de syscall para saída de dados e encerramento.
- Campos de codificação dos formatos R, I e J, exibidos como demonstração.

Para detalhes sobre a organização dos módulos e o fluxo interno, consulte
[Arquitetura do projeto](docs/arquitetura.md).

## Stack e dependências

- **Python 3** para parser, estado, codificação e execução.
- **GTK 3** e **PyGObject** (`gi`) para a interface gráfica.
- Bibliotecas padrão Python, incluindo `re` e `collections`.

Não há dependências Python declaradas em `requirements.txt` ou configuração de
gerenciador de pacotes. GTK 3 e PyGObject são dependências do sistema e devem
estar disponíveis no ambiente Python usado para iniciar o programa.

## Instalação e execução

Em Debian ou Ubuntu, instale Python 3, GTK 3 e os bindings PyGObject:

```bash
sudo apt update
sudo apt install python3 python3-gi gir1.2-gtk-3.0
```

Clone ou baixe o repositório, entre na pasta do projeto e execute um dos
exemplos:

```bash
python3 src/main.py testes/test_arithmetic.asm
```

Outros exemplos disponíveis:

```bash
python3 src/main.py testes/test_memory.asm
python3 src/main.py testes/test_flow_control.asm
```

É necessário iniciar o programa em um ambiente gráfico com GTK 3 acessível ao
Python. A interface é iniciada com um arquivo `.asm` como argumento.

## Exemplos incluídos

- `testes/test_arithmetic.asm`: operações aritméticas, lógicas, deslocamento,
  comparação e encerramento.
- `testes/test_memory.asm`: dados `.asciiz` e `.word`, acesso `lw`/`sw` e saída
  por syscall.
- `testes/test_flow_control.asm`: labels, `jal`, `jr`, syscalls de impressão e
  retorno de uma rotina.

Os arquivos em `testes/` são programas de exemplo para execução manual; não são
uma suíte automatizada de testes Python.
