# Sección de datos
.data
.word 0x12345678   # Palabra de 32 bits en la sección de datos

# Sección de código
.text
main:             # Etiqueta de inicio
    addi x1, x0, 10   # x1 = x0 + 10
    add x2, x1, x1    # x2 = x1 + x1
    lw x3, 4(x2)      # x3 = Memoria[x2 + 4]
    sw x3, 8(x1)      # Memoria[x1 + 8] = x3
    beq x1, x2, main  # Si x1 == x2, saltar a main