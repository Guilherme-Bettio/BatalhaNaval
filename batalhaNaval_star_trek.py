import random
import os
import time

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

ANSI_RESET = "\033[0m"
ANSI_BLUE = "\033[34m"
ANSI_CYAN = "\033[36m"
ANSI_GREEN = "\033[32m"
ANSI_RED = "\033[31m"
ANSI_YELLOW = "\033[33m"
ANSI_MAGENTA = "\033[35m"


def habilitar_ansi():
    if os.name == "nt":
        os.system("")


def tocar_som(tipo):
    if winsound:
        if tipo == "hit":
            winsound.Beep(880, 120)
        elif tipo == "miss":
            winsound.Beep(440, 90)
        elif tipo == "repeat":
            winsound.Beep(330, 80)
        elif tipo == "end":
            winsound.Beep(988, 140)
            winsound.Beep(784, 140)
    else:
        print("\a", end="", flush=True)


def cor(texto, codigo):
    return f"{codigo}{texto}{ANSI_RESET}"


def cabecalho_startrek():
    print(cor("=== MISSÃO ESTELAR: BATALHA NAVAL STAR TREK ===", ANSI_CYAN))
    print(cor("Federação Unida dos Planetas contra a ameaça Klingon.", ANSI_BLUE))
    print(cor("No comando da Ponte, prepare-se para atacar os segmentos inimigos.", ANSI_BLUE))
    print()


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def criar_tabuleiro():
    return [[AGUA for _ in range(TAMANHO)] for _ in range(TAMANHO)]


def exibir_tabuleiro(tabuleiro, esconder_navios=False):
    print(cor("   " + " ".join(str(i) for i in range(TAMANHO)), ANSI_YELLOW))
    for linha in range(TAMANHO):
        linha_str = [
            AGUA if esconder_navios and valor == NAVIO else valor
            for valor in tabuleiro[linha]
        ]
        linha_colorida = []
        for valor in linha_str:
            if valor == TIRO_ACERTO:
                linha_colorida.append(cor(valor, ANSI_RED))
            elif valor == TIRO_AGUA:
                linha_colorida.append(cor(valor, ANSI_BLUE))
            elif valor == NAVIO:
                linha_colorida.append(cor(valor, ANSI_GREEN))
            else:
                linha_colorida.append(cor(valor, ANSI_CYAN))
        print(cor(str(linha), ANSI_YELLOW), " ".join(linha_colorida))


def posicao_valida(tabuleiro, linha, coluna, tamanho_navio, direcao):
    for passo in range(tamanho_navio):
        nova_linha = linha + (passo if direcao == "vertical" else 0)
        nova_coluna = coluna + (passo if direcao == "horizontal" else 0)
        if not (0 <= nova_linha < TAMANHO and 0 <= nova_coluna < TAMANHO):
            return False
        if tabuleiro[nova_linha][nova_coluna] != AGUA:
            return False
    return True


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
            for l, c in coords:
                tabuleiro[l][c] = NAVIO
            return coords


def posicionar_navios(tabuleiro):
    navios = []
    for nome, tamanho in FROTA:
        coords = posicionar_navio(tabuleiro, tamanho)
        navios.append({"nome": nome, "tamanho": tamanho, "coords": coords})
    return navios


def pedir_coordenada(mensagem):
    while True:
        try:
            valor = int(input(cor(mensagem, ANSI_GREEN)))
            if 0 <= valor < TAMANHO:
                return valor
            print(cor(f"Digite um número entre 0 e {TAMANHO - 1}.", ANSI_YELLOW))
        except ValueError:
            print(cor("Entrada inválida. Digite um número inteiro.", ANSI_YELLOW))


def realizar_tiro(tabuleiro, linha, coluna):
    if tabuleiro[linha][coluna] == NAVIO:
        tabuleiro[linha][coluna] = TIRO_ACERTO
        return "acerto"
    if tabuleiro[linha][coluna] == AGUA:
        tabuleiro[linha][coluna] = TIRO_AGUA
        return "agua"
    return "repetido"


