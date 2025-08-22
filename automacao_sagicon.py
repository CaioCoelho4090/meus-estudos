import customtkinter as ctk
from playwright.sync_api import sync_playwright, TimeoutError
import shutil
import os
import time

def obter_dados_protocolo():
    """
    Cria e exibe uma interface gráfica dinâmica que ajusta os campos visíveis
    com base no tipo de ocorrência selecionado.
    """
    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('blue')
    
    dados_inseridos = {}
    
    app = ctk.CTk()
    app.title("Dados para Automação de Protocolo")
    app.geometry('700x700') # Ajustado para a nova dinâmica

    # --- DICIONÁRIO DE MAPEAMENTO ---
    # Mapeia o texto que o usuário vê para o código que o sistema usa.
    ocorrencias_map = {
        "Responsabilidade Técnica": "925",
        "Alteração de Assistência Farmacêutica": "142",
        "Alteração de Horário de Funcionamento": "106",
        "Baixa de Responsabilidade Técnica": "162"
    }

    # --- FUNÇÕES DE LÓGICA ---

    def atualizar_campos(selecao):
        """
        Esta função é chamada sempre que o ComboBox de Ocorrência muda.
        Ela esconde todos os campos condicionais e depois exibe apenas os necessários.
        """
        # 1. Esconde todos os campos que podem ser opcionais
        label_inscricao_profissional.grid_forget()
        entry_inscricao_profissional.grid_forget()
        label_data_rescisao.grid_forget()
        entry_data_rescisao.grid_forget()
        label_data_contratual.grid_forget()
        entry_data_contratual.grid_forget()
        label_tipo_profissional.grid_forget()
        combo_tipo_profissional.grid_forget()
        label_tipo_contrato.grid_forget()
        combo_tipo_contrato.grid_forget()
        label_meio_contrato.grid_forget()
        combo_meio_contrato.grid_forget()
        label_tem_intervalo.grid_forget()
        switch_tem_intervalo.grid_forget()
        label_horarios1.grid_forget()
        frame_horario1.grid_forget()
        label_horarios2.grid_forget()
        frame_horario2.grid_forget()
        label_horario_funcionamento.grid_forget()
        frame_funcionamento.grid_forget()

        # 2. Exibe os campos baseados na seleção
        if selecao == "Responsabilidade Técnica":
            label_inscricao_profissional.grid(row=6, column=0, padx=10, pady=5, sticky="w")
            entry_inscricao_profissional.grid(row=6, column=1, padx=10, pady=5, sticky="ew")
            label_data_contratual.grid(row=9, column=0, padx=10, pady=5, sticky="w")
            entry_data_contratual.grid(row=9, column=1, padx=10, pady=5, sticky="ew")
            label_tipo_profissional.grid(row=10, column=0, padx=10, pady=5, sticky="w")
            combo_tipo_profissional.grid(row=10, column=1, padx=10, pady=5, sticky="ew")
            label_tipo_contrato.grid(row=11, column=0, padx=10, pady=5, sticky="w")
            combo_tipo_contrato.grid(row=11, column=1, padx=10, pady=5, sticky="ew")
            label_meio_contrato.grid(row=12, column=0, padx=10, pady=5, sticky="w")
            combo_meio_contrato.grid(row=12, column=1, padx=10, pady=5, sticky="ew")
            label_tem_intervalo.grid(row=14, column=0, padx=10, pady=10, sticky="w")
            switch_tem_intervalo.grid(row=14, column=1, padx=10, pady=10, sticky="w")
            label_horarios1.grid(row=15, column=0, padx=10, pady=5, sticky="w")
            frame_horario1.grid(row=15, column=1, padx=10, pady=5, sticky="ew")
            label_horarios2.grid(row=16, column=0, padx=10, pady=5, sticky="w")
            frame_horario2.grid(row=16, column=1, padx=10, pady=5, sticky="ew")

        elif selecao == "Alteração de Assistência Farmacêutica":
            label_inscricao_profissional.grid(row=6, column=0, padx=10, pady=5, sticky="w")
            entry_inscricao_profissional.grid(row=6, column=1, padx=10, pady=5, sticky="ew")
            label_tem_intervalo.grid(row=14, column=0, padx=10, pady=10, sticky="w")
            switch_tem_intervalo.grid(row=14, column=1, padx=10, pady=10, sticky="w")
            label_horarios1.grid(row=15, column=0, padx=10, pady=5, sticky="w")
            frame_horario1.grid(row=15, column=1, padx=10, pady=5, sticky="ew")
            label_horarios2.grid(row=16, column=0, padx=10, pady=5, sticky="w")
            frame_horario2.grid(row=16, column=1, padx=10, pady=5, sticky="ew")

        elif selecao == "Alteração de Horário de Funcionamento":
            label_horario_funcionamento.grid(row=17, column=0, padx=10, pady=5, sticky="w")
            frame_funcionamento.grid(row=17, column=1, padx=10, pady=5, sticky="ew")

        elif selecao == "Baixa de Responsabilidade Técnica":
            label_inscricao_profissional.grid(row=6, column=0, padx=10, pady=5, sticky="w")
            entry_inscricao_profissional.grid(row=6, column=1, padx=10, pady=5, sticky="ew")
            label_data_rescisao.grid(row=8, column=0, padx=10, pady=5, sticky="w")
            entry_data_rescisao.grid(row=8, column=1, padx=10, pady=5, sticky="ew")


    def ao_clicar_iniciar():
        selecao_atual = combo_ocorrencia.get()
        
        # Dados comuns a quase todos
        dados_inseridos["usuario_login"] = entry_usuario_login.get()
        dados_inseridos["senha_login"] = entry_senha_login.get()
        dados_inseridos["ocorrencia"] = ocorrencias_map[selecao_atual] # Pega o CÓDIGO, não o texto

        # Coleta os dados de forma condicional
        if selecao_atual in ["Responsabilidade Técnica", "Alteração de Assistência Farmacêutica", "Alteração de Horário de Funcionamento", "Baixa de Responsabilidade Técnica"]:
            dados_inseridos["inscricao_firma"] = entry_inscricao_firma.get()

        if selecao_atual in ["Responsabilidade Técnica", "Alteração de Assistência Farmacêutica", "Baixa de Responsabilidade Técnica"]:
            dados_inseridos["inscricao_profissional"] = entry_inscricao_profissional.get()
        
        if selecao_atual == "Responsabilidade Técnica":
            dados_inseridos["data_contratual"] = entry_data_contratual.get()
            dados_inseridos["tipo_profissional"] = combo_tipo_profissional.get()
            dados_inseridos["tipo_contrato"] = combo_tipo_contrato.get()
            dados_inseridos["meio_contrato"] = combo_meio_contrato.get()

        if selecao_atual == "Baixa de Responsabilidade Técnica":
            dados_inseridos["data_rescisao"] = entry_data_rescisao.get()

        if selecao_atual in ["Responsabilidade Técnica", "Alteração de Assistência Farmacêutica"]:
            tem_intervalo_valor = switch_tem_intervalo.get()
            dados_inseridos["tem_intervalo"] = "Sim" if tem_intervalo_valor == 1 else "Não"
            dados_inseridos["horarios_entrada"] = entry_horarios_entrada.get()
            dados_inseridos["horarios_saida"] = entry_horarios_saida.get()
            dados_inseridos["horarios_entrada2"] = entry_horarios_entrada2.get()
            dados_inseridos["horarios_saida2"] = entry_horarios_saida2.get()
        
        if selecao_atual == "Alteração de Horário de Funcionamento":
            dados_inseridos["horario_funcionamento_abertura"] = entry_horario_funcionamento_abertura.get()
            dados_inseridos["horario_funcionamento_fechamento"] = entry_horario_funcionamento_fechamento.get()
        
        app.destroy()

    # --- LAYOUT PRINCIPAL ---
    scrollable_frame = ctk.CTkScrollableFrame(app, label_text="Preencha os dados para o protocolo")
    scrollable_frame.pack(fill="both", expand=True, padx=15, pady=15)
    scrollable_frame.grid_columnconfigure(1, weight=1)

    # --- WIDGETS ---
    # Seção de Acesso (Sempre visível)
    ctk.CTkLabel(scrollable_frame, text="1. Acesso ao Sistema", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")
    ctk.CTkLabel(scrollable_frame, text='Usuário:').grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_usuario_login = ctk.CTkEntry(scrollable_frame, placeholder_text="Seu nome de usuário")
    entry_usuario_login.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
    ctk.CTkLabel(scrollable_frame, text="Senha:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_senha_login = ctk.CTkEntry(scrollable_frame, placeholder_text="Sua senha", show="*")
    entry_senha_login.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
    
    # Seção de Dados (Parte dinâmica)
    ctk.CTkLabel(scrollable_frame, text="2. Dados do Protocolo", font=ctk.CTkFont(weight="bold")).grid(row=3, column=0, columnspan=2, pady=(20, 10), sticky="w")
    
    # Ocorrência (O controle principal)
    ctk.CTkLabel(scrollable_frame, text="Ocorrência:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    combo_ocorrencia = ctk.CTkComboBox(scrollable_frame, values=list(ocorrencias_map.keys()), command=atualizar_campos)
    combo_ocorrencia.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

    # Campos que são comuns mas podem ser escondidos/mostrados
    ctk.CTkLabel(scrollable_frame, text="Inscrição da Firma:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
    entry_inscricao_firma = ctk.CTkEntry(scrollable_frame)
    entry_inscricao_firma.grid(row=5, column=1, padx=10, pady=5, sticky="ew")
    
    # --- AQUI CRIAMOS TODOS OS WIDGETS CONDICIONAIS ---
    # Eles serão gerenciados pela função atualizar_campos()
    label_inscricao_profissional = ctk.CTkLabel(scrollable_frame, text="Inscrição do Profissional:")
    entry_inscricao_profissional = ctk.CTkEntry(scrollable_frame)
    label_data_rescisao = ctk.CTkLabel(scrollable_frame, text="Data de Rescisão:")
    entry_data_rescisao = ctk.CTkEntry(scrollable_frame, placeholder_text="dd/mm/aaaa")
    label_data_contratual = ctk.CTkLabel(scrollable_frame, text="Data do Contrato:")
    entry_data_contratual = ctk.CTkEntry(scrollable_frame, placeholder_text="dd/mm/aaaa")
    label_tipo_profissional = ctk.CTkLabel(scrollable_frame, text='Tipo de Profissional:')
    combo_tipo_profissional = ctk.CTkComboBox(scrollable_frame, values=["Assistente Técnico", "Diretor Técnico", "Substituto"])
    label_tipo_contrato = ctk.CTkLabel(scrollable_frame, text='Tipo de Vínculo:')
    combo_tipo_contrato = ctk.CTkComboBox(scrollable_frame, values=["Contratado", "Servidor Público", "Sócio", "Proprietário"])
    label_meio_contrato = ctk.CTkLabel(scrollable_frame, text='Meio Contratual:')
    combo_meio_contrato = ctk.CTkComboBox(scrollable_frame, values=["CTPS", "Contrato de Prestação de Serviço", "Outros"])
    label_tem_intervalo = ctk.CTkLabel(scrollable_frame, text="Possui intervalo de almoço?")
    switch_tem_intervalo = ctk.CTkSwitch(scrollable_frame, text="Não/Sim", onvalue=1, offvalue=0)
    label_horarios1 = ctk.CTkLabel(scrollable_frame, text="Entrada 1 / Saída 1:")
    frame_horario1 = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
    entry_horarios_entrada = ctk.CTkEntry(frame_horario1, placeholder_text="HH:MM")
    entry_horarios_entrada.pack(side="left", expand=True, fill="x", padx=(0, 5))
    entry_horarios_saida = ctk.CTkEntry(frame_horario1, placeholder_text="HH:MM")
    entry_horarios_saida.pack(side="left", expand=True, fill="x", padx=(5, 0))
    label_horarios2 = ctk.CTkLabel(scrollable_frame, text="Entrada 2 / Saída 2 (pós-intervalo):")
    frame_horario2 = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
    entry_horarios_entrada2 = ctk.CTkEntry(frame_horario2, placeholder_text="HH:MM")
    entry_horarios_entrada2.pack(side="left", expand=True, fill="x", padx=(0, 5))
    entry_horarios_saida2 = ctk.CTkEntry(frame_horario2, placeholder_text="HH:MM")
    entry_horarios_saida2.pack(side="left", expand=True, fill="x", padx=(5, 0))
    label_horario_funcionamento = ctk.CTkLabel(scrollable_frame, text="Abertura / Fechamento da Empresa:")
    frame_funcionamento = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
    entry_horario_funcionamento_abertura = ctk.CTkEntry(frame_funcionamento, placeholder_text="HH:MM")
    entry_horario_funcionamento_abertura.pack(side="left", expand=True, fill="x", padx=(0, 5))
    entry_horario_funcionamento_fechamento = ctk.CTkEntry(frame_funcionamento, placeholder_text="HH:MM")
    entry_horario_funcionamento_fechamento.pack(side="left", expand=True, fill="x", padx=(5, 0))

    # --- ESTADO INICIAL ---
    # Define uma seleção padrão e chama a função para mostrar os campos corretos ao iniciar
    combo_ocorrencia.set("Responsabilidade Técnica")
    atualizar_campos("Responsabilidade Técnica")

    # Botão de Iniciar
    button_iniciar = ctk.CTkButton(master=app, text="Iniciar Automação", command=ao_clicar_iniciar)
    button_iniciar.pack(pady=20, padx=20)
    
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
            
            # Se for uma Baixa de Responsabilidade Técnica
            if dados_protocolo["ocorrencia"] == "162":
                page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt128"]').click()
                page.locator('xpath=//*[@id="formPesquisaOcorrencia:j_idt2250"]').select_option(value='Código')
                page.locator('xpath=//*[@id="formPesquisaOcorrencia:value1N"]').fill(dados_protocolo["ocorrencia"])
                page.locator('xpath=//*[@id="formPesquisaOcorrencia:j_idt2284"]').click()
                page.locator('xpath=//*[@id="formPesquisaOcorrencia:j_idt2286"]').click()
                time.sleep(1.5)
                
                # Seleciona a empresa
                page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt151"]').click()
                page.locator('xpath=//*[@id="formPesquisaEstabelecimento:value1T"]').fill(dados_protocolo["inscricao_firma"])
                page.locator('xpath=//*[@id="formPesquisaEstabelecimento:j_idt2192"]').click()
                page.locator('xpath=//*[@id="formPesquisaEstabelecimento:j_idt2194"]').click()
                time.sleep(1.5)
                
                # Seleciona o profissional
                page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt174"]').click()
                page.locator('xpath=//*[@id="formPesquisaProfissional:value1T"]').fill(dados_protocolo["inscricao_profissional"])
                page.locator('xpath=//*[@id="formPesquisaProfissional:j_idt2054"]').click()
                page.locator('xpath=//*[@id="formPesquisaProfissional:j_idt2056"]').click()
                time.sleep(1.5)
                
                # Vai para "Dados da Firma"
                page.locator('xpath=//*[@id="formCadastrarProtocolo"]/div[1]/div[3]/ul/li[4]/a').click()
                # Vai para "Responsável Técnico"
                page.locator('xpath=//*[@id="formCadastrarProtocolo:panelTabDadosFirmas"]/div/div/ul/li[4]/a').click()
                # Clica em "Carregar Contrato Profissional" e depois no ícone de editar
                page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt1357"]').click()
                page.locator('xpath=//*[@id="formCadastrarProtocolo:dataTableRTAtivo:0:j_idt1330"]').click()
                # Preenche a data de rescisao e clica em salvar
                page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt1123_input"]').fill(dados_protocolo["data_rescisao"])
                page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt1155"]').click()
            elif dados_protocolo["ocorrencia"] == "925":         # Se for uma Responsabilidade Técnica
                page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt128"]').click()
                page.locator('xpath=//*[@id="formPesquisaOcorrencia:j_idt2250"]').select_option(value='Código')
                page.locator('xpath=//*[@id="formPesquisaOcorrencia:value1N"]').fill(dados_protocolo["ocorrencia"])
                page.locator('xpath=//*[@id="formPesquisaOcorrencia:j_idt2284"]').click()
                page.locator('xpath=//*[@id="formPesquisaOcorrencia:j_idt2286"]').click()
                time.sleep(1.5)
                
                # Seleciona a empresa
                page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt151"]').click()
                page.locator('xpath=//*[@id="formPesquisaEstabelecimento:value1T"]').fill(dados_protocolo["inscricao_firma"])
                page.locator('xpath=//*[@id="formPesquisaEstabelecimento:j_idt2192"]').click()
                page.locator('xpath=//*[@id="formPesquisaEstabelecimento:j_idt2194"]').click()
                time.sleep(1.5)
                
                # Seleciona o profissional
                page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt174"]').click()
                page.locator('xpath=//*[@id="formPesquisaProfissional:value1T"]').fill(dados_protocolo["inscricao_profissional"])
                page.locator('xpath=//*[@id="formPesquisaProfissional:j_idt2054"]').click()
                page.locator('xpath=//*[@id="formPesquisaProfissional:j_idt2056"]').click()
                time.sleep(1.5)
                
                # Vai para "Dados da Firma" e depois clica em Responsável Técnico
                page.locator('xpath=//*[@id="formCadastrarProtocolo"]/div[1]/div[3]/ul/li[4]/a').click()
                page.locator('xpath=//*[@id="formCadastrarProtocolo:panelTabDadosFirmas"]/div/div/ul/li[4]/a').click()
                # Clica em "Adicionar RT"
                page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt1354"]').click()
                # Seleciona o Tipo de Profissional
                if dados_protocolo["tipo_profissional"] == "Assistente Técnico":
                    page.locator('xpath=//*[@id="formCadastrarProtocolo:divRespTec"]/div[1]/div[1]/div[4]/div[1]/select').select_option(value="A")
                elif dados_protocolo["tipo_profissional"] == "Diretor Técnico":
                    page.locator('xpath=//*[@id="formCadastrarProtocolo:divRespTec"]/div[1]/div[1]/div[4]/div[1]/select').select_option(value="N")
                elif dados_protocolo["tipo_profissional"] == "Substituto":
                    page.locator('xpath=//*[@id="formCadastrarProtocolo:divRespTec"]/div[1]/div[1]/div[4]/div[1]/select').select_option(value="S")
                else:
                    print("Tipo de profissional em branco")
                # Insere a data do contrato
                page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt1120_input"]').fill(dados_protocolo["data_contratual"])
                
                # Seleciona o tipo de contrato
                if dados_protocolo["tipo_contrato"] == "Contratado":
                    page.locator('xpath=/html/body/div[4]/aside[2]/section[2]/div[1]/form[1]/div[1]/div[3]/div/div[4]/div/div/div/div/div[4]/div/span/div[1]/div[1]/div[4]/div[3]/div[1]/select').select_option(value="C")
                elif dados_protocolo["tipo_contrato"] == "Sócio":
                    page.locator('xpath=/html/body/div[4]/aside[2]/section[2]/div[1]/form[1]/div[1]/div[3]/div/div[4]/div/div/div/div/div[4]/div/span/div[1]/div[1]/div[4]/div[3]/div[1]/select').select_option(value="S")
                elif dados_protocolo["tipo_contrato"] == "Proprietário":
                    page.locator('xpath=/html/body/div[4]/aside[2]/section[2]/div[1]/form[1]/div[1]/div[3]/div/div[4]/div/div/div/div/div[4]/div/span/div[1]/div[1]/div[4]/div[3]/div[1]/select').select_option(value="P")
                elif dados_protocolo["tipo_contrato"] == "Servidor Público":
                    page.locator('xpath=/html/body/div[4]/aside[2]/section[2]/div[1]/form[1]/div[1]/div[3]/div/div[4]/div/div/div/div/div[4]/div/span/div[1]/div[1]/div[4]/div[3]/div[1]/select').select_option(value="U")
                else:
                    print("Tipo de contrato em branco")
                    
                # Seleciona o meio contratual
                if dados_protocolo["meio_contrato"] == "CTPS":
                    page.locator('xpath=/html/body/div[4]/aside[2]/section[2]/div[1]/form[1]/div[1]/div[3]/div/div[4]/div/div/div/div/div[4]/div/span/div[1]/div[1]/div[4]/div[3]/div[2]/select').select_option(value="1")
                elif dados_protocolo["meio_contrato"] == "Contrato de Prestação de Serviço":
                    page.locator('xpath=/html/body/div[4]/aside[2]/section[2]/div[1]/form[1]/div[1]/div[3]/div/div[4]/div/div/div/div/div[4]/div/span/div[1]/div[1]/div[4]/div[3]/div[2]/select').select_option(value="2")
                elif dados_protocolo["meio_contrato"] == "Outros":
                    page.locator('xpath=/html/body/div[4]/aside[2]/section[2]/div[1]/form[1]/div[1]/div[3]/div/div[4]/div/div/div/div/div[4]/div/span/div[1]/div[1]/div[4]/div[3]/div[2]/select').select_option(value="4")
                else:
                    print("Meio contratual em branco")
                
                # Verifica se tem intervalo
                if dados_protocolo["tem_intervalo"] == "Sim":
                    # Insere os horários antes do intervalo e salva
                    page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt1186"]').click()
                    page.locator('xpath=//*[@id="formCadastrarProtocolo:modal-horarios-contratoIn"]').fill(dados_protocolo["horarios_entrada"])
                    page.locator('xpath=//*[@id="formCadastrarProtocolo:modal-horarios-contratoOut"]').fill(dados_protocolo["horarios_saida"])
                    page.locator('xpath=//*[@id="formCadastrarProtocolo:modal-horarios-contratoIncluir"]').click()
                    # Insere os horários depois do intervalo e salva
                    page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt1186"]').click()
                    page.locator('xpath=//*[@id="formCadastrarProtocolo:modal-horarios-contratoIn"]').fill(dados_protocolo["horarios_entrada2"])
                    page.locator('xpath=//*[@id="formCadastrarProtocolo:modal-horarios-contratoOut"]').fill(dados_protocolo["horarios_saida2"])
                    page.locator('xpath=//*[@id="formCadastrarProtocolo:modal-horarios-contratoIncluir"]').click()
                elif dados_protocolo["tem_intervalo"] == "Não":
                    # Insere os horários antes do intervalo e salva
                    page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt1186"]').click()
                    page.locator('xpath=//*[@id="formCadastrarProtocolo:modal-horarios-contratoIn"]').fill(dados_protocolo["horarios_entrada"])
                    page.locator('xpath=//*[@id="formCadastrarProtocolo:modal-horarios-contratoOut"]').fill(dados_protocolo["horarios_saida"])
                    page.locator('xpath=//*[@id="formCadastrarProtocolo:modal-horarios-contratoIncluir"]').click()
                else:
                    print("Algo deu errado")
                # Salva os dados contratuais e horários
                page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt1155"]').click()
            elif dados_protocolo["ocorrencia"] == "142":    # Se for uma Alteração de Assistência Farmacêutica
                # Seleciona a ocorrência
                page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt128"]').click()
                page.locator('xpath=//*[@id="formPesquisaOcorrencia:j_idt2250"]').select_option(value='Código')
                page.locator('xpath=//*[@id="formPesquisaOcorrencia:value1N"]').fill(dados_protocolo["ocorrencia"])
                page.locator('xpath=//*[@id="formPesquisaOcorrencia:j_idt2284"]').click()
                page.locator('xpath=//*[@id="formPesquisaOcorrencia:j_idt2286"]').click()
                time.sleep(1.5)
                    
                # Seleciona a empresa
                page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt151"]').click()
                page.locator('xpath=//*[@id="formPesquisaEstabelecimento:value1T"]').fill(dados_protocolo["inscricao_firma"])
                page.locator('xpath=//*[@id="formPesquisaEstabelecimento:j_idt2192"]').click()
                page.locator('xpath=//*[@id="formPesquisaEstabelecimento:j_idt2194"]').click()
                time.sleep(1.5)
                    
                # Seleciona o profissional
                page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt174"]').click()
                page.locator('xpath=//*[@id="formPesquisaProfissional:value1T"]').fill(dados_protocolo["inscricao_profissional"])
                page.locator('xpath=//*[@id="formPesquisaProfissional:j_idt2054"]').click()
                page.locator('xpath=//*[@id="formPesquisaProfissional:j_idt2056"]').click()
                time.sleep(1.5)
                
                # Vai para "Dados da Firma" e depois "Responsável Técnico"
                page.locator('xpath=//*[@id="formCadastrarProtocolo"]/div[1]/div[3]/ul/li[4]/a').click()
                page.locator('xpath=//*[@id="formCadastrarProtocolo:panelTabDadosFirmas"]/div/div/ul/li[4]/a').click()
                
                # Clica em "Carregar Contrato Profissional" e depois no ícone de editar
                page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt1357"]').click()
                page.locator('xpath=//*[@id="formCadastrarProtocolo:dataTableRTAtivo:0:j_idt1330"]').click()
                
                # Clica no ícone para remover o horário antigo e clica em sim para confirmar
                page.locator('xpath=//*[@id="formCadastrarProtocolo:tbHorarioRT:0:j_idt1184"]').click()
                page.locator('xpath=//*[@id="formmodalConfirmaDeleteHorarioRT:excluirComAction"]').click()
                
                # Verifica se tem intervalo
                if dados_protocolo["tem_intervalo"] == "Sim":
                    # Insere os horários antes do intervalo e salva
                    page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt1186"]').click()
                    page.locator('xpath=//*[@id="formCadastrarProtocolo:modal-horarios-contratoIn"]').fill(dados_protocolo["horarios_entrada"])
                    page.locator('xpath=//*[@id="formCadastrarProtocolo:modal-horarios-contratoOut"]').fill(dados_protocolo["horarios_saida"])
                    page.locator('xpath=//*[@id="formCadastrarProtocolo:modal-horarios-contratoIncluir"]').click()
                    # Insere os horários depois do intervalo e salva
                    page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt1186"]').click()
                    page.locator('xpath=//*[@id="formCadastrarProtocolo:modal-horarios-contratoIn"]').fill(dados_protocolo["horarios_entrada2"])
                    page.locator('xpath=//*[@id="formCadastrarProtocolo:modal-horarios-contratoOut"]').fill(dados_protocolo["horarios_saida2"])
                    page.locator('xpath=//*[@id="formCadastrarProtocolo:modal-horarios-contratoIncluir"]').click()
                elif dados_protocolo["tem_intervalo"] == "Não":
                    # Insere os horários antes do intervalo e salva
                    page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt1186"]').click()
                    page.locator('xpath=//*[@id="formCadastrarProtocolo:modal-horarios-contratoIn"]').fill(dados_protocolo["horarios_entrada"])
                    page.locator('xpath=//*[@id="formCadastrarProtocolo:modal-horarios-contratoOut"]').fill(dados_protocolo["horarios_saida"])
                    page.locator('xpath=//*[@id="formCadastrarProtocolo:modal-horarios-contratoIncluir"]').click()
                else:
                    print("Algo deu errado")
                # Salva os dados contratuais e horários
                page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt1155"]').click()
            elif dados_protocolo["ocorrencia"] == "106":    # Se for uma alteração de horário de funcionamento
                # Seleciona a ocorrência
                page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt128"]').click()
                page.locator('xpath=//*[@id="formPesquisaOcorrencia:j_idt2250"]').select_option(value='Código')
                page.locator('xpath=//*[@id="formPesquisaOcorrencia:value1N"]').fill(dados_protocolo["ocorrencia"])
                page.locator('xpath=//*[@id="formPesquisaOcorrencia:j_idt2284"]').click()
                page.locator('xpath=//*[@id="formPesquisaOcorrencia:j_idt2286"]').click()
                time.sleep(1.5)
                    
                # Seleciona a empresa
                page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt151"]').click()
                page.locator('xpath=//*[@id="formPesquisaEstabelecimento:value1T"]').fill(dados_protocolo["inscricao_firma"])
                page.locator('xpath=//*[@id="formPesquisaEstabelecimento:j_idt2192"]').click()
                page.locator('xpath=//*[@id="formPesquisaEstabelecimento:j_idt2194"]').click()
                time.sleep(1.5)
                
                # Vai para "Dados da Firma" e depois "Horários"
                page.locator('xpath=//*[@id="formCadastrarProtocolo"]/div[1]/div[3]/ul/li[4]/a').click()
                page.locator('xpath=/html/body/div[4]/aside[2]/section[2]/div[1]/form[1]/div[1]/div[3]/div/div[4]/div/div/div/ul/li[2]/a').click()
                
                # Clica no ícone para excluir o horário antigo e depois em sim para confirmar
                page.locator('xpath=//*[@id="formCadastrarProtocolo:tbHorarioFunc:0:j_idt827"]').click()
                page.locator('xpath=//*[@id="formmodalConfirmaDeleteHorario:excluirComAction"]').click()
                
                # Clical em adicionar horário, preenche e salva (Apenas segunda à sexta por enquanto, sem fechar para intervalo)
                page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt830"]').click()
                page.locator('xpath=//*[@id="formCadastrarProtocolo:modal-horariosIn"]').fill(dados_protocolo["horario_funcionamento_abertura"])
                page.locator('xpath=//*[@id="formCadastrarProtocolo:modal-horariosOut"]').fill(dados_protocolo["horario_funcionamento_fechamento"])
                page.locator('xpath=//*[@id="formCadastrarProtocolo:modal-horariosIncluir"]').click()
            else:
                print("Deu algum erro")
            
            time.sleep(5)
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
        finally:
            navegador.close()
            
if __name__ == '__main__':
    dados_automacao = obter_dados_protocolo()
    if dados_automacao:
        executar_automacao = inicia_a_geracao_do_protocolo(dados_automacao)