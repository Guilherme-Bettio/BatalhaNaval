import os
import random
import tkinter as tk
from tkinter import messagebox

try:
    import winsound
except ImportError:
    winsound = None

TAMANHO = 10
FROTA = [
    ("USS Enterprise", 4),
    ("USS Voyager", 3),
    ("USS Defiant", 2),
    ("USS Excelsior", 2),
]
AGUA = "~"
NAVIO = "N"
TIRO_AGUA = "O"
TIRO_ACERTO = "X"
MODOS = [
    ("Jogador vs Computador", "pvc"),
    ("Jogador vs Jogador", "pvp"),
    ("Simulação", "sim"),
]


def criar_tabuleiro():
    return [[AGUA for _ in range(TAMANHO)] for _ in range(TAMANHO)]


def posicionar_navio(tabuleiro, tamanho_navio):
    while True:
        linha = random.randint(0, TAMANHO - 1)
        coluna = random.randint(0, TAMANHO - 1)
        direcao = random.choice(["horizontal", "vertical"])
        coords = []
        for passo in range(tamanho_navio):
            nova_linha = linha + (passo if direcao == "vertical" else 0)
            nova_coluna = coluna + (passo if direcao == "horizontal" else 0)
            if nova_linha >= TAMANHO or nova_coluna >= TAMANHO:
                coords = []
                break
            if tabuleiro[nova_linha][nova_coluna] != AGUA:
                coords = []
                break
            coords.append((nova_linha, nova_coluna))
        if coords:
            for linha_atual, coluna_atual in coords:
                tabuleiro[linha_atual][coluna_atual] = NAVIO
            return coords


def posicionar_navios(tabuleiro):
    navios = []
    for nome, tamanho in FROTA:
        coords = posicionar_navio(tabuleiro, tamanho)
        navios.append({"nome": nome, "tamanho": tamanho, "coords": coords})
    return navios


def contar_navios_restantes(tabuleiro):
    return sum(posicao == NAVIO for linha in tabuleiro for posicao in linha)


def tamanhos_restantes(navios, tabuleiro):
    return [navio["tamanho"] for navio in navios if any(tabuleiro[l][c] == NAVIO for l, c in navio["coords"])]


def formatar_tamanhos(tamanhos):
    if not tamanhos:
        return "Nenhuma nave restante"
    return ", ".join(str(t) for t in sorted(tamanhos, reverse=True))


