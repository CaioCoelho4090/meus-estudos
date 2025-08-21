faturamento_por_produto = {}

with open("vendas.txt", "r", encoding='utf-8') as arquivo:
    for linha in arquivo:
        linha_limpa = linha.strip()
        
        linha_separada = linha_limpa.split(',')
        produto = linha_separada[0]
        quantidade = int(linha_separada[1])
        preco_unitario = float(linha_separada[2])
        
        faturamento = quantidade * preco_unitario
        
        if produto in faturamento_por_produto:
            faturamento_por_produto[produto] += faturamento
        else:
            faturamento_por_produto[produto] = faturamento

print("Faturamento por produto:")
for produto, faturamento_total in faturamento_por_produto.items():
    print(f"- {produto}: R$ {faturamento_total:.2f}")