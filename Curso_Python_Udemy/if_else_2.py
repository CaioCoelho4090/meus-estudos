def faixa_etaria(valor):
    idade = valor
    if idade >= 0 and idade < 18:
        return "Menor de idade"
    elif idade >= 18 and idade <= 64:
        return "Adulto"
    elif idade >= 65 and idade < 100:
        return "Melhor idade"
    elif idade >= 100:
        return "Centenário"
    else:
        return "Idade inválida"
    
idade = int(input("Digite sua idade: "))
print(faixa_etaria(idade))