def computador_escolhe_tiro(tabuleiro):
    while True:
        linha = random.randint(0, TAMANHO - 1)
        coluna = random.randint(0, TAMANHO - 1)
        if tabuleiro[linha][coluna] not in (TIRO_AGUA, TIRO_ACERTO):
            return linha, coluna


def contar_navios_restantes(tabuleiro):
    return sum(posicao == NAVIO for linha in tabuleiro for posicao in linha)


def tamanhos_restantes(navios, tabuleiro):
    return [navio["tamanho"] for navio in navios if any(tabuleiro[l][c] == NAVIO for l, c in navio["coords"])]


def formatar_tamanhos(tamanhos):
    if not tamanhos:
        return "Nenhuma nave restante"
    return ", ".join(str(t) for t in sorted(tamanhos, reverse=True))


def turno_jogador(nome_jogador, tabuleiro_inimigo):
    print(cor(f"\n{nome_jogador}, prepare-se para disparar os torpedos fotônicos.", ANSI_CYAN))
    linha = pedir_coordenada("Digite a linha do tiro: ")
    coluna = pedir_coordenada("Digite a coluna do tiro: ")
    resultado = realizar_tiro(tabuleiro_inimigo, linha, coluna)
    if resultado == "acerto":
        tocar_som("hit")
        print(cor("Impacto crítico! Cruzador Klingon atingido.", ANSI_RED))
    elif resultado == "agua":
        tocar_som("miss")
        print(cor("Tiro na água. O alvo mudou de curso.", ANSI_BLUE))
    else:
        tocar_som("repeat")
        print(cor("Setor já atacado. Recalibrando sensores.", ANSI_YELLOW))


def turno_computador(tabuleiro_inimigo, nome="Klingon AI"):
    linha, coluna = computador_escolhe_tiro(tabuleiro_inimigo)
    print(cor(f"\n{nome} disparou em ({linha}, {coluna})", ANSI_CYAN))
    resultado = realizar_tiro(tabuleiro_inimigo, linha, coluna)
    if resultado == "acerto":
        tocar_som("hit")
        print(cor(f"{nome} acertou uma nave! Alerta de dano. ", ANSI_RED))
    else:
        tocar_som("miss")
        print(cor(f"{nome} errou. O alvo continua em curso.", ANSI_BLUE))


def preparar_jogo():
    tabuleiro_1 = criar_tabuleiro()
    tabuleiro_2 = criar_tabuleiro()
    navios_1 = posicionar_navios(tabuleiro_1)
    navios_2 = posicionar_navios(tabuleiro_2)
    return tabuleiro_1, navios_1, tabuleiro_2, navios_2


def jogo_jogador_vs_jogador():
    tabuleiro_1, navios_1, tabuleiro_2, navios_2 = preparar_jogo()
    while True:
        print(cor("\nSetor inimigo (Jogador 2)", ANSI_MAGENTA))
        print(cor(f"Tamanhos restantes do inimigo: {formatar_tamanhos(tamanhos_restantes(navios_2, tabuleiro_2))}", ANSI_YELLOW))
        exibir_tabuleiro(tabuleiro_2, esconder_navios=True)
        turno_jogador("Oficial 1", tabuleiro_2)
        if not tamanhos_restantes(navios_2, tabuleiro_2):
            print(cor("\nOficial 1 venceu! A Federação triunfou.", ANSI_GREEN))
            break
        input(cor("Pressione Enter para passar o turno.", ANSI_YELLOW))
        limpar_tela()
        print(cor("\nSetor inimigo (Jogador 1)", ANSI_MAGENTA))
        print(cor(f"Tamanhos restantes do inimigo: {formatar_tamanhos(tamanhos_restantes(navios_1, tabuleiro_1))}", ANSI_YELLOW))
        exibir_tabuleiro(tabuleiro_1, esconder_navios=True)
        turno_jogador("Oficial 2", tabuleiro_1)
        if not tamanhos_restantes(navios_1, tabuleiro_1):
            print(cor("\nOficial 2 venceu! A Ponte foi capturada.", ANSI_RED))
            break
        input(cor("Pressione Enter para passar o turno.", ANSI_YELLOW))
        limpar_tela()


