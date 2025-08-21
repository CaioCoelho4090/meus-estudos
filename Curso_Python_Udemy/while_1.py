from random import *

numero_informado = 0
numero_secreto = randint(0, 9)

while numero_informado != numero_secreto:
    numero_informado = int(input("digite um numero entre 1 e 10: "))

print(f"O numero secreto {numero_secreto} foi encontrado")
