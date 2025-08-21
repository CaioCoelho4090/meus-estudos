import customtkinter as ctk
# Resolvido: Mantive a importação do TimeoutError, que é uma adição útil.
from playwright.sync_api import sync_playwright, TimeoutError
import shutil
import os
import time

# ctk.set_appearance_mode('dark')
# app = ctk.CTk()
# app.title("Gerador de protocolos automático")
# app.geometry('800x600')

with sync_playwright() as p:
    navegador = p.chromium.launch(headless=False)
    page = navegador.new_page()
    page.set_default_timeout(30000)
    try:
        # Efetua o login
        page.goto("http://sagicon.crf-to.cisantec.com.br/sagicon/login.jsf")
        page.fill('xpath=//*[@id="formLogin:j_username"]', "CAIO")
        page.fill('xpath=//*[@id="formLogin:j_password"]', "Gsacap21@")
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
        page.fill('xpath=//*[@id="formPesquisaOcorrencia:value1N"]', '925')
        page.locator('xpath=//*[@id="formPesquisaOcorrencia:j_idt2284"]').click()
        page.locator('xpath=//*[@id="formPesquisaOcorrencia:j_idt2286"]').click()
        
        # Seleciona a empresa
        page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt151"]').click()
        page.fill('xpath=//*[@id="formPesquisaEstabelecimento:value1T"]', '3445')
        page.locator('xpath=//*[@id="formPesquisaEstabelecimento:j_idt2192"]').click()
        page.locator('xpath=//*[@id="formPesquisaEstabelecimento:j_idt2194"]').click()
        
        # Seleciona o profissional
        page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt174"]').click()
        page.fill('xpath=//*[@id="formPesquisaProfissional:value1T"]', "4138")
        page.locator('xpath=//*[@id="formPesquisaProfissional:j_idt2054"]').click()
        page.locator('xpath=//*[@id="formPesquisaProfissional:j_idt2056"]').click()
        
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