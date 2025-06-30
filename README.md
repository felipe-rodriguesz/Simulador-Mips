# MIPS Simulator em Python

Este é um simulador para um subconjunto da arquitetura MIPS de 32 bits, desenvolvido em Python com uma interface gráfica GTK3.

## Pré-requisitos

Certifique-se de ter o Python 3 e o GTK3 instalados, juntamente com as bibliotecas de introspecção GObject para Python.

### Instalando Dependências

-   **Ubuntu/Debian**:
    ```bash
    sudo apt update
    sudo apt install -y python3 python3-gi gir1.2-gtk-3.0
    ```
-   **Fedora**:
    ```bash
    sudo dnf install -y python3-gobject gtk3
    ```
-   **Arch Linux**:
    ```bash
    sudo pacman -Syu python-gobject gtk3
    ```
-   **Windows**:
    A instalação pode ser mais complexa. É recomendado usar o MSYS2:
    ```bash
    pacman -S mingw-w64-x86_64-gtk3 mingw-w64-x86_64-python3-gobject
    ```

## Como Executar

1.  **Clone o repositório** ou baixe os arquivos para uma pasta local.

2.  **Navegue até o diretório do projeto** e execute o simulador, passando um arquivo de teste como argumento:
    ```bash
    python3 src/main.py testes/test_memory.asm
    ```
    Você pode substituir `test_memory.asm` por `test_arithmetic.asm` ou `test_flow_control.asm` para testar diferentes funcionalidades.

## Funcionalidades

A interface gráfica permite:
-   **Visualizar Registradores**: O painel esquerdo mostra o valor de todos os 32 registradores em tempo real.
-   **Acompanhar a Execução**: O painel superior direito lista cada instrução à medida que é executada.
-   **Ver Código Binário**: O código binário da última instrução executada é exibido.
-   **Saída do Programa**: A saída de chamadas de sistema (como impressão de textos e números) aparece no painel inferior direito.
-   **Controle de Execução**:
    -   `Próxima Instrução`: Executa o programa passo a passo.
    -   `Executar Tudo`: Executa o restante do programa automaticamente.
    -   `Sair`: Fecha o simulador.
