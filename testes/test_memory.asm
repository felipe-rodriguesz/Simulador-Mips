# Testa acesso à memória e pseudo-instruções
.data
my_message: .asciiz "Valor carregado: "
my_value:   .word   42
result_str: .asciiz "\nResultado salvo na memoria."

.text
main:
    # Carrega endereço da mensagem em $a0
    la $a0, my_message
    li $v0, 4
    syscall         # Imprime "Valor carregado: "

    # Carrega valor da memória
    la $t0, my_value
    lw $a0, 0($t0)  # Carrega o valor 42 em $a0
    
    li $v0, 1
    syscall         # Imprime 42
    
    # Salva um novo valor na memória
    addi $t1, $zero, 99
    sw $t1, 0($t0)  # Salva 99 no endereço de my_value
    
    # Imprime mensagem de confirmação
    la $a0, result_str
    li $v0, 4
    syscall
    
    # Fim
    li $v0, 10
    syscall