def jogo_computador_vs_computador():
    tabuleiro_1, navios_1, tabuleiro_2, navios_2 = preparar_jogo()
    rodada = 1
    while True:
        print(cor(f"\nRodada {rodada}", ANSI_MAGENTA))
        print(cor(f"Tamanhos restantes frota 1: {formatar_tamanhos(tamanhos_restantes(navios_1, tabuleiro_1))}", ANSI_YELLOW))
        print(cor(f"Tamanhos restantes frota 2: {formatar_tamanhos(tamanhos_restantes(navios_2, tabuleiro_2))}", ANSI_YELLOW))
        print(cor("\nFrota 1", ANSI_YELLOW))
        exibir_tabuleiro(tabuleiro_1)
        print(cor("\nFrota 2", ANSI_YELLOW))
        exibir_tabuleiro(tabuleiro_2)
        turno_computador(tabuleiro_2, "USS Klingon")
        if not tamanhos_restantes(navios_2, tabuleiro_2):
            print(cor("\nA USS Klingon venceu! A Federação está em perigo.", ANSI_RED))
            break
        time.sleep(1)
        turno_computador(tabuleiro_1, "USS Romulano")
        if not tamanhos_restantes(navios_1, tabuleiro_1):
            print(cor("\nA USS Romulana venceu! A Federação perdeu nesta simulação.", ANSI_RED))
            break
        time.sleep(1)
        rodada += 1
    print(cor("\nTabuleiro final da Frota 1", ANSI_YELLOW))
    exibir_tabuleiro(tabuleiro_1)
    print(cor("\nTabuleiro final da Frota 2", ANSI_YELLOW))
    exibir_tabuleiro(tabuleiro_2)


def jogo_computador_vs_jogador():
    tabuleiro_computador, navios_computador, tabuleiro_jogador, navios_jogador = preparar_jogo()
    while True:
        print(cor("\nAlvo dos Klingons", ANSI_MAGENTA))
        print(cor(f"Tamanhos restantes do inimigo: {formatar_tamanhos(tamanhos_restantes(navios_computador, tabuleiro_computador))}", ANSI_YELLOW))
        exibir_tabuleiro(tabuleiro_computador, esconder_navios=True)
        turno_jogador("Capitão", tabuleiro_computador)
        if not tamanhos_restantes(navios_computador, tabuleiro_computador):
            print(cor("\nParabéns, Capitão! A Federação venceu a batalha.", ANSI_GREEN))
            break
        print(cor("\nEscudo da ponte sob ataque.", ANSI_MAGENTA))
        print(cor(f"Tamanhos restantes da Federação: {formatar_tamanhos(tamanhos_restantes(navios_jogador, tabuleiro_jogador))}", ANSI_YELLOW))
        exibir_tabuleiro(tabuleiro_jogador)
        input(cor("Pressione Enter para ativar a IA inimiga.", ANSI_YELLOW))
        turno_computador(tabuleiro_jogador)
        if not tamanhos_restantes(navios_jogador, tabuleiro_jogador):
            print(cor("\nAlerta! O Klingon destruiu sua frota.", ANSI_RED))
            break


def menu():
    habilitar_ansi()
    limpar_tela()
    cabecalho_startrek()
    while True:
        print(cor("=== PONTE DA USS ENTERPRISE ===", ANSI_MAGENTA))
        print(cor("Escolha sua missão:", ANSI_BLUE))
        print(cor("1. Oficial contra Oficial", ANSI_YELLOW))
        print(cor("2. Simulação de treino", ANSI_YELLOW))
        print(cor("3. Treino contra a IA Klingon", ANSI_YELLOW))
        print(cor("4. Sair da missão", ANSI_YELLOW))
        opcao = input(cor("Digite a opção: ", ANSI_GREEN))
        if opcao == "1":
            limpar_tela()
            jogo_jogador_vs_jogador()
        elif opcao == "2":
            limpar_tela()
            jogo_computador_vs_computador()
        elif opcao == "3":
            limpar_tela()
            jogo_computador_vs_jogador()
        elif opcao == "4":
            print(cor("Encerrando missão. Até a próxima jornada estelar.", ANSI_CYAN))
            break
        else:
            print(cor("Opção inválida. Tente novamente.", ANSI_YELLOW))


if __name__ == "__main__":
    menu()
