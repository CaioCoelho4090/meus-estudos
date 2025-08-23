import customtkinter as ctk
from playwright.sync_api import sync_playwright, TimeoutError
import shutil
import os
import time

def obter_dados_protocolo():
    """
    Cria e exibe uma interface gráfica dinâmica que ajusta os campos visíveis,
    incluindo checkboxes para os dias da semana, com base na ocorrência.
    """
    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('blue')
    
    dados_inseridos = {}
    
    app = ctk.CTk()
    app.title("Dados para Automação de Protocolo")
    app.geometry('750x750')

    ocorrencias_map = {
        "Responsabilidade Técnica": "925",
        "Alteração de Assistência Farmacêutica": "142",
        "Alteração de Horário de Funcionamento": "106",
        "Baixa de Responsabilidade Técnica": "162"
    }
    
    DIAS_SEMANA = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

    # --- FUNÇÕES AUXILIARES PARA OS BOTÕES DE SELEÇÃO RÁPIDA ---
    def selecionar_dias(checkbox_dict, dias_para_selecionar):
        """Função genérica para marcar/desmarcar checkboxes."""
        for dia, checkbox in checkbox_dict.items():
            if dia in dias_para_selecionar:
                checkbox.select()
            else:
                checkbox.deselect()

    # Funções para o grupo "Assistência Técnica"
    def sel_assist_seg_sex(): selecionar_dias(checkboxes_assistencia, DIAS_SEMANA[0:5])
    def sel_assist_sab_dom(): selecionar_dias(checkboxes_assistencia, ["Sábado", "Domingo"])
    def sel_assist_sab(): selecionar_dias(checkboxes_assistencia, ["Sábado"])
    def sel_assist_dom(): selecionar_dias(checkboxes_assistencia, ["Domingo"])

    # Funções para o grupo "Horário de Funcionamento"
    def sel_func_todos(): selecionar_dias(checkboxes_funcionamento, DIAS_SEMANA)
    def sel_func_seg_sab(): selecionar_dias(checkboxes_funcionamento, DIAS_SEMANA[0:6])
    def sel_func_seg_sex(): selecionar_dias(checkboxes_funcionamento, DIAS_SEMANA[0:5])


    # --- FUNÇÕES DE LÓGICA PRINCIPAL ---
    def atualizar_campos(selecao):
        """Esconde/mostra campos baseados na seleção da Ocorrência."""
        # 1. Esconde todos os campos condicionais (código existente)
        # ... (este bloco continua exatamente o mesmo) ...
        label_inscricao_profissional.grid_forget(); entry_inscricao_profissional.grid_forget()
        label_data_rescisao.grid_forget(); entry_data_rescisao.grid_forget()
        label_data_contratual.grid_forget(); entry_data_contratual.grid_forget()
        label_tipo_profissional.grid_forget(); combo_tipo_profissional.grid_forget()
        label_tipo_contrato.grid_forget(); combo_tipo_contrato.grid_forget()
        label_meio_contrato.grid_forget(); combo_meio_contrato.grid_forget()
        label_tem_intervalo.grid_forget(); switch_tem_intervalo.grid_forget()
        label_horarios1.grid_forget(); frame_horario1.grid_forget()
        label_horarios2.grid_forget(); frame_horario2.grid_forget()
        label_horario_funcionamento.grid_forget(); frame_funcionamento.grid_forget()
        frame_dias_assistencia.grid_forget()
        frame_dias_funcionamento.grid_forget()
        
         # ### NOVO: Esconde os campos de Horário de Funcionamento ###
        label_tem_intervalo_func.grid_forget(); switch_tem_intervalo_func.grid_forget()
        label_horario_funcionamento1.grid_forget(); frame_funcionamento1.grid_forget()
        label_horario_funcionamento2.grid_forget(); frame_funcionamento2.grid_forget()
        frame_dias_funcionamento.grid_forget()


        # 2. Exibe os campos baseados na seleção
        if selecao == "Responsabilidade Técnica" or selecao == "Alteração de Assistência Farmacêutica":
            # ... (Lógica para RT e Assistência Farmacêutica continua a mesma) ...
            label_inscricao_profissional.grid(row=6, column=0, **grid_args_label); entry_inscricao_profissional.grid(row=6, column=1, **grid_args_entry)
            if selecao == "Responsabilidade Técnica":
                label_data_contratual.grid(row=9, column=0, **grid_args_label); entry_data_contratual.grid(row=9, column=1, **grid_args_entry)
                label_tipo_profissional.grid(row=10, column=0, **grid_args_label); combo_tipo_profissional.grid(row=10, column=1, **grid_args_entry)
                label_tipo_contrato.grid(row=11, column=0, **grid_args_label); combo_tipo_contrato.grid(row=11, column=1, **grid_args_entry)
                label_meio_contrato.grid(row=12, column=0, **grid_args_label); combo_meio_contrato.grid(row=12, column=1, **grid_args_entry)
            
            # Mostra os campos de horário para ambos
            label_tem_intervalo.grid(row=14, column=0, **grid_args_label_check); switch_tem_intervalo.grid(row=14, column=1, **grid_args_check)
            label_horarios1.grid(row=15, column=0, **grid_args_label); frame_horario1.grid(row=15, column=1, **grid_args_entry)
            label_horarios2.grid(row=16, column=0, **grid_args_label); frame_horario2.grid(row=16, column=1, **grid_args_entry)
            frame_dias_assistencia.grid(row=17, column=0, columnspan=2, pady=(15, 5), sticky="ew")

        elif selecao == "Alteração de Horário de Funcionamento":
            # ### ALTERAÇÃO: Mostra os novos widgets dedicados ###
            label_tem_intervalo_func.grid(row=18, column=0, **grid_args_label_check)
            switch_tem_intervalo_func.grid(row=18, column=1, **grid_args_check)
            label_horario_funcionamento1.grid(row=19, column=0, **grid_args_label)
            frame_funcionamento1.grid(row=19, column=1, **grid_args_entry)
            label_horario_funcionamento2.grid(row=20, column=0, **grid_args_label)
            frame_funcionamento2.grid(row=20, column=1, **grid_args_entry)
            frame_dias_funcionamento.grid(row=21, column=0, columnspan=2, pady=(15, 5), sticky="ew")

        elif selecao == "Baixa de Responsabilidade Técnica":
            # ... (Lógica para Baixa de RT continua a mesma) ...
            label_inscricao_profissional.grid(row=6, column=0, **grid_args_label); entry_inscricao_profissional.grid(row=6, column=1, **grid_args_entry)
            label_data_rescisao.grid(row=8, column=0, **grid_args_label); entry_data_rescisao.grid(row=8, column=1, **grid_args_entry)

    def ao_clicar_iniciar():
        selecao_atual = combo_ocorrencia.get()
        # ... (Coleta de dados comuns continua a mesma) ...
        dados_inseridos["usuario_login"] = entry_usuario_login.get()
        dados_inseridos["senha_login"] = entry_senha_login.get()
        dados_inseridos["ocorrencia"] = ocorrencias_map[selecao_atual]

        # Coleta de dados condicional
        # ... (aqui fica um pouco mais complexo, vamos refatorar) ...

        # ### ALTERAÇÃO NA COLETA DE DADOS ###
        
        # Campos que dependem da seleção, mas não são de horário
        if selecao_atual != "Alteração de Horário de Funcionamento":
            dados_inseridos["inscricao_profissional"] = entry_inscricao_profissional.get()
        if selecao_atual == "Responsabilidade Técnica":
            dados_inseridos["data_contratual"] = entry_data_contratual.get()
            dados_inseridos["tipo_profissional"] = combo_tipo_profissional.get()
            dados_inseridos["tipo_contrato"] = combo_tipo_contrato.get()
            dados_inseridos["meio_contrato"] = combo_meio_contrato.get()
        if selecao_atual == "Baixa de Responsabilidade Técnica":
            dados_inseridos["data_rescisao"] = entry_data_rescisao.get()
        
        # Campos de horário (agora para 3 tipos de ocorrência)
        if selecao_atual in ["Responsabilidade Técnica", "Alteração de Assistência Farmacêutica", "Alteração de Horário de Funcionamento"]:
            dados_inseridos["inscricao_firma"] = entry_inscricao_firma.get()
            tem_intervalo_valor = switch_tem_intervalo.get()
            dados_inseridos["tem_intervalo"] = "Sim" if tem_intervalo_valor == 1 else "Não"
            dados_inseridos["horarios_entrada"] = entry_horarios_entrada.get()
            dados_inseridos["horarios_saida"] = entry_horarios_saida.get()
            dados_inseridos["horarios_entrada2"] = entry_horarios_entrada2.get()
            dados_inseridos["horarios_saida2"] = entry_horarios_saida2.get()
        
        # Coleta dos dias da semana
        if selecao_atual in ["Responsabilidade Técnica", "Alteração de Assistência Farmacêutica"]:
            dias_selecionados = [dia for dia, checkbox in checkboxes_assistencia.items() if checkbox.get() == 1]
            dados_inseridos["dias_assistencia"] = dias_selecionados
        if selecao_atual == "Alteração de Horário de Funcionamento":
            dias_selecionados = [dia for dia, checkbox in checkboxes_funcionamento.items() if checkbox.get() == 1]
            dados_inseridos["dias_funcionamento"] = dias_selecionados
        
        # ### NOVO: Bloco de coleta de dados dedicado para Horário de Funcionamento ###
        if selecao_atual == "Alteração de Horário de Funcionamento":
            tem_intervalo_valor_func = switch_tem_intervalo_func.get()
            dados_inseridos["tem_intervalo_funcionamento"] = "Sim" if tem_intervalo_valor_func == 1 else "Não"
            dados_inseridos["horario_funcionamento_abertura"] = entry_horario_funcionamento_abertura.get()
            dados_inseridos["horario_funcionamento_fechamento"] = entry_horario_funcionamento_fechamento.get()
            # Coleta os horários 2 apenas se houver intervalo
            if tem_intervalo_valor_func == 1:
                dados_inseridos["horario_funcionamento_abertura2"] = entry_horario_funcionamento_abertura2.get()
                dados_inseridos["horario_funcionamento_fechamento2"] = entry_horario_funcionamento_fechamento2.get()
            
            dias_selecionados = [dia for dia, checkbox in checkboxes_funcionamento.items() if checkbox.get() == 1]
            dados_inseridos["dias_funcionamento"] = dias_selecionados
        
        app.destroy()
    
    # --- LAYOUT E WIDGETS ---
    scrollable_frame = ctk.CTkScrollableFrame(app, label_text="Preencha os dados para o protocolo")
    scrollable_frame.pack(fill="both", expand=True, padx=15, pady=15)
    scrollable_frame.grid_columnconfigure(1, weight=1)

    grid_args_label = {"padx": 10, "pady": 5, "sticky": "w"}
    grid_args_entry = {"padx": 10, "pady": 5, "sticky": "ew"}
    grid_args_check = {"padx": 10, "pady": 10, "sticky": "w"}
    grid_args_label_check = {"padx": 10, "pady": 10, "sticky": "w"}

    # Widgets fixos
    ctk.CTkLabel(scrollable_frame, text="1. Acesso ao Sistema", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")
    ctk.CTkLabel(scrollable_frame, text='Usuário:').grid(row=1, column=0, **grid_args_label); entry_usuario_login = ctk.CTkEntry(scrollable_frame, placeholder_text="Seu nome de usuário"); entry_usuario_login.grid(row=1, column=1, **grid_args_entry)
    ctk.CTkLabel(scrollable_frame, text="Senha:").grid(row=2, column=0, **grid_args_label); entry_senha_login = ctk.CTkEntry(scrollable_frame, placeholder_text="Sua senha", show="*"); entry_senha_login.grid(row=2, column=1, **grid_args_entry)
    ctk.CTkLabel(scrollable_frame, text="2. Dados do Protocolo", font=ctk.CTkFont(weight="bold")).grid(row=3, column=0, columnspan=2, pady=(20, 10), sticky="w")
    ctk.CTkLabel(scrollable_frame, text="Ocorrência:").grid(row=4, column=0, **grid_args_label); combo_ocorrencia = ctk.CTkComboBox(scrollable_frame, values=list(ocorrencias_map.keys()), command=atualizar_campos); combo_ocorrencia.grid(row=4, column=1, **grid_args_entry)
    ctk.CTkLabel(scrollable_frame, text="Inscrição da Firma:").grid(row=5, column=0, **grid_args_label); entry_inscricao_firma = ctk.CTkEntry(scrollable_frame); entry_inscricao_firma.grid(row=5, column=1, **grid_args_entry)
    
    # Widgets condicionais
    label_inscricao_profissional = ctk.CTkLabel(scrollable_frame, text="Inscrição do Profissional:"); entry_inscricao_profissional = ctk.CTkEntry(scrollable_frame)
    label_data_rescisao = ctk.CTkLabel(scrollable_frame, text="Data de Rescisão:"); entry_data_rescisao = ctk.CTkEntry(scrollable_frame, placeholder_text="dd/mm/aaaa")
    label_data_contratual = ctk.CTkLabel(scrollable_frame, text="Data do Contrato:"); entry_data_contratual = ctk.CTkEntry(scrollable_frame, placeholder_text="dd/mm/aaaa")
    label_tipo_profissional = ctk.CTkLabel(scrollable_frame, text='Tipo de Profissional:'); combo_tipo_profissional = ctk.CTkComboBox(scrollable_frame, values=["Assistente Técnico", "Diretor Técnico", "Substituto"])
    label_tipo_contrato = ctk.CTkLabel(scrollable_frame, text='Tipo de Vínculo:'); combo_tipo_contrato = ctk.CTkComboBox(scrollable_frame, values=["Contratado", "Servidor Público", "Sócio", "Proprietário"])
    label_meio_contrato = ctk.CTkLabel(scrollable_frame, text='Meio Contratual:'); combo_meio_contrato = ctk.CTkComboBox(scrollable_frame, values=["CTPS", "Contrato de Prestação de Serviço", "Outros"])
    label_tem_intervalo = ctk.CTkLabel(scrollable_frame, text="Possui intervalo de almoço?"); switch_tem_intervalo = ctk.CTkSwitch(scrollable_frame, text="Não/Sim", onvalue=1, offvalue=0)
    label_horarios1 = ctk.CTkLabel(scrollable_frame, text="Entrada 1 / Saída 1:"); frame_horario1 = ctk.CTkFrame(scrollable_frame, fg_color="transparent"); entry_horarios_entrada = ctk.CTkEntry(frame_horario1, placeholder_text="HH:MM"); entry_horarios_entrada.pack(side="left", expand=True, fill="x", padx=(0, 5)); entry_horarios_saida = ctk.CTkEntry(frame_horario1, placeholder_text="HH:MM"); entry_horarios_saida.pack(side="left", expand=True, fill="x", padx=(5, 0))
    label_horarios2 = ctk.CTkLabel(scrollable_frame, text="Entrada 2 / Saída 2 (pós-intervalo):"); frame_horario2 = ctk.CTkFrame(scrollable_frame, fg_color="transparent"); entry_horarios_entrada2 = ctk.CTkEntry(frame_horario2, placeholder_text="HH:MM"); entry_horarios_entrada2.pack(side="left", expand=True, fill="x", padx=(0, 5)); entry_horarios_saida2 = ctk.CTkEntry(frame_horario2, placeholder_text="HH:MM"); entry_horarios_saida2.pack(side="left", expand=True, fill="x", padx=(5, 0))
    label_horario_funcionamento = ctk.CTkLabel(scrollable_frame, text="Abertura / Fechamento da Empresa:"); frame_funcionamento = ctk.CTkFrame(scrollable_frame, fg_color="transparent"); entry_horario_funcionamento_abertura = ctk.CTkEntry(frame_funcionamento, placeholder_text="HH:MM"); entry_horario_funcionamento_abertura.pack(side="left", expand=True, fill="x", padx=(0, 5)); entry_horario_funcionamento_fechamento = ctk.CTkEntry(frame_funcionamento, placeholder_text="HH:MM"); entry_horario_funcionamento_fechamento.pack(side="left", expand=True, fill="x", padx=(5, 0))
    
    # ### NOVO: Criação dos widgets dedicados para Horário de Funcionamento ###
    # Eles serão criados mas ficarão escondidos até serem necessários.
    label_tem_intervalo_func = ctk.CTkLabel(scrollable_frame, text="Funcionamento possui intervalo?")
    switch_tem_intervalo_func = ctk.CTkSwitch(scrollable_frame, text="Não/Sim", onvalue=1, offvalue=0)
    
    label_horario_funcionamento1 = ctk.CTkLabel(scrollable_frame, text="Abertura 1 / Fechamento 1:")
    frame_funcionamento1 = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
    entry_horario_funcionamento_abertura = ctk.CTkEntry(frame_funcionamento1, placeholder_text="HH:MM")
    entry_horario_funcionamento_abertura.pack(side="left", expand=True, fill="x", padx=(0, 5))
    entry_horario_funcionamento_fechamento = ctk.CTkEntry(frame_funcionamento1, placeholder_text="HH:MM")
    entry_horario_funcionamento_fechamento.pack(side="left", expand=True, fill="x", padx=(5, 0))

    label_horario_funcionamento2 = ctk.CTkLabel(scrollable_frame, text="Abertura 2 / Fechamento 2:")
    frame_funcionamento2 = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
    entry_horario_funcionamento_abertura2 = ctk.CTkEntry(frame_funcionamento2, placeholder_text="HH:MM")
    entry_horario_funcionamento_abertura2.pack(side="left", expand=True, fill="x", padx=(0, 5))
    entry_horario_funcionamento_fechamento2 = ctk.CTkEntry(frame_funcionamento2, placeholder_text="HH:MM")
    entry_horario_funcionamento_fechamento2.pack(side="left", expand=True, fill="x", padx=(5, 0))

    # ### ALTERAÇÃO AQUI: Frame de Dias de Assistência agora usa .grid() ###
    frame_dias_assistencia = ctk.CTkFrame(scrollable_frame)
    ctk.CTkLabel(frame_dias_assistencia, text="Dias da Assistência:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=4, sticky="w", padx=10, pady=(10,5))
    checkboxes_assistencia = {dia: ctk.CTkCheckBox(frame_dias_assistencia, text=dia) for dia in DIAS_SEMANA}
    for i, checkbox in enumerate(checkboxes_assistencia.values()):
        # Organiza em 2 linhas: 4 na primeira, 3 na segunda
        row = i // 4 + 1  # +1 para pular a linha do título
        col = i % 4
        checkbox.grid(row=row, column=col, padx=10, pady=5, sticky="w")
    frame_botoes_assist = ctk.CTkFrame(frame_dias_assistencia, fg_color="transparent")
    frame_botoes_assist.grid(row=3, column=0, columnspan=4, pady=(5,10))
    ctk.CTkButton(frame_botoes_assist, text="Seg-Sex", width=80, command=sel_assist_seg_sex).pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes_assist, text="Sáb-Dom", width=80, command=sel_assist_sab_dom).pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes_assist, text="Sábado", width=80, command=sel_assist_sab).pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes_assist, text="Domingo", width=80, command=sel_assist_dom).pack(side="left", padx=5)

    # ### ALTERAÇÃO AQUI: Frame de Dias de Funcionamento agora usa .grid() ###
    frame_dias_funcionamento = ctk.CTkFrame(scrollable_frame)
    ctk.CTkLabel(frame_dias_funcionamento, text="Dias de Funcionamento:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, columnspan=4, sticky="w", padx=10, pady=(10,5))
    checkboxes_funcionamento = {dia: ctk.CTkCheckBox(frame_dias_funcionamento, text=dia) for dia in DIAS_SEMANA}
    for i, checkbox in enumerate(checkboxes_funcionamento.values()):
        row = i // 4 + 1
        col = i % 4
        checkbox.grid(row=row, column=col, padx=10, pady=5, sticky="w")
    frame_botoes_func = ctk.CTkFrame(frame_dias_funcionamento, fg_color="transparent")
    frame_botoes_func.grid(row=3, column=0, columnspan=4, pady=(5,10))
    ctk.CTkButton(frame_botoes_func, text="Todos", width=100, command=sel_func_todos).pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes_func, text="Seg-Sáb", width=100, command=sel_func_seg_sab).pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes_func, text="Seg-Sex", width=100, command=sel_func_seg_sex).pack(side="left", padx=5)
    
    # --- ESTADO INICIAL ---
    combo_ocorrencia.set("Responsabilidade Técnica")
    atualizar_campos("Responsabilidade Técnica")

    button_iniciar = ctk.CTkButton(master=app, text="Iniciar Automação", command=ao_clicar_iniciar)
    button_iniciar.pack(pady=20, padx=20)
    
    app.mainloop()
    return dados_inseridos

