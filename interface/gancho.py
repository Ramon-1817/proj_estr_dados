
"""Garra animada para o Insertion Sort.

Arquivo: interface/gancho.py
A classe herda a interface original; não altera o algoritmo nem os botões.
"""

import math
import time

from configuracao import (
    ALTURA_CANVAS,
    COR_CAIXA,
    COR_CHAVE,
    COR_COMPARACAO,
    COR_LINHA,
    COR_NORMAL,
    COR_ORDENADO,
    COR_TEXTO,
    LARGURA_CANVAS,
    TEMPO_PASSO,
)
from interface.app import AppOrdenacao


class AppOrdenacaoComGancho(AppOrdenacao):
    """Mostra uma garra com compartimento enquanto a ordenação acontece."""

    # Posição de descanso da garra, próxima ao trilho superior.
    ALTURA_DESCANSO = 57
    # Quantos pixels acima da tela a garra fica recolhida.
    ALTURA_RECOLHIDA = -55

    def __init__(self, janela):
        # A interface original chama desenhar_estado() durante a criação.
        self._tarefa_garra = None
        self._posicao_garra = None
        self._escala = None
        super().__init__(janela)

    @staticmethod
    def _suavizar(valor):
        """Começa e termina cada movimento de forma progressiva."""
        t = max(0.0, min(1.0, valor))
        return (1.0 - math.cos(math.pi * t)) / 2.0

    @staticmethod
    def _misturar(inicio, fim, t):
        return inicio + (fim - inicio) * t

    def _centro(self, indice, quantidade):
        return LARGURA_CANVAS * (indice + 0.5) / quantidade

    def _altura_barra(self, numero):
        minimo, maximo = self._escala
        if minimo == maximo:
            return 80.0
        proporcao = (numero - minimo) / (maximo - minimo)
        return 55.0 + 80.0 * max(0.0, min(1.0, proporcao))

    def _altura_pegada(self, numero):
        """Alinha as duas pinças com o topo do número escolhido."""
        topo_barra = ALTURA_CANVAS - 25 - self._altura_barra(numero)
        return topo_barra - 37

    def _seguir_rota(self, rota, tempo):
        """Interpola os pontos de uma rota (tempo, x, y)."""
        if tempo <= rota[0][0]:
            return rota[0][1], rota[0][2]

        for inicio, fim in zip(rota, rota[1:]):
            t0, x0, y0 = inicio
            t1, x1, y1 = fim
            if tempo <= t1:
                progresso = self._suavizar((tempo - t0) / (t1 - t0))
                return (
                    self._misturar(x0, x1, progresso),
                    self._misturar(y0, y1, progresso),
                )

        return rota[-1][1], rota[-1][2]

    def _rota_da_etapa(self, estado):
        """Define os movimentos de pegar, carregar e depositar cada barra."""
        vetor = estado["vetor"]
        tipo = estado["tipo"]
        quantidade = len(vetor)
        descanso = self.ALTURA_DESCANSO

        # A última posição da garra é a origem do próximo movimento.
        origem = self._posicao_garra
        if origem is None:
            x_inicial = self._centro(min(1, quantidade - 1), quantidade)
            origem = (x_inicial, self.ALTURA_RECOLHIDA)

        ox, oy = origem

        if tipo == "inicio":
            x = self._centro(min(1, quantidade - 1), quantidade)
            return [(0.0, x, self.ALTURA_RECOLHIDA),
                    (1.0, x, descanso)]

        if tipo == "selecionar":
            indice = estado["i"]
            x = self._centro(indice, quantidade)
            y = self._altura_pegada(estado["chave"])
            # Aproxima -> desce -> recolhe a chave -> volta ao alto.
            return [(0.0, ox, oy), (0.23, x, descanso),
                    (0.43, x, y), (0.55, x, y),
                    (0.90, x, descanso), (1.0, x, descanso)]

        if tipo == "comparar":
            indice = estado.get("comparar_indice")
            if isinstance(indice, int) and 0 <= indice < quantidade:
                x = self._centro(indice, quantidade)
            else:
                x = ox
            # A chave permanece guardada durante a comparação.
            return [(0.0, ox, oy), (1.0, x, descanso)]

        if tipo == "deslocar":
            j = estado["j"]
            numero = vetor[j + 1]
            x_origem = self._centro(j, quantidade)
            x_destino = self._centro(j + 1, quantidade)
            y = self._altura_pegada(numero)

            # Pega outra barra, levanta, transporta e deposita.
            # O compartimento continua guardando a chave original.
            return [(0.0, ox, oy), (0.13, x_origem, descanso),
                    (0.29, x_origem, y), (0.43, x_origem, descanso),
                    (0.74, x_destino, descanso),
                    (0.90, x_destino, y), (1.0, x_destino, descanso)]

        if tipo == "inserir":
            indice = estado["j"]
            x = self._centro(indice, quantidade)
            y = self._altura_pegada(estado["chave"])

            # Desce até a posição vazia, deposita a chave e sobe.
            return [(0.0, ox, oy), (0.29, x, descanso),
                    (0.56, x, y), (0.72, x, y),
                    (1.0, x, descanso)]

        if tipo == "fim":
            # Retira o mecanismo da tela.
            return [(0.0, ox, oy),
                    (1.0, ox, self.ALTURA_RECOLHIDA)]

        return [(0.0, ox, oy), (1.0, ox, oy)]

    def desenhar_estado(self, estado):
        """Substitui apenas o desenho; o Insertion Sort continua original."""
        if self._tarefa_garra is not None:
            self.janela.after_cancel(self._tarefa_garra)
            self._tarefa_garra = None

        atual = dict(estado)
        atual["vetor"] = list(estado.get("vetor", []))
        tipo = atual.get("tipo", "normal")

        # Antes de ARRUMAR não aparece trilho, cabo ou garra.
        if tipo == "normal" or not atual["vetor"]:
            self._posicao_garra = None
            self._escala = None
            super().desenhar_estado(atual)
            return

        if self._escala is None or tipo == "inicio":
            vetor = atual["vetor"]
            self._escala = (min(vetor), max(vetor))

        rota = self._rota_da_etapa(atual)
        inicio = time.monotonic()

        # Cabe dentro do intervalo entre etapas do app.py.
        duracao = max(0.15, (TEMPO_PASSO - 25) / 1000.0)

        def desenhar_frame():
            progresso = min(1.0, (time.monotonic() - inicio) / duracao)
            x, y = self._seguir_rota(rota, progresso)
            self._posicao_garra = (x, y)

            self._desenhar_cena(atual, progresso, x, y, rota)

            if progresso < 1.0:
                self._tarefa_garra = self.janela.after(16, desenhar_frame)
            else:
                self._tarefa_garra = None
                if tipo == "fim":
                    self._posicao_garra = None

        desenhar_frame()

    def _desenhar_cena(self, estado, progresso, x_garra, y_garra, rota):
        """Desenha as barras e a garra em cada quadro de animação."""
        self.canvas.delete("all")

        vetor = estado["vetor"]
        tipo = estado["tipo"]
        quantidade = len(vetor)
        espaco = LARGURA_CANVAS / quantidade
        largura = min(72, espaco * 0.62)
        base = ALTURA_CANVAS - 25
        buraco = estado.get("buraco")
        indice_comparacao = estado.get("comparar_indice")
        ordenado_ate = estado.get("ordenado_ate", -1)

        # Linha inferior (mantém o visual da interface existente).
        self.canvas.create_line(
            20, base + 5,
            LARGURA_CANVAS - 20, base + 5,
            fill=COR_LINHA, width=3
        )

        # Enquanto desloca, vetor[j+1] já contém o valor novo, mas ele
        # ainda precisa viajar visualmente de j para j+1.
        j_movimento = estado.get("j") if tipo == "deslocar" else None
        movendo = (
            isinstance(j_movimento, int)
            and 0 <= j_movimento < quantidade - 1
        )

        for indice, numero in enumerate(vetor):

            # Durante o transporte essas duas posições são desenhadas
            # separadamente por uma única barra móvel, mais abaixo.
            if movendo and indice in (j_movimento, j_movimento + 1):
                continue

            # A chave só sai da lista quando entra no compartimento.
            if tipo == "selecionar" and indice == estado["i"]:
                if progresso >= 0.50:
                    continue
                cor = COR_CHAVE

            # A chave só reaparece depois de sair do compartimento.
            elif tipo == "inserir" and indice == estado["j"]:
                if progresso < 0.72:
                    continue

                # A chave reaparece gradualmente na posição correta.
                escala = self._suavizar((progresso - 0.72) / 0.23)

                self._desenhar_barra(
                    self._centro(indice, quantidade),
                    base, largura, numero, COR_ORDENADO, escala
                )
                continue

            # Quando a chave está guardada, o espaço fica invisível.
            elif indice == buraco:
                continue

            elif indice == indice_comparacao:
                cor = COR_COMPARACAO
            elif indice <= ordenado_ate:
                cor = COR_ORDENADO
            else:
                cor = COR_NORMAL

            self._desenhar_barra(
                self._centro(indice, quantidade),
                base, largura, numero, cor
            )

        # A garra transporta FISICAMENTE cada barra deslocada.
        if movendo:
            j = j_movimento
            numero = vetor[j + 1]

            # Até agarrar a barra, ela continua na posição original.
            if progresso < 0.29:
                x_barra = self._centro(j, quantidade)
                base_barra = base

            elif progresso <= 0.90:
                # O número acompanha as pinças durante o transporte.
                x_barra = x_garra
                base_barra = base + y_garra - self._altura_pegada(numero)

            else:
                # A barra fica depositada enquanto a garra sobe vazia.
                x_barra = self._centro(j + 1, quantidade)
                base_barra = base

            self._desenhar_barra(
                x_barra, base_barra, largura, numero, COR_COMPARACAO
            )

        # Linha verde indicando o trecho já ordenado.
        if ordenado_ate >= 0:
            fim = min(
                espaco * (ordenado_ate + 1),
                LARGURA_CANVAS - 20
            )
            if fim > 20:
                self.canvas.create_line(
                    20, base + 5, fim, base + 5,
                    fill=COR_ORDENADO, width=4
                )

        # A chave permanece guardada enquanto os OUTROS números se movem.
        chave = estado.get("chave")

        if tipo == "selecionar":
            armazenado = chave if progresso >= 0.50 else None
        elif tipo in ("comparar", "deslocar"):
            armazenado = chave
        elif tipo == "inserir":
            armazenado = chave if progresso < 0.72 else None
        else:
            armazenado = None

        # Após o recolhimento, não há gancho nem cabo na tela.
        if tipo == "fim" and progresso >= 1.0:
            return

        if tipo in ("comparar", "deslocar"):
            cor_garra = COR_COMPARACAO
        elif tipo == "fim":
            cor_garra = COR_ORDENADO
        else:
            cor_garra = COR_CHAVE

        self._desenhar_garra(
            x_garra, y_garra, largura, cor_garra, armazenado
        )

    def _desenhar_barra(self, x, base, largura, numero, cor, escala=1.0):
        altura = self._altura_barra(numero) * escala

        if altura <= 1:
            return

        self.canvas.create_rectangle(
            x - largura / 2, base - altura,
            x + largura / 2, base,
            fill=COR_CAIXA,
            outline=cor,
            width=3
        )

        if altura >= 36:
            self.canvas.create_text(
                x, base - altura + 20,
                text=str(numero),
                fill=COR_TEXTO,
                font=("Arial", 14, "bold")
            )

    def _desenhar_garra(self, x, y, largura, cor, chave_guardada):
        """Trilho, cabo, compartimento da chave e pinças."""

        self.canvas.create_line(
            18, 16,
            LARGURA_CANVAS - 18, 16,
            fill=COR_LINHA,
            width=2
        )

        # A garra surge por baixo do trilho e fica presa pelo cabo.
        if y < -37:
            return

        self.canvas.create_rectangle(
            x - 19, 9,
            x + 19, 24,
            fill="#10283F",
            outline=cor,
            width=2
        )

        self.canvas.create_oval(
            x - 4, 12,
            x + 4, 20,
            fill=COR_CHAVE,
            outline=""
        )

        if y - 18 > 24:
            self.canvas.create_line(
                x, 24, x, y - 18,
                fill="#91A7B8",
                width=2
            )

        # Compartimento: mostra somente a chave.
        self.canvas.create_rectangle(
            x - 28, y - 18,
            x + 28, y + 17,
            fill="#24344A",
            outline=cor,
            width=2
        )

        if chave_guardada is not None:
            self.canvas.create_text(
                x, y + 3,
                text=str(chave_guardada),
                fill=COR_TEXTO,
                font=("Arial", 15, "bold")
            )
        else:
            self.canvas.create_line(
                x - 12, y + 2,
                x + 12, y + 2,
                fill="#52697B",
                width=2
            )

        # As pinças transportam outras barras mesmo
        # quando o compartimento está ocupado pela chave.
        abertura = max(22, min(42, largura / 2 + 6))

        for lado in (-1, 1):
            self.canvas.create_line(
                x + lado * 18, y + 16,
                x + lado * abertura, y + 16,
                x + lado * abertura, y + 37,
                x + lado * (abertura - 10), y + 37,
                fill=cor,
                width=3,
                joinstyle="round"
            )