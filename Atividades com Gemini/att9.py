def agrupar_por_conceito(lista):
    conceitos = {
        "A": [],
        "B": [],
        "C": [],
        "D": [],
        "F": []
    }
    
    for alunos in lista:
        nome = alunos["nome"]
        nota = alunos["nota"]
        if nota > 9:
            conceitos["A"].append(nome)
        elif nota > 8 and nota <= 9:
            conceitos["B"].append(nome)
        elif nota > 7 and nota <= 8:
            conceitos["C"].append(nome)
        elif nota >= 6 and nota <= 7:
            conceitos["D"].append(nome)
        else:
            conceitos["F"].append(nome)
    return conceitos

alunos = [
    {"nome": "Ana", "nota": 8.5},
    {"nome": "Bruno", "nota": 5.8},
    {"nome": "Carlos", "nota": 9.2},
    {"nome": "Diana", "nota": 7.6},
    {"nome": "Eduardo", "nota": 6.8},
    {"nome": "Mariana", "nota": 8.1},
]
resultado = agrupar_por_conceito(alunos)
print(resultado)