def inicia_a_geracao_do_protocolo(dados_protocolo: dict):
    # Inicia o navegador chrome
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=False, args=['--start-maximized'])
        contexto = navegador.new_context(no_viewport=True)
        page = contexto.new_page()
        page.set_default_timeout(30000)
        
        try:
            # Define os seletores de login como variáveis
            SELETOR_INPUT_USERNAME = r'#formLogin\:j_username'
            SELETOR_INPUT_PASSWORD = r'#formLogin\:j_password'
            SELETOR_BOTAO_LOGIN = r'#formLogin\:btnEntrar'
            
            # Define os seletores do caminho para Dados da Firma e Responsável Técnico e Adicionar RT
            XPATH_DADOS_FIRMA = r'//*[@id="formCadastrarProtocolo"]/div[1]/div[3]/ul/li[4]/a'
            XPATH_RESPONSAVEL_TECNICO = r'//*[@id="formCadastrarProtocolo:panelTabDadosFirmas"]/div/div/ul/li[4]/a'
            SELETOR_ADICIONAR_RT = r'#formCadastrarProtocolo\:j_idt1354'
            SELETOR_DATA_CONTRATO = r'#formCadastrarProtocolo\:j_idt1120_input'
            SELETOR_BOTAO_SALVAR_DADOS_CONTRATUAIS = r'#formCadastrarProtocolo\:j_idt1155'
            SELETOR_BOTAO_CARREGAR_CONTRATO = r'#formCadastrarProtocolo\:j_idt1357'
            SELETOR_ICONE_EDITAR = r'#formCadastrarProtocolo\:dataTableRTAtivo\:0\:j_idt1330'
            SELETOR_ICONE_EXCLUIR_HORARIO = r'#formCadastrarProtocolo\:tbHorarioRT\:0\:j_idt1184'
            SELETOR_BOTAO_CONFIRMAR_EXCLUSAO = r'#formmodalConfirmaDeleteHorarioRT\:excluirComAction'
            XPATH_BOTAO_HORARIOS = R'//*[@id="formCadastrarProtocolo:panelTabDadosFirmas"]/div/div/ul/li[2]/a'
            SELETOR_ICONE_EXCLUIR_HORARIO_FIRMA = r'#formCadastrarProtocolo\:tbHorarioFunc\:0\:j_idt827'
            SELETOR_CONFIRMAR_EXCLUSAO_HORARIO_FIRMA = r'#formmodalConfirmaDeleteHorario\:excluirComAction'
            
            # Efetua o login
            page.goto("http://sagicon.crf-to.cisantec.com.br/sagicon/login.jsf")
            page.locator(SELETOR_INPUT_USERNAME).fill(dados_protocolo["usuario_login"])
            page.locator(SELETOR_INPUT_PASSWORD).fill(dados_protocolo["senha_login"])
            page.locator(SELETOR_BOTAO_LOGIN).click()
            
            # Vai para a página de protocolos
            page.locator('xpath=/html/body/header/nav/a').click()
            page.locator('xpath=//*[@id="j_idt56:j_idt60"]/div[4]/h3').click()
            page.locator('xpath=//*[@id="j_idt56:j_idt60_3"]/ul/li[2]/a').click()
            
            # Clica no botão "Inserir" e depois "FIRMA"
            page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt1781"]').click()
            page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt1801:j_idt1807"]').click()
            
            # Função para selecionar a ocorrência
            def seleciona_ocorrencia(page, codigo_ocorrencia: str):
                # Define os seletores como variáveis
                BOTAO_LUPA_ABRIR_CAIXA_PESQUISA = r'#formCadastrarProtocolo\:j_idt128'
                BOTAO_SELECT_CODIGO_OCORRENCIA = r'#formPesquisaOcorrencia\:j_idt2250'
                CAIXA_INPUT_CODIGO_OCORRENCIA = r'#formPesquisaOcorrencia\:value1N'
                BOTAO_PESQUISAR_OCORRENCIA = r'#formPesquisaOcorrencia\:j_idt2284'
                BOTAO_RETORNA_PESQUISA = r'#formPesquisaOcorrencia\:j_idt2286'
                try:
                    # Clica no ícone para pesquisa da ocorrência e aguarda ficar visível
                    page.locator(BOTAO_LUPA_ABRIR_CAIXA_PESQUISA).click()
                    page.wait_for_selector(BOTAO_SELECT_CODIGO_OCORRENCIA, state="visible", timeout=10000)
                    
                    # Muda o tipo de pesquisa para Código e preenche
                    page.locator(BOTAO_SELECT_CODIGO_OCORRENCIA).select_option(value='Código')
                    page.locator(CAIXA_INPUT_CODIGO_OCORRENCIA).fill(codigo_ocorrencia)
                    
                    # Clica no botão de pesquisa e depois no botão Retornar
                    page.locator(BOTAO_PESQUISAR_OCORRENCIA).click()
                    page.locator(BOTAO_RETORNA_PESQUISA).click()
                except Exception as e:
                    print(f"Ocorreu um erro: {e}")
            # Função para selecionar a Empresa
            def seleciona_empresa(page, codigo_empresa: str):
                # Define os seletores como variáveis
                BOTAO_ABRIR_CAIXA_PESQUISA_FIRMA = r'#formCadastrarProtocolo\:j_idt151'
                CAIXA_INPUT_CODIGO_EMPRESA = r'#formPesquisaEstabelecimento\:value1T'
                BOTAO_PESQUISAR_EMPRESA = r'#formPesquisaEstabelecimento\:j_idt2192'
                BOTAO_RETORNAR_EMPRESA = r'#formPesquisaEstabelecimento\:j_idt2194'
                try:
                    # Clica no ícone para pesquisa da firma e aguarda ficar visivel
                    page.locator(BOTAO_ABRIR_CAIXA_PESQUISA_FIRMA).click()
                    page.wait_for_selector(CAIXA_INPUT_CODIGO_EMPRESA, state="visible", timeout=10000)
                    
                    # Insere o código da firma e clica em pesquisar
                    page.locator(CAIXA_INPUT_CODIGO_EMPRESA).fill(codigo_empresa)
                    page.locator(BOTAO_PESQUISAR_EMPRESA).click()
                    
                    # Clica no botão Retornar
                    page.locator(BOTAO_RETORNAR_EMPRESA).click()
                except Exception as e:
                    print(f"Ocorreu um erro: {e}")
            # Função para selecionar o Profissional
            def seleciona_profissional(page, codigo_profissional: str):
                BOTAO_ABRIR_CAIXA_PESQUISA_PROFISSIONAL = r'#formCadastrarProtocolo\:j_idt174'
                CAIXA_INPUT_CODIGO_PROFISSIONAL = r'#formPesquisaProfissional\:value1T'
                BOTAO_PESQUISAR_PROFISSIONAL = r'#formPesquisaProfissional\:j_idt2054'
                BOTAO_RETORNAR_PROFISSIONAL = r'#formPesquisaProfissional\:j_idt2056'
                try:
                    # Clica no ícone para pesquisa do profissional e aguarda ficar visivel
                    page.locator(BOTAO_ABRIR_CAIXA_PESQUISA_PROFISSIONAL).click()
                    page.wait_for_selector(CAIXA_INPUT_CODIGO_PROFISSIONAL, state="visible", timeout=10000)
                    
                    # Insere o código do profissional e clica em pesquisar
                    page.locator(CAIXA_INPUT_CODIGO_PROFISSIONAL).fill(codigo_profissional)
                    page.locator(BOTAO_PESQUISAR_PROFISSIONAL).click()
                    
                    # Clica no botão Retornar
                    page.locator(BOTAO_RETORNAR_PROFISSIONAL).click()
                except Exception as e:
                    print(f"Ocorreu um erro: {e}")
            # Função para o Tipo de Profissional (Diretor Técnico, Assistênte Técnico ou Substituto)
            def seleciona_tipo_profissional(page, tipo_profissional: str):
                XPATH_OPCOES_TIPO_PROFISSIONAL = r'//*[@id="formCadastrarProtocolo:divRespTec"]/div[1]/div[1]/div[4]/div[1]/select'
                try:
                    if tipo_profissional == "Assistente Técnico":
                        page.locator(XPATH_OPCOES_TIPO_PROFISSIONAL).select_option(value="A")
                    elif tipo_profissional == "Diretor Técnico":
                        page.locator(XPATH_OPCOES_TIPO_PROFISSIONAL).select_option(value="N")
                    elif tipo_profissional == "Substituto":
                        page.locator(XPATH_OPCOES_TIPO_PROFISSIONAL).select_option(value="S")
                except Exception as e:
                    print(f"Ocorreu um erro: {e}")
            # Função para o Tipo de Contrato (Contratado, Servidor Público, Sócio, Proprietário)
            def seleciona_tipo_contrato(page, tipo_contrato: str):
                XPATH_OPCOES_TIPO_CONTRATO = r'//*[@id="formCadastrarProtocolo:divRespTec"]/div[1]/div[1]/div[4]/div[3]/div[1]/select'
                try:
                    if tipo_contrato == "Contratado":
                        page.locator(XPATH_OPCOES_TIPO_CONTRATO).select_option(value="C")
                    elif tipo_contrato == "Sócio":
                        page.locator(XPATH_OPCOES_TIPO_CONTRATO).select_option(value="S")
                    elif tipo_contrato == "Proprietário":
                        page.locator(XPATH_OPCOES_TIPO_CONTRATO).select_option(value="P")
                    elif tipo_contrato == "Servidor Público":
                        page.locator(XPATH_OPCOES_TIPO_CONTRATO).select_option(value="U")
                except Exception as e:
                    print(f"Ocorreu um erro: {e}")
            # Função para o Meio Contratual (CTPS, Contrato de Prestação de Serviço, Outros)
            def seleciona_meio_contratual(page, meio_contratual: str):
                XPATH_OPCOES_MEIO_CONTRATO = r'//*[@id="formCadastrarProtocolo:divRespTec"]/div[1]/div[1]/div[4]/div[3]/div[2]/select'
                try:
                    if meio_contratual == "CTPS":
                        page.locator(XPATH_OPCOES_MEIO_CONTRATO).select_option(value="1")
                    elif meio_contratual == "Contrato de Prestação de Serviço":
                        page.locator(XPATH_OPCOES_MEIO_CONTRATO).select_option(value="2")
                    elif meio_contratual == "Outros":
                        page.locator(XPATH_OPCOES_MEIO_CONTRATO).select_option(value="4")
                except Exception as e:
                    print(f"Ocorreu um erro: {e}")
            # Função para verificar se existe intervalo e preencher os horários
            def verifica_intervalo_e_preenche_horarios(page, tem_intervalo: str, horarios_entrada: str, horarios_saida: str, horarios_entrada2: str, horarios_saida2: str):
                # Define os seletores como variáveis
                SELETOR_ADICIONAR_HORARIO = r'//*[@id="formCadastrarProtocolo:j_idt1186"]'
                CAIXA_INPUT_HORARIO_ENTRADA = r'#formCadastrarProtocolo\:modal-horarios-contratoIn'
                CAIXA_INPUT_HORARIO_SAIDA = r'#formCadastrarProtocolo\:modal-horarios-contratoOut'
                SELETOR_BOTAO_INCLUIR = r'#formCadastrarProtocolo\:modal-horarios-contratoIncluir'
                if tem_intervalo == "Sim":
                    # Insere os horários antes do intervalo e salva
                    page.wait_for_selector(SELETOR_ADICIONAR_HORARIO, state="visible", timeout=10000)
                    page.locator(SELETOR_ADICIONAR_HORARIO).click()
                    page.wait_for_selector(CAIXA_INPUT_HORARIO_ENTRADA, state="visible", timeout=10000)
                    page.locator(CAIXA_INPUT_HORARIO_ENTRADA).fill(horarios_entrada)
                    page.locator(CAIXA_INPUT_HORARIO_SAIDA).fill(horarios_saida)
                    page.locator(SELETOR_BOTAO_INCLUIR).click()
                    # Insere os horários depois do intervalo e salva
                    page.wait_for_selector(SELETOR_ADICIONAR_HORARIO, state="visible", timeout=10000)
                    page.locator(SELETOR_ADICIONAR_HORARIO).click()
                    page.wait_for_selector(CAIXA_INPUT_HORARIO_ENTRADA, state="visible", timeout=10000)
                    page.locator(CAIXA_INPUT_HORARIO_ENTRADA).fill(horarios_entrada2)
                    page.locator(CAIXA_INPUT_HORARIO_SAIDA).fill(horarios_saida2)
                    page.locator(SELETOR_BOTAO_INCLUIR).click()
                elif tem_intervalo == "Não":
                    # Insere os horários antes do intervalo e salva
                    page.wait_for_selector(SELETOR_ADICIONAR_HORARIO, state="visible", timeout=10000)
                    page.locator(SELETOR_ADICIONAR_HORARIO).click()
                    page.wait_for_selector(CAIXA_INPUT_HORARIO_ENTRADA, state="visible", timeout=10000)
                    page.locator(CAIXA_INPUT_HORARIO_ENTRADA).fill(horarios_entrada)
                    page.locator(CAIXA_INPUT_HORARIO_SAIDA).fill(horarios_saida)
                    page.locator(SELETOR_BOTAO_INCLUIR).click()
            # Função para verificar se existe intervalo e preencher horários da firma
            def verifica_intervalo_preenche_horarios_firma(page, tem_intervalo_funcionamento: str, horario_abertura: str, horario_fechamento: str, horario_abertura2: str, horario_fechamento2: str):
                SELETOR_ADICIONAR_HORARIO_FIRMA = r'#formCadastrarProtocolo\:j_idt830'
                CAIXA_INPUT_HORARIO_ABERTURA = r'#formCadastrarProtocolo\:modal-horariosIn'
                CAIXA_INPUT_HORARIO_FECHAMENTO = r'#formCadastrarProtocolo\:modal-horariosOut'
                SELETOR_BOTAO_INCLUIR_FIRMA = r'#formCadastrarProtocolo\:modal-horariosIncluir'
                if tem_intervalo_funcionamento == "Sim":
                    # Insere os horários antes do intervalo
                    page.wait_for_selector(SELETOR_ADICIONAR_HORARIO_FIRMA, state="visible", timeout=10000)
                    page.locator(SELETOR_ADICIONAR_HORARIO_FIRMA).click()
                    page.wait_for_selector(CAIXA_INPUT_HORARIO_ABERTURA, state="visible", timeout=10000)
                    page.locator(CAIXA_INPUT_HORARIO_ABERTURA).fill(horario_abertura)
                    page.locator(CAIXA_INPUT_HORARIO_FECHAMENTO).fill(horario_fechamento)
                    page.locator(SELETOR_BOTAO_INCLUIR_FIRMA).click()
                    # Insere os horários depois do intervalo
                    page.wait_for_selector(SELETOR_ADICIONAR_HORARIO_FIRMA, state="visible", timeout=10000)
                    page.locator(SELETOR_ADICIONAR_HORARIO_FIRMA).click()
                    page.wait_for_selector(CAIXA_INPUT_HORARIO_ABERTURA, state="visible", timeout=10000)
                    page.locator(CAIXA_INPUT_HORARIO_ABERTURA).fill(horario_abertura2)
                    page.locator(CAIXA_INPUT_HORARIO_FECHAMENTO).fill(horario_fechamento2)
                    page.locator(SELETOR_BOTAO_INCLUIR_FIRMA).click()
                elif tem_intervalo_funcionamento == "Não":
                    # Insere os horários antes do intervalo
                    page.wait_for_selector(SELETOR_ADICIONAR_HORARIO_FIRMA, state="visible", timeout=10000)
                    page.locator(SELETOR_ADICIONAR_HORARIO_FIRMA).click()
                    page.wait_for_selector(CAIXA_INPUT_HORARIO_ABERTURA, state="visible", timeout=10000)
                    page.locator(CAIXA_INPUT_HORARIO_ABERTURA).fill(horario_abertura)
                    page.locator(CAIXA_INPUT_HORARIO_FECHAMENTO).fill(horario_fechamento)
                    page.locator(SELETOR_BOTAO_INCLUIR_FIRMA).click()
                    
            ocorrencia = dados_protocolo["ocorrencia"]
            # Se for uma Baixa de Responsabilidade Técnica
            if ocorrencia == '162': 
                codigo_empresa = dados_protocolo["inscricao_firma"]
                codigo_profissional = dados_protocolo["inscricao_profissional"]
                seleciona_ocorrencia(page, ocorrencia)
                seleciona_empresa(page, codigo_empresa)
                seleciona_profissional(page, codigo_profissional)
                # Vai para "Dados da Firma"
                page.locator(XPATH_DADOS_FIRMA).click()
                # Vai para "Responsável Técnico"
                page.locator(XPATH_RESPONSAVEL_TECNICO).click()
                # Clica em "Carregar Contrato Profissional" e depois no ícone de editar
                page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt1357"]').click()
                page.locator('xpath=//*[@id="formCadastrarProtocolo:dataTableRTAtivo:0:j_idt1330"]').click()
                # Preenche a data de rescisao e clica em salvar
                page.locator('xpath=//*[@id="formCadastrarProtocolo:j_idt1123_input"]').fill(dados_protocolo["data_rescisao"])
                page.locator(SELETOR_BOTAO_SALVAR_DADOS_CONTRATUAIS).click()
            # Se for uma Responsabilidade Técnica
            elif ocorrencia == '925':
                codigo_empresa = dados_protocolo["inscricao_firma"]
                codigo_profissional = dados_protocolo["inscricao_profissional"]
                tipo_profissional = dados_protocolo["tipo_profissional"]
                tipo_contrato = dados_protocolo["tipo_contrato"]
                meio_contratual = dados_protocolo["meio_contrato"]
                tem_intervalo = dados_protocolo["tem_intervalo"]
                horarios_entrada = dados_protocolo["horarios_entrada"]
                horarios_saida = dados_protocolo["horarios_saida"]
                horarios_entrada2 = dados_protocolo["horarios_entrada2"]
                horarios_saida2 = dados_protocolo["horarios_saida2"]
                seleciona_ocorrencia(page, ocorrencia)
                seleciona_empresa(page, codigo_empresa)
                seleciona_profissional(page, codigo_profissional)
                # Vai para "Dados da Firma" e depois clica em Responsável Técnico
                page.locator(XPATH_DADOS_FIRMA).click()
                page.locator(XPATH_RESPONSAVEL_TECNICO).click()
                # Clica em "Adicionar RT"
                page.locator(SELETOR_ADICIONAR_RT).click()
                seleciona_tipo_profissional(page, tipo_profissional)
                # Insere a data do contrato
                page.locator(SELETOR_DATA_CONTRATO).fill(dados_protocolo["data_contratual"])
                seleciona_tipo_contrato(page, tipo_contrato)
                seleciona_meio_contratual(page, meio_contratual)
                verifica_intervalo_e_preenche_horarios(page, tem_intervalo, horarios_entrada, horarios_saida, horarios_entrada2, horarios_saida2)
                # Salva os dados contratuais e horários
                page.locator(SELETOR_BOTAO_SALVAR_DADOS_CONTRATUAIS).click()
            # Se for uma Alteração de Assistência Farmacêutica
            elif ocorrencia == '142':
                codigo_empresa = dados_protocolo["inscricao_firma"]
                codigo_profissional = dados_protocolo["inscricao_profissional"]
                tem_intervalo = dados_protocolo["tem_intervalo"]
                horarios_entrada = dados_protocolo["horarios_entrada"]
                horarios_saida = dados_protocolo["horarios_saida"]
                horarios_entrada2 = dados_protocolo["horarios_entrada2"]
                horarios_saida2 = dados_protocolo["horarios_saida2"]
                seleciona_ocorrencia(page, ocorrencia)
                seleciona_empresa(page, codigo_empresa)
                seleciona_profissional(page, codigo_profissional)
                # Vai para "Dados da Firma" e depois clica em Responsável Técnico
                page.locator(XPATH_DADOS_FIRMA).click()
                page.locator(XPATH_RESPONSAVEL_TECNICO).click()
                # Clica em "Carregar Contrato Profissional" e depois no ícone de editar
                page.locator(SELETOR_BOTAO_CARREGAR_CONTRATO).click()
                page.locator(SELETOR_ICONE_EDITAR).click()
                # Verifica quantos horários antigos existem para excluir
                page.wait_for_selector(SELETOR_ICONE_EXCLUIR_HORARIO, state="visible", timeout=10000)
                while page.locator(SELETOR_ICONE_EXCLUIR_HORARIO).count() > 0:
                    page.locator(SELETOR_ICONE_EXCLUIR_HORARIO).click()
                    page.wait_for_selector(SELETOR_BOTAO_CONFIRMAR_EXCLUSAO, state='visible', timeout=10000)
                    page.locator(SELETOR_BOTAO_CONFIRMAR_EXCLUSAO).click()
                    page.wait_for_selector(SELETOR_BOTAO_CONFIRMAR_EXCLUSAO, state="hidden", timeout=10000)
                verifica_intervalo_e_preenche_horarios(page, tem_intervalo, horarios_entrada, horarios_saida, horarios_entrada2, horarios_saida2)
                # Salva os dados contratuais e horários
                page.locator(SELETOR_BOTAO_SALVAR_DADOS_CONTRATUAIS).click()
            # Se for uma Alteração de Horário de Funcionamento
            elif ocorrencia == '106':
                codigo_empresa = dados_protocolo.get("inscricao_firma", "")
                horarios_abertura = dados_protocolo.get("horario_funcionamento_abertura", "")
                horarios_fechamento = dados_protocolo.get("horario_funcionamento_fechamento", "")
                tem_intervalo_funcionamento = dados_protocolo.get("tem_intervalo_funcionamento", "Não")
                horarios_abertura2 = dados_protocolo.get("horario_funcionamento_abertura2", "")
                horarios_fechamento2 = dados_protocolo.get("horario_funcionamento_fechamento2", "")
                seleciona_ocorrencia(page, ocorrencia)
                seleciona_empresa(page, codigo_empresa)
                # Vai para "Dados da Firma" e depois clica em Horários
                page.locator(XPATH_DADOS_FIRMA).click()
                page.locator(XPATH_BOTAO_HORARIOS).click()
                # Loop while para verificar quantos horários existem e excluí-los
                page.wait_for_selector(SELETOR_ICONE_EXCLUIR_HORARIO_FIRMA, state="visible", timeout=10000)
                while page.locator(SELETOR_ICONE_EXCLUIR_HORARIO_FIRMA).count() > 0:
                    page.locator(SELETOR_ICONE_EXCLUIR_HORARIO_FIRMA).click()
                    page.wait_for_selector(SELETOR_CONFIRMAR_EXCLUSAO_HORARIO_FIRMA, state='visible', timeout=10000)
                    page.locator(SELETOR_CONFIRMAR_EXCLUSAO_HORARIO_FIRMA).click()
                    page.wait_for_selector(SELETOR_CONFIRMAR_EXCLUSAO_HORARIO_FIRMA, state="hidden", timeout=10000)
                verifica_intervalo_preenche_horarios_firma(page, tem_intervalo_funcionamento, horarios_abertura, horarios_fechamento, horarios_abertura2, horarios_fechamento2)
            time.sleep(5)
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
        finally:
            navegador.close()
            
if __name__ == '__main__':
    dados_automacao = obter_dados_protocolo()
    if dados_automacao:
        executar_automacao = inicia_a_geracao_do_protocolo(dados_automacao)