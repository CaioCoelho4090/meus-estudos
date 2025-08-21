from playwright.sync_api import sync_playwright
import time
import shutil
import os

pasta_origem = r'C:\Users\caio4\OneDrive\Documents\ArquivosProtocolos'
pasta_destino = 'C:/DownloadsPython/arquivos_compactados/'
pasta_comprimidos = 'C:/Users/caio4/OneDrive/Documents/ArquivosProtocolos/arquivos_compactados/'

os.makedirs(pasta_destino, exist_ok=True)
os.makedirs(pasta_comprimidos, exist_ok=True)

with sync_playwright() as p:
    navegador = p.chromium.launch(headless=False)
    page = navegador.new_page()
    
    arquivos_na_pasta = os.listdir(pasta_origem)
    
    for nome_do_arquivo in arquivos_na_pasta:
        caminho_origem_completo = os.path.join(pasta_origem, nome_do_arquivo)
        
        if not os.path.isfile(caminho_origem_completo) or not nome_do_arquivo.lower().endswith('.pdf'):
            continue
        
        try:
            page.goto("https://www.ilovepdf.com/pt/comprimir_pdf", timeout=60000)
            with page.expect_file_chooser() as fc_info:
                page.locator('xpath=//*[@id="pickfiles"]').click()
                file_chooser = fc_info.value
                file_chooser.set_files(caminho_origem_completo)
                
            page.locator('xpath=//*[@id="processTask"]').click()
            time.sleep(5)
            with page.expect_download() as download_info:
                page.locator('xpath=//*[@id="pickfiles"]').click()
                
            download = download_info.value
            caminho_temporario = download.path()
            caminho_salvamento = os.path.join(pasta_destino, download.suggested_filename)
            shutil.move(caminho_temporario, caminho_salvamento)
            time.sleep(5)
        except TimeoutError:
            continue
        except Exception as e:
            print(f"❌ ERRO INESPERADO ao processar '{nome_do_arquivo}': {e}")
            continue
    