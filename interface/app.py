# INTERFACE GRÁFICA

import tkinter as tk

from tkinter import messagebox

# Algoritmo
from funcoes.funcoes import gerar_passos_ordenacao

# Configurações
from configuracao import (
    COR_FUNDO,
    COR_PAINEL,
    COR_CAIXA,
    COR_TEXTO,
    COR_TEXTO_SECUNDARIO,
    COR_AZUL,
    COR_LARANJA,
    COR_VERDE,
    COR_VERMELHO,
    LARGURA_JANELA,
    ALTURA_JANELA,
    LARGURA_CANVAS,
    ALTURA_CANVAS,
    LIMITE_NUMEROS,
    TEMPO_PASSO,
    COR_NORMAL,
    COR_ORDENADO,
    COR_CHAVE,
    COR_COMPARACAO,
    COR_LINHA
)

class AppOrdenacao:

    # INICIALIZAÇÃO

    def __init__(self, janela):

        self.janela = janela

        self.numeros = []

        self.passos = []

        self.indice_passo = 0

        self.animando = False

        # JANELA

        self.janela.title(
            "Visualizador de Ordenção"
        )

        self.janela.geometry(
            f"{LARGURA_JANELA}x{ALTURA_JANELA}"
        )

        self.janela.configure(
            bg=COR_FUNDO
        )

        # CRIAÇÃO DA INTERFACE

        self.criar_cabecalho()

        self.criar_contadores()

        self.criar_canvas()

        self.criar_controles()

        self.criar_status()

        self.criar_painel_codigo()

        # ENTER também adiciona.
        self.janela.bind(
            "<Return>",
            lambda evento: self.adicionar_numero()
        )

        self.desenhar_lista_normal()

    # CABEÇALHO

    def criar_cabecalho(self):

        titulo = tk.Label(
            self.janela,
            text="ORDENADOR",
            font=("Arial", 28, "bold"),
            fg=COR_TEXTO,
            bg=COR_FUNDO
        )

        titulo.pack(
            pady=(15, 0)
        )

        subtitulo = tk.Label(
            self.janela,
            text="ORDENAÇÃO DE NUMERAÇÃO",
            font=("Arial", 11),
            fg=COR_TEXTO_SECUNDARIO,
            bg=COR_FUNDO
        )

        subtitulo.pack(
            pady=(0, 12)
        )

    # CONTADORES

    def criar_contadores(self):

        frame = tk.Frame(
            self.janela,
            bg=COR_FUNDO
        )

        frame.pack(
            pady=5
        )

        # COMPARAÇÕES

        frame_comparacoes = tk.Frame(
            frame,
            bg=COR_PAINEL,
            padx=30,
            pady=10
        )

        frame_comparacoes.grid(
            row=0,
            column=0,
            padx=8
        )

        tk.Label(
            frame_comparacoes,
            text="COMPARA",
            bg=COR_PAINEL,
            fg=COR_TEXTO_SECUNDARIO,
            font=("Arial", 10)
        ).pack(
            side="left"
        )

        self.label_comparacoes = tk.Label(
            frame_comparacoes,
            text="0",
            bg=COR_PAINEL,
            fg=COR_AZUL,
            font=("Arial", 20, "bold")
        )

        self.label_comparacoes.pack(
            side="left",
            padx=(25, 0)
        )

        # DESLOCAMENTOS

        frame_deslocamentos = tk.Frame(
            frame,
            bg=COR_PAINEL,
            padx=30,
            pady=10
        )

        frame_deslocamentos.grid(
            row=0,
            column=1,
            padx=8
        )

        tk.Label(
            frame_deslocamentos,
            text="DESLOCA",
            bg=COR_PAINEL,
            fg=COR_TEXTO_SECUNDARIO,
            font=("Arial", 10)
        ).pack(
            side="left"
        )

        self.label_deslocamentos = tk.Label(
            frame_deslocamentos,
            text="0",
            bg=COR_PAINEL,
            fg=COR_LARANJA,
            font=("Arial", 20, "bold")
        )

        self.label_deslocamentos.pack(
            side="left",
            padx=(25, 0)
        )

    # CANVAS

    def criar_canvas(self):

        self.canvas = tk.Canvas(
            self.janela,
            width=LARGURA_CANVAS,
            height=ALTURA_CANVAS,
            bg=COR_FUNDO,
            highlightthickness=0
        )

        self.canvas.pack(
            pady=5
        )

    # CONTROLES

    def criar_controles(self):

        frame = tk.Frame(
            self.janela,
            bg=COR_FUNDO
        )

        frame.pack(
            pady=5
        )

        self.entrada_numero = tk.Entry(
            frame,
            width=10,
            justify="center",
            font=("Arial", 15)
        )

        self.entrada_numero.grid(
            row=0,
            column=0,
            padx=5,
            ipady=5
        )

        self.botao_adicionar = tk.Button(
            frame,
            text="ADICIONAR",
            command=self.adicionar_numero,
            bg=COR_AZUL,
            fg="#06111F",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=7
        )

        self.botao_adicionar.grid(
            row=0,
            column=1,
            padx=5
        )

        self.botao_arrumar = tk.Button(
            frame,
            text="ARRUMAR",
            command=self.arrumar_numeros,
            bg=COR_VERDE,
            fg="#06111F",
            font=("Arial", 10, "bold"),
            padx=18,
            pady=7
        )

        self.botao_arrumar.grid(
            row=0,
            column=2,
            padx=5
        )

        self.botao_limpar = tk.Button(
            frame,
            text="LIMPAR",
            command=self.limpar,
            bg=COR_VERMELHO,
            fg="#FFFFFF",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=7
        )

        self.botao_limpar.grid(
            row=0,
            column=3,
            padx=5
        )

    # STATUS

    def criar_status(self):

        self.label_lista = tk.Label(
            self.janela,
            text="Lista atual: []",
            bg=COR_FUNDO,
            fg=COR_TEXTO,
            font=("Consolas", 11)
        )

        self.label_lista.pack(
            pady=(5, 0)
        )

        self.label_status = tk.Label(
            self.janela,
            text="Adicione números para começar.",
            bg=COR_FUNDO,
            fg=COR_TEXTO_SECUNDARIO,
            font=("Arial", 10)
        )

        self.label_status.pack(
            pady=(2, 6)
        )

    # PAINEL DO ALGORITMO

    def criar_painel_codigo(self):

        frame = tk.Frame(
            self.janela,
            bg="#06111F",
            padx=15,
            pady=8
        )

        frame.pack(
            padx=80,
            pady=5,
            fill="x"
        )

        self.codigo_text = tk.Text(
            frame,
            height=7,
            bg="#06111F",
            fg="#A7D9F5",
            insertbackground="#FFFFFF",
            relief="flat",
            font=("Consolas", 11),
            padx=10,
            pady=5
        )

        codigo = (
            "1  for i in range(1, len(vetor)):\n"
            "2      chave = vetor[i]\n"
            "3      j = i - 1\n"
            "4      while j >= 0 and vetor[j] > chave:\n"
            "5          vetor[j + 1] = vetor[j]\n"
            "6          j -= 1\n"
            "7      vetor[j + 1] = chave"
        )

        self.codigo_text.insert(
            "1.0",
            codigo
        )

        self.codigo_text.tag_configure(
            "ativa",
            background="#213853",
            foreground="#FFFFFF"
        )

        self.codigo_text.config(
            state="disabled"
        )

        self.codigo_text.pack(
            fill="x"
        )

        # Variáveis do algoritmo.
        self.label_variaveis = tk.Label(
            frame,
            text="n = 0     i = -     j = -     chave = -",
            bg="#10283F",
            fg=COR_TEXTO,
            font=("Consolas", 11, "bold"),
            anchor="w",
            padx=12,
            pady=5
        )

        self.label_variaveis.pack(
            fill="x"
        )

    # ADICIONAR NÚMERO

    def adicionar_numero(self):

        # Não permite alterar a lista durante a animação.
        if self.animando:
            return

        valor = self.entrada_numero.get().strip()

        if valor == "":

            messagebox.showwarning(
                "Atenção",
                "Digite um número."
            )

            return

        try:

            numero = int(valor)

        except ValueError:

            messagebox.showerror(
                "Erro",
                "Digite apenas números inteiros."
            )

            return

        if len(self.numeros) >= LIMITE_NUMEROS:

            messagebox.showwarning(
                "Limite",
                f"Você pode inserir até {LIMITE_NUMEROS} números."
            )

            return

        self.numeros.append(
            numero
        )

        self.entrada_numero.delete(
            0,
            tk.END
        )

        # Ao inserir um número novo, os contadores
        # voltam ao início.
        self.label_comparacoes.config(
            text="0"
        )

        self.label_deslocamentos.config(
            text="0"
        )

        self.atualizar_lista()

        self.label_status.config(
            text=f"Número {numero} adicionado."
        )

        self.desenhar_lista_normal()

    # INICIAR ORDENAÇÃO

    def arrumar_numeros(self):

        if self.animando:
            return

        if len(self.numeros) < 2:

            messagebox.showwarning(
                "Atenção",
                "Insira pelo menos dois números."
            )

            return

        # Geramos todos os passos do algoritmo.
        self.passos = list(
            gerar_passos_ordenacao(
                self.numeros
            )
        )

        self.indice_passo = 0

        self.animando = True

        # Evita que o usuário altere a lista
        # durante a ordenação.
        self.botao_adicionar.config(
            state="disabled"
        )

        self.botao_arrumar.config(
            state="disabled"
        )

        self.botao_limpar.config(
            state="disabled"
        )

        self.entrada_numero.config(
            state="disabled"
        )

        self.executar_proximo_passo()

    # ANIMAÇÃO

    def executar_proximo_passo(self):

        # Terminamos todos os passos.
        if self.indice_passo >= len(self.passos):

            self.animando = False

            self.botao_adicionar.config(
                state="normal"
            )

            self.botao_arrumar.config(
                state="normal"
            )

            self.botao_limpar.config(
                state="normal"
            )

            self.entrada_numero.config(
                state="normal"
            )

            return

        estado = self.passos[
            self.indice_passo
        ]

        # Atualiza a lista interna.
        self.numeros = estado[
            "vetor"
        ].copy()

        # Atualiza contadores.
        self.label_comparacoes.config(
            text=str(
                estado["comparacoes"]
            )
        )

        self.label_deslocamentos.config(
            text=str(
                estado["deslocamentos"]
            )
        )

        # Atualiza mensagem.
        self.label_status.config(
            text=estado["mensagem"]
        )

        self.atualizar_lista()

        # Atualiza variáveis.
        self.atualizar_variaveis(
            estado
        )

        # Destaca linha do código.
        self.destacar_linha(
            estado["linha"]
        )

        # Redesenha a visualização.
        self.desenhar_estado(
            estado
        )

        self.indice_passo += 1

        # Executa o próximo passo depois do tempo definido.
        self.janela.after(
            TEMPO_PASSO,
            self.executar_proximo_passo
        )

    # DESTACAR LINHA DO CÓDIGO

    def destacar_linha(self, linha):

        self.codigo_text.config(
            state="normal"
        )

        self.codigo_text.tag_remove(
            "ativa",
            "1.0",
            tk.END
        )

        if linha is not None:

            self.codigo_text.tag_add(
                "ativa",
                f"{linha}.0",
                f"{linha}.end"
            )

        self.codigo_text.config(
            state="disabled"
        )

    # MOSTRAR VARIÁVEIS

    def atualizar_variaveis(self, estado):

        n = len(
            estado["vetor"]
        )

        i = (
            "-"
            if estado["i"] is None
            else estado["i"]
        )

        j = (
            "-"
            if estado["j"] is None
            else estado["j"]
        )

        chave = (
            "-"
            if estado["chave"] is None
            else estado["chave"]
        )

        self.label_variaveis.config(
            text=(
                f"n = {n}     "
                f"i = {i}     "
                f"j = {j}     "
                f"chave = {chave}"
            )
        )

    # DESENHAR LISTA SEM ANIMAÇÃO

    def desenhar_lista_normal(self):

        estado = {
            "vetor": self.numeros,
            "tipo": "normal",
            "chave": None,
            "buraco": None,
            "comparar_indice": None,
            "ordenado_ate": -1
        }

        self.desenhar_estado(
            estado
        )

    # DESENHAR ESTADO

    def desenhar_estado(self, estado):

        self.canvas.delete(
            "all"
        )

        vetor = estado["vetor"]

        if len(vetor) == 0:

            self.canvas.create_text(
                LARGURA_CANVAS / 2,
                ALTURA_CANVAS / 2,
                text="Insira alguns números para começar",
                fill=COR_TEXTO_SECUNDARIO,
                font=("Arial", 15)
            )

            return

        maior = max(vetor)

        menor = min(vetor)

        quantidade = len(vetor)

        espaco = (
            LARGURA_CANVAS
            /
            quantidade
        )

        largura = min(
            72,
            espaco * 0.62
        )

        # Região reservada para as barras.
        base_y = ALTURA_CANVAS - 25

        buraco = estado.get(
            "buraco"
        )

        comparar_indice = estado.get(
            "comparar_indice"
        )

        ordenado_ate = estado.get(
            "ordenado_ate",
            -1
        )

        chave = estado.get(
            "chave"
        )

        # CHAVE SUSPENSA

        if chave is not None:

            centro_chave = (
                LARGURA_CANVAS / 2
            )

            # Linha vertical.
            self.canvas.create_line(
                centro_chave,
                28,
                centro_chave,
                88,
                fill=COR_CHAVE,
                width=3
            )

            # Caixa da chave.
            self.canvas.create_rectangle(
                centro_chave - 34,
                38,
                centro_chave + 34,
                78,
                fill="#3B3020",
                outline=COR_CHAVE,
                width=3
            )

            self.canvas.create_text(
                centro_chave,
                58,
                text=str(chave),
                fill=COR_TEXTO,
                font=("Arial", 15, "bold")
            )

            self.canvas.create_text(
                centro_chave,
                18,
                text="CHAVE",
                fill=COR_CHAVE,
                font=("Arial", 9, "bold")
            )

        # BARRAS

        for indice, numero in enumerate(vetor):

            centro_x = (
                espaco * indice
                +
                espaco / 2
            )

            # POSIÇÃO DO BURACO

            if indice == buraco:

                self.canvas.create_rectangle(
                    centro_x - largura / 2,
                    base_y - 60,
                    centro_x + largura / 2,
                    base_y,
                    outline=COR_CHAVE,
                    dash=(5, 4),
                    width=2
                )

                continue

            # ALTURA

            if maior == menor:

                altura = 80

            else:

                proporcao = (
                    (numero - menor)
                    /
                    (maior - menor)
                )

                altura = (55 + proporcao * 80)

            y1 = base_y - altura

            # COR

            if indice == comparar_indice:

                cor = COR_COMPARACAO

            elif indice <= ordenado_ate:

                cor = COR_ORDENADO

            else:

                cor = COR_NORMAL

            # BARRA

            self.canvas.create_rectangle(
                centro_x - largura / 2,
                y1,
                centro_x + largura / 2,
                base_y,
                fill=COR_CAIXA,
                outline=cor,
                width=3
            )

            # Número.
            self.canvas.create_text(
                centro_x,
                y1 + 20,
                text=str(numero),
                fill=COR_TEXTO,
                font=("Arial", 14, "bold")
            )

        # LINHA DE BASE

        self.canvas.create_line(
            20,
            base_y + 5,
            LARGURA_CANVAS - 20,
            base_y + 5,
            fill=COR_LINHA,
            width=3
        )

        # Parte já ordenada.
        if ordenado_ate >= 0:

            fim_ordenado = (
                espaco * (ordenado_ate + 1)
            )

            self.canvas.create_line(
                20,
                base_y + 5,
                min(
                    fim_ordenado,
                    LARGURA_CANVAS - 20
                ),
                base_y + 5,
                fill=COR_ORDENADO,
                width=4
            )

    # ATUALIZAR LISTA

    def atualizar_lista(self):

        self.label_lista.config(
            text=f"Lista atual: {self.numeros}"
        )

    # LIMPAR

    def limpar(self):

        if self.animando:
            return

        self.numeros.clear()

        self.label_comparacoes.config(
            text="0"
        )

        self.label_deslocamentos.config(
            text="0"
        )

        self.label_status.config(
            text="Adicione números para começar."
        )

        self.label_variaveis.config(
            text="n = 0     i = -     j = -     chave = -"
        )

        self.atualizar_lista()

        self.destacar_linha(
            None
        )

        self.desenhar_lista_normal()