def inverter_string(palavra):
    texto_invertido = palavra[::-1]
    return texto_invertido

palavra = input("Digite uma palavra: ")
print(inverter_string(palavra))