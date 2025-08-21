def verifica_conceito(valor):
    nota = float(valor)
    if nota > 9 and nota <= 10:
        return "A"
    elif nota > 8  and nota <= 9:
        return "A-"
    elif nota > 7 and nota <= 8:
        return "B"
    elif nota > 6 and nota <= 7:
        return "B-"
    elif nota > 5 and nota <= 6:
        return "C"
    elif nota > 4 and nota <= 5:
        return "C-"
    elif nota > 3 and nota <= 4:
        return "D"
    elif nota > 2 and nota <= 3:
        return "D-"
    elif nota > 1 and nota <= 2:
        return "E"
    elif nota >= 0 and nota <= 1:
        return "E-"
    else:
        return "Nota inválida"

nota = float(input("Digite sua nota: "))
print(verifica_conceito(nota))
         
