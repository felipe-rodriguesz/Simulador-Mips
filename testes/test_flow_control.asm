# Testa o controle de fluxo com j, jal e syscall
.data
msg_main:   .asciiz "Na main.\n"
msg_func:   .asciiz "Dentro da funcao.\n"
msg_exit:   .asciiz "Saindo."

.text
main:
    # Imprime que está em main
    li $v0, 4
    la $a0, msg_main
    syscall

    # Chama a função
    jal my_function
    
    # Após o retorno da função, prepara para sair
    li $v0, 4
    la $a0, msg_exit
    syscall
    
    # Encerra o programa
    li $v0, 10
    syscall
    
    # Esta parte não deve ser alcançada
    li $v0, 1
    li $a0, 999
    syscall

my_function:
    # Imprime que está na função
    li $v0, 4
    la $a0, msg_func
    syscall
    
    # Retorna para o chamador
    jr $ra