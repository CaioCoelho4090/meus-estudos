produtos = [
    {"nome": "Smartphone", "preco": 1200, "categoria": "Eletrônicos"},
    {"nome": "Tênis", "preco": 300, "categoria": "Vestuário"},
    {"nome": "Notebook", "preco": 3500, "categoria": "Eletrônicos"},
    {"nome": "Camiseta", "preco": 80, "categoria": "Vestuário"},
    {"nome": "Monitor", "preco": 450, "categoria": "Eletrônicos"},
]

produtos_caros = [produto for produto in produtos if produto["categoria"] == "Eletrônicos" and produto["preco"] > 500]

print(produtos_caros) 

