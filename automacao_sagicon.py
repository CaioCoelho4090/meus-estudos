import customtkinter as ctk
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
        # Vai para a página de protocolos, insere os dados da empresa, profissional e ocorrência
        page.locator('xpath=/html/body/header/nav/a').click()
        page.locator('xpath=//*[@id="j_idt56:j_idt60"]/div[4]/h3').click()
        page.locator('xpath=//*[@id="j_idt56:j_idt60_3"]/ul/li[2]/a').click()
        page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt1781"]').click()
        page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt1801:j_idt1807"]').click()
        # page.fill('xpath=//*[@id="formCadastrarProtocolo:codigoOcorrencia"]', "925") - Atualizar
        # page.fill('xpath=//*[@id="formCadastrarProtocolo:codigoFiscalPesq"]', "3445") - Atualizar
        page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt174"]').click()
        page.fill('xpath=//*[@id="formPesquisaProfissional:value1T"]', "4138")
        page.locator('xpath=//*[@id="formPesquisaProfissional:j_idt2054"]').click()
        page.locator('xpath=//*[@id="formPesquisaProfissional:j_idt2056"]').click()
        # Insere os dados em "Dados da Firma"
        page.locator('xpath=//*[@id="formCadastrarProtocolo"]/div[1]/div[3]/ul/li[4]/a').click()
        page.locator('xpath=//*[@id="formCadastrarProtocolo:panelTabDadosFirmas"]/div/div/ul/li[4]/a').click()
        page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt1354"]').click()
        page.locator('xpath=//*[@id="formCadastrarProtocolo:divRespTec"]/div[1]/div[1]/div[4]/div[1]/select').select_option(value="1")
        page.fill('xpath=//*[@id="formCadastrarProtocolo:j_idt1120_input"]', "28052024")
        page.locator('xpath=//*[@id="formCadastrarProtocolo:divRespTec"]/div[1]/div[1]/div[4]/div[3]/div[1]/select').select_option(value="1")
        page.locator('xpath=//*[@id="formCadastrarProtocolo:divRespTec"]/div[1]/div[1]/div[4]/div[3]/div[2]/select').select_option(value="1")
        page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt1186"]').click()
        page.fill('xpath=//*[@id="formCadastrarProtocolo:modal-horarios-contratoIn"]', '0100')
        page.fill('xpath=//*[@id="formCadastrarProtocolo:modal-horarios-contratoOut"]', '0700')
        page.locator('xpath=//*[@id="formCadastrarProtocolo:modal-horarios-contratoIncluir"]').click()
        #page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt1783"]').click()
        time.sleep(5)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    