class StarTrekBattleshipGUI:
    def __init__(self, master):
        self.master = master
        master.title("Batalha Naval Star Trek")
        master.configure(bg="#0b1a2f")

        self.status_text = tk.StringVar()
        self.status_text.set("Missão: Neutralizar a frota Klingon.")

        self.mode = None
        self.active_player = 0
        self.player_names = ["Capitão 1", "Capitão 2"]

        self.carregar_imagens()
        self.criar_widgets()
        self.mostrar_menu()

    def carregar_imagens(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        img_dir = os.path.join(base_dir, "assets", "images")
        self.images = {
            "water": tk.PhotoImage(file=os.path.join(img_dir, "water.png")),
            "federation": tk.PhotoImage(file=os.path.join(img_dir, "federation.png")),
            "klingon": tk.PhotoImage(file=os.path.join(img_dir, "klingon.png")),
            "hit": tk.PhotoImage(file=os.path.join(img_dir, "hit.png")),
            "miss": tk.PhotoImage(file=os.path.join(img_dir, "miss.png")),
        }

    def criar_widgets(self):
        título = tk.Label(
            self.master,
            text="MISSÃO ESTELAR: BATALHA NAVAL",
            font=("Helvetica", 16, "bold"),
            fg="#aad8ff",
            bg="#0b1a2f",
        )
        título.pack(pady=10)

        status = tk.Label(
            self.master,
            textvariable=self.status_text,
            font=("Helvetica", 11),
            fg="#cce7ff",
            bg="#0b1a2f",
            wraplength=620,
            justify="center",
        )
        status.pack(pady=4)

        self.menu_frame = tk.Frame(self.master, bg="#0b1a2f")
        menu_label = tk.Label(
            self.menu_frame,
            text="Selecione a modalidade de missão:",
            font=("Helvetica", 12, "bold"),
            fg="#cce7ff",
            bg="#0b1a2f",
        )
        menu_label.pack(pady=6)

        for texto, modo in MODOS:
            botao = tk.Button(
                self.menu_frame,
                text=texto,
                font=("Helvetica", 11, "bold"),
                bg="#2680c6",
                fg="#ffffff",
                activebackground="#3e8ccf",
                width=22,
                command=lambda m=modo: self.iniciar_missao(m),
            )
            botao.pack(pady=4)

        self.game_frame = tk.Frame(self.master, bg="#0b1a2f")
        board_frame = tk.Frame(self.game_frame, bg="#0b1a2f")
        board_frame.pack(padx=10, pady=10)

        self.enemigo_frame = tk.LabelFrame(
            board_frame,
            text="Setor inimigo",
            fg="#ffdd75",
            bg="#0b1a2f",
            labelanchor="n",
            font=("Helvetica", 12, "bold"),
            padx=5,
            pady=5,
        )
        self.enemigo_frame.grid(row=0, column=0, padx=10)

        self.jogador_frame = tk.LabelFrame(
            board_frame,
            text="Seu setor",
            fg="#75d7ff",
            bg="#0b1a2f",
            labelanchor="n",
            font=("Helvetica", 12, "bold"),
            padx=5,
            pady=5,
        )
        self.jogador_frame.grid(row=0, column=1, padx=10)

        self.botões_inimigos = []
        for linha in range(TAMANHO):
            row = []
            for coluna in range(TAMANHO):
                btn = tk.Button(
                    self.enemigo_frame,
                    image=self.images["water"],
                    width=32,
                    height=32,
                    bg="#164575",
                    activebackground="#3b6eb8",
                    command=lambda l=linha, c=coluna: self.atacar(l, c),
                )
                btn.grid(row=linha, column=coluna, padx=1, pady=1)
                row.append(btn)
            self.botões_inimigos.append(row)

        self.labels_jogador = []
        for linha in range(TAMANHO):
            row = []
            for coluna in range(TAMANHO):
                label = tk.Label(
                    self.jogador_frame,
                    image=self.images["water"],
                    width=32,
                    height=32,
                    bg="#1f3e6d",
                    relief="ridge",
                    borderwidth=1,
                )
                label.grid(row=linha, column=coluna, padx=1, pady=1)
                row.append(label)
            self.labels_jogador.append(row)

        painel_inferior = tk.Frame(self.game_frame, bg="#0b1a2f")
        painel_inferior.pack(pady=10)

        self.frota_label = tk.Label(
            painel_inferior,
            text="Tamanhos restantes: Federação 4, 3, 2, 2 | Inimigo 4, 3, 2, 2",
            font=("Helvetica", 11),
            fg="#cce7ff",
            bg="#0b1a2f",
        )
        self.frota_label.pack(pady=4)

        botoes = tk.Frame(painel_inferior, bg="#0b1a2f")
        botoes.pack(pady=4)

        reiniciar_btn = tk.Button(
            botoes,
            text="Reiniciar Missão",
            font=("Helvetica", 10, "bold"),
            bg="#2680c6",
            fg="#ffffff",
            activebackground="#3e8ccf",
            command=self.reiniciar_jogo,
        )
        reiniciar_btn.pack(side="left", padx=6)

        voltar_btn = tk.Button(
            botoes,
            text="Menu Principal",
            font=("Helvetica", 10, "bold"),
            bg="#6a4e98",
            fg="#ffffff",
            activebackground="#8b6dd4",
            command=self.mostrar_menu,
        )
        voltar_btn.pack(side="left", padx=6)

        sair_btn = tk.Button(
            botoes,
            text="Sair",
            font=("Helvetica", 10, "bold"),
            bg="#b83232",
            fg="#ffffff",
            activebackground="#d24a4a",
            command=self.master.quit,
        )
        sair_btn.pack(side="left", padx=6)

    def mostrar_menu(self):
        self.game_frame.pack_forget()
        self.menu_frame.pack(pady=10)
        self.status_text.set("Missão: escolha sua modalidade e prepare a frota.")

    def iniciar_missao(self, modo):
        self.mode = modo
        self.active_player = 0
        self.menu_frame.pack_forget()
        self.game_frame.pack()
        self.reiniciar_jogo()

    def reiniciar_jogo(self):
        self.tabuleiro_1 = criar_tabuleiro()
        self.tabuleiro_2 = criar_tabuleiro()
        self.navios_1 = posicionar_navios(self.tabuleiro_1)
        self.navios_2 = posicionar_navios(self.tabuleiro_2)
        self.jogo_terminado = False
        self.status_text.set("Missão reiniciada: prepare-se para atacar o inimigo.")
        self.atualizar_telas()
        if self.mode == "sim":
            self.master.after(1000, self.simulacao)

    def obter_boards(self):
        if self.mode == "pvp":
            inimigo = self.tabuleiro_2 if self.active_player == 0 else self.tabuleiro_1
            jogador = self.tabuleiro_1 if self.active_player == 0 else self.tabuleiro_2
            navios_inimigo = self.navios_2 if self.active_player == 0 else self.navios_1
            navios_jogador = self.navios_1 if self.active_player == 0 else self.navios_2
        else:
            inimigo = self.tabuleiro_2
            jogador = self.tabuleiro_1
            navios_inimigo = self.navios_2
            navios_jogador = self.navios_1
        return inimigo, jogador, navios_inimigo, navios_jogador

    def tocar_som(self, tipo):
        if winsound:
            if tipo == "hit":
                winsound.Beep(880, 120)
            elif tipo == "miss":
                winsound.Beep(440, 90)
            elif tipo == "enemy_hit":
                winsound.Beep(660, 110)
            elif tipo == "enemy_miss":
                winsound.Beep(350, 80)
            elif tipo == "end":
                winsound.Beep(988, 130)
                winsound.Beep(784, 130)
        else:
            self.master.bell()

    def atualizar_telas(self):
        inimigo, jogador, navios_inimigo, navios_jogador = self.obter_boards()
        for linha in range(TAMANHO):
            for coluna in range(TAMANHO):
                estado = inimigo[linha][coluna]
                btn = self.botões_inimigos[linha][coluna]
                if estado == TIRO_ACERTO:
                    btn.configure(image=self.images["hit"], bg="#b83232")
                elif estado == TIRO_AGUA:
                    btn.configure(image=self.images["miss"], bg="#82a6d6")
                else:
                    btn.configure(image=self.images["water"], bg="#164575")

                valor = jogador[linha][coluna]
                label = self.labels_jogador[linha][coluna]
                if valor == NAVIO:
                    label.configure(image=self.images["federation"], bg="#2b6f48")
                elif valor == TIRO_ACERTO:
                    label.configure(image=self.images["hit"], bg="#b83232")
                elif valor == TIRO_AGUA:
                    label.configure(image=self.images["miss"], bg="#82a6d6")
                else:
                    label.configure(image=self.images["water"], bg="#1f3e6d")

        tam_inimigo = formatar_tamanhos(tamanhos_restantes(navios_inimigo, inimigo))
        tam_jogador = formatar_tamanhos(tamanhos_restantes(navios_jogador, jogador))
        self.frota_label.configure(
            text=f"Tamanhos restantes: {self.player_names[self.active_player]} {tam_jogador} | Inimigo {tam_inimigo}"
        )

        self.current_images = self.images

    def atacar(self, linha, coluna):
        if self.jogo_terminado or self.mode == "sim":
            return

        inimigo, jogador, navios_inimigo, navios_jogador = self.obter_boards()
        valor_atual = inimigo[linha][coluna]
        if valor_atual in (TIRO_AGUA, TIRO_ACERTO):
            self.status_text.set("Setor já atacado. Recalibre os sistemas e tente outro alvo.")
            return

        if valor_atual == NAVIO:
            inimigo[linha][coluna] = TIRO_ACERTO
            self.status_text.set(f"{self.player_names[self.active_player]} acertou um navio inimigo!")
            self.tocar_som("hit")
        else:
            inimigo[linha][coluna] = TIRO_AGUA
            self.status_text.set("Tiro na água. O inimigo evadiu o ataque.")
            self.tocar_som("miss")

        self.atualizar_telas()
        if not tamanhos_restantes(navios_inimigo, inimigo):
            self.finalizar_missao(f"{self.player_names[self.active_player]} venceu! Todas as naves inimigas foram destruídas.")
            return

        if self.mode == "pvc":
            self.master.after(700, self.turno_computador)
        else:
            self.active_player = 1 - self.active_player
            self.status_text.set(f"Turno de {self.player_names[self.active_player]}.")
            self.atualizar_telas()

    def turno_computador(self):
        if self.jogo_terminado:
            return

        inimigo = self.tabuleiro_2
        jogador = self.tabuleiro_1
        while True:
            linha = random.randint(0, TAMANHO - 1)
            coluna = random.randint(0, TAMANHO - 1)
            if jogador[linha][coluna] not in (TIRO_AGUA, TIRO_ACERTO):
                break

        if jogador[linha][coluna] == NAVIO:
            jogador[linha][coluna] = TIRO_ACERTO
            self.status_text.set("O Klingon acertou sua nave.")
            self.tocar_som("enemy_hit")
        else:
            jogador[linha][coluna] = TIRO_AGUA
            self.status_text.set("O Klingon errou. Escudos mantidos.")
            self.tocar_som("enemy_miss")

        self.atualizar_telas()
        if not tamanhos_restantes(self.navios_1, jogador):
            self.finalizar_missao("Missão fracassada. A Federação perdeu a batalha.")

    def simulacao(self):
        if self.jogo_terminado:
            return

        acao = random.choice([0, 1])
        if acao == 0:
            self.turno_computador()
        else:
            self.turno_computador()

        if not self.jogo_terminado:
            self.master.after(800, self.simulacao)

    def finalizar_missao(self, mensagem):
        self.jogo_terminado = True
        self.status_text.set(mensagem)
        self.tocar_som("end")
        messagebox.showinfo("Fim da Missão", mensagem)


if __name__ == "__main__":
    root = tk.Tk()
    app = StarTrekBattleshipGUI(root)
    root.mainloop()