from collections import Counter

with open('artigo.txt', 'r', encoding='utf-8') as arquivo:
    texto = arquivo.read()

texto_processado = texto.lower()
pontuacoes = '.,;:!?()[]'
for p in pontuacoes:
    texto_processado = texto_processado.replace(p, '')

lista_de_palavras = texto_processado.split()

frequencia_de_palavras = Counter(lista_de_palavras)
mais_frequentes = frequencia_de_palavras.most_common(10)
for palavra, contagem in mais_frequentes:
    print(f"{palavra}: {contagem} vezes")

