import customtkinter as ctk
from playwright.sync_api import sync_playwright, TimeoutError
import shutil
import os
import time

def obter_dados_protocolo():
    # Inicia a interface gráfica
    ctk.set_appearance_mode('dark')
    
    # Onde será salvo os dados
    dados_inseridos = {}
    
    app = ctk.CTk()
    app.title("Dados do protocolo")
    app.geometry('800x600')
    
    def ao_clicar_iniciar():
        dados_inseridos["ocorrencia"] = entry_ocorrencia.get()
        dados_inseridos["inscricao_firma"] = entry_inscricao_firma.get()
        dados_inseridos["inscricao_profissional"] = entry_inscricao_profissional.get()
        dados_inseridos["usuario_login"] = entry_usuario_login.get()
        dados_inseridos["senha_login"] = entry_senha_login.get()
        app.destroy()
    
    # Entrada do nome de usuário
    label_usuario = ctk.CTkLabel(app, text='Insira seu nome de usuário')
    label_usuario.pack(pady=(0, 5))
    entry_usuario_login = ctk.CTkEntry(app, placeholder_text="Nome de usuário")
    entry_usuario_login.pack()
    
    # Entrada da senha
    label_senha = ctk.CTkLabel(app, text="Insira sua senha")
    label_senha.pack(pady=(10, 5))
    entry_senha_login = ctk.CTkEntry(app, placeholder_text="Senha")
    entry_senha_login.pack()
    
    # Entrada do número da ocorrência
    label_ocorrencia = ctk.CTkLabel(app, text="Insira o código da ocorrência")
    label_ocorrencia.pack(pady=(10, 5))
    entry_ocorrencia = ctk.CTkEntry(app, placeholder_text="Código Ocorrência")
    entry_ocorrencia.pack()
    
    # Entrada do número de inscrição da firma
    label_inscricao_firma = ctk.CTkLabel(app, text="Insira o número de inscrição da firma")
    label_inscricao_firma.pack(pady=(10, 5))
    entry_inscricao_firma = ctk.CTkEntry(app, placeholder_text="No. Inscrição")
    entry_inscricao_firma.pack()
    
    # Entrada do número de inscrição do profissional
    label_inscricao_profissional = ctk.CTkLabel(app, text="Insira o número de inscrição do profissional")
    label_inscricao_profissional.pack(pady=(10, 5))
    entry_inscricao_profissional = ctk.CTkEntry(app, placeholder_text="No. Inscrição")
    entry_inscricao_profissional.pack()
    
    # Inicia a inserção dos dados
    button_iniciar = ctk.CTkButton(master=app, text="Iniciar automação", command=ao_clicar_iniciar)
    button_iniciar.pack(pady=10, padx=20)
    app.mainloop()
    
    return dados_inseridos

def inicia_a_geracao_do_protocolo(dados_protocolo: dict):
    # Inicia o navegador chrome
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=False)
        page = navegador.new_page()
        page.set_default_timeout(30000)
        try:
            # Efetua o login
            page.goto("http://sagicon.crf-to.cisantec.com.br/sagicon/login.jsf")
            page.locator('xpath=//*[@id="formLogin:j_username"]').fill(dados_protocolo["usuario_login"])
            page.locator('xpath=//*[@id="formLogin:j_password"]').fill(dados_protocolo["senha_login"])
            page.locator('xpath=//*[@id="formLogin:btnEntrar"]').click()
            
            # Vai para a página de protocolos
            page.locator('xpath=/html/body/header/nav/a').click()
            page.locator('xpath=//*[@id="j_idt56:j_idt60"]/div[4]/h3').click()
            page.locator('xpath=//*[@id="j_idt56:j_idt60_3"]/ul/li[2]/a').click()
            
            # Clica no botão "Inserir" e depois "FIRMA"
            page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt1781"]').click()
            page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt1801:j_idt1807"]').click()
            
            # Seleciona a ocorrência
            page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt128"]').click()
            page.locator('xpath=//*[@id="formPesquisaOcorrencia:j_idt2250"]').select_option(value='Código')
            page.locator('xpath=//*[@id="formPesquisaOcorrencia:value1N"]').fill(dados_protocolo["ocorrencia"])
            page.locator('xpath=//*[@id="formPesquisaOcorrencia:j_idt2284"]').click()
            page.locator('xpath=//*[@id="formPesquisaOcorrencia:j_idt2286"]').click()
            time.sleep(3.5)
            
            # Seleciona a empresa
            page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt151"]').click()
            page.locator('xpath=//*[@id="formPesquisaEstabelecimento:value1T"]').fill(dados_protocolo["inscricao_firma"])
            page.locator('xpath=//*[@id="formPesquisaEstabelecimento:j_idt2192"]').click()
            page.locator('xpath=//*[@id="formPesquisaEstabelecimento:j_idt2194"]').click()
            time.sleep(3.5)
            
            # Seleciona o profissional
            page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt174"]').click()
            page.locator('xpath=//*[@id="formPesquisaProfissional:value1T"]').fill(dados_protocolo["inscricao_profissional"])
            page.locator('xpath=//*[@id="formPesquisaProfissional:j_idt2054"]').click()
            page.locator('xpath=//*[@id="formPesquisaProfissional:j_idt2056"]').click()
            time.sleep(3.5)
            
            # Vai para "Dados da Firma"
            page.locator('xpath=//*[@id="formCadastrarProtocolo"]/div[1]/div[3]/ul/li[4]/a').click()
            
            # Vai para "Responsável Técnico"
            page.locator('xpath=//*[@id="formCadastrarProtocolo:panelTabDadosFirmas"]/div/div/ul/li[4]/a').click()
            
            # Clica em "Adicionar RT"
            page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt1354"]').click()
            
            # Seleciona "Assistente Técnico"
            page.locator('xpath=//*[@id="formCadastrarProtocolo:divRespTec"]/div[1]/div[1]/div[4]/div[1]/select').select_option(value="A")
            
            # Insere a data do contrato
            page.fill('xpath=//*[@id="formCadastrarProtocolo:j_idt1120_input"]', "28052024")
            
            # Seleciona "Contratado"
            page.locator('xpath=//*[@id="formCadastrarProtocolo:divRespTec"]/div[1]/div[1]/div[4]/div[3]/div[1]/select').select_option(value="C")
            
            # Seleciona "CTPS"
            page.locator('xpath=//*[@id="formCadastrarProtocolo:divRespTec"]/div[1]/div[1]/div[4]/div[3]/div[2]/select').select_option(value="1")
            
            # Clica em "Adicionar Horário" e preenche os campos
            page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt1186"]').click()
            page.fill('xpath=//*[@id="formCadastrarProtocolo:modal-horarios-contratoIn"]', '0100')
            page.fill('xpath=//*[@id="formCadastrarProtocolo:modal-horarios-contratoOut"]', '0700')
            
            # Clica em "Incluir"
            page.locator('xpath=//*[@id="formCadastrarProtocolo:modal-horarios-contratoIncluir"]').click()
            
            # Salva os dados do contrato
            page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt1155"]').click()
            
            time.sleep(5)
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
        finally:
            navegador.close()
            
if __name__ == '__main__':
    dados_automacao = obter_dados_protocolo()
    if dados_automacao:
        executar_automacao = inicia_a_geracao_do_protocolo(dados_automacao)