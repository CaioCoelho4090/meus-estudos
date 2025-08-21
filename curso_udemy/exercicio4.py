nome = input("Digite seu primeiro nome: ")

if len(nome) > 0 and len(nome) <= 4:
    print("Seu nome é muito curto")
elif len(nome) >= 5 and len(nome) <= 6:
    print("Seu nome é normal")
elif len(nome) > 6:
    print("Seu nome é muito grande")
else:
    print("Nome em branco")
