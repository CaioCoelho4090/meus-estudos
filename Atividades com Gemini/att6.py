def calcular_media(lista):
    if len(lista) == 0:
        return 0
    else:
        quantidade = len(lista)
        soma = sum(lista)
        media = soma / quantidade
        return media
    
lista = [10,20,4,6,8]
print(f"A média é {calcular_media(lista)}")