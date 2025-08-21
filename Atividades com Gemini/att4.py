def soma_pares(numeros):
    pares = [numero for numero in numeros if numero % 2 == 0]
    return sum(pares)

lista = [10,2,3,1,9,24,16,7]
print(soma_pares(lista))