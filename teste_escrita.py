import os

# A mesma pasta que deu o erro
pasta_teste = r"C:\DownloadsPython\arquivos_compactados"

# Garante que a pasta exista
os.makedirs(pasta_teste, exist_ok=True)

# O caminho completo para um arquivo de teste
caminho_arquivo_teste = os.path.join(pasta_teste, "teste.txt")

try:
    print(f"Tentando escrever um arquivo em: {caminho_arquivo_teste}")
    with open(caminho_arquivo_teste, "w") as f:
        f.write("Olá, mundo!")
    
    print("✅ Sucesso! O arquivo foi escrito sem problemas.")
    # Se chegou aqui, o problema PODE ser específico do Playwright/Chromium

except Exception as e:
    print(f"❌ Falhou! Erro recebido: {e}")
    # Se der o mesmo erro de "Permission denied", o problema é 100% o antivírus/Windows.