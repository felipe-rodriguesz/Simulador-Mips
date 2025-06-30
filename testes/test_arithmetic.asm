# Testa instruções lógicas e aritméticas
.data
.text
main:
    addi $t0, $zero, 10      # $t0 = 10
    addi $t1, $zero, 5       # $t1 = 5
    
    add  $t2, $t0, $t1       # $t2 = 10 + 5 = 15
    sub  $t3, $t0, $t1       # $t3 = 10 - 5 = 5
    
    lui  $t4, 0x1001         # $t4 = 0x10010000
    or   $t5, $t4, $t2       # $t5 = 0x1001000F
    and  $s0, $t0, $t1       # $s0 = 10 & 5 = 0
    
    sll  $s1, $t1, 2         # $s1 = 5 << 2 = 20
    
    slt  $s2, $t0, $t1       # $s2 = (10 < 5) ? 1 : 0 -> 0
    slti $s3, $t1, 100       # $s3 = (5 < 100) ? 1 : 0 -> 1

    # Fim do programa
    li $v0, 10
    syscall