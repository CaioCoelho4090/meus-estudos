def encontrar_extremos(lista):
    maior = max(lista)
    menor = min(lista)
    return maior, menor

numeros = [5, 29, 1, 87, 4, 33]
maior, menor = encontrar_extremos(numeros)
print(maior, menor)