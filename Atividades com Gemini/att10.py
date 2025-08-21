def eh_palindromo(frase):
    formatado = frase.lower()
    pontuacoes = ' .,;:!?()[]'
    for p in pontuacoes:
        formatado = formatado.replace(p, '')
    
    if formatado == formatado[::-1]:
        return True
    else:
        return False
    
frase = "Anotaram a data da maratona"
print(eh_palindromo(frase))
    