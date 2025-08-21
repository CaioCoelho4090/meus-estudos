num = int(input("Digite um numero inteiro: "))
tabuada = 0
for n in range(10):
    tabuada += 1
    resultado = num * tabuada
    print(f"{num} x {tabuada} = {resultado}")
    