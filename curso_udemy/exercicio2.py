num = input("Digite um numero inteiro: ")
try:
    eh_inteiro = int(num) % 2 == 0
    if eh_inteiro:
        print("É inteiro e é par")
    else:
        print("É inteiro e é impar")
except:
    print("Não é inteiro")