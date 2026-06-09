import random
import os
import time

TAMANHO = 10
TAMANHOS_NAVIOS = [4, 3, 2, 1]
AGUA = "~"
NAVIO = "N"
TIRO_AGUA = "O"
TIRO_ACERTO = "X"


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def criar_tabuleiro():
    tabuleiro = []
    for _ in range(TAMANHO):
        linha = []
        for _ in range(TAMANHO):
            linha.append(AGUA)
        tabuleiro.append(linha)
    return tabuleiro


def exibir_tabuleiro(tabuleiro, esconder_navios=False):
    print("  ", end="")
    for coluna in range(TAMANHO):
        print(coluna, end=" ")
    print()

    for indice_linha in range(TAMANHO):
        print(indice_linha, end=" ")
        for indice_coluna in range(TAMANHO):
            valor = tabuleiro[indice_linha][indice_coluna]
            if esconder_navios and valor == NAVIO:
                print(AGUA, end=" ")
            else:
                print(valor, end=" ")
        print()


def posicao_valida(tabuleiro, linha, coluna, tamanho_navio, direcao):
    for passo in range(tamanho_navio):
        nova_linha = linha
        nova_coluna = coluna

        if direcao == "horizontal":
            nova_coluna += passo
        else:
            nova_linha += passo

        if nova_linha >= TAMANHO or nova_coluna >= TAMANHO:
            return False

        if tabuleiro[nova_linha][nova_coluna] != AGUA:
            return False

    return True


def posicionar_navio(tabuleiro, tamanho_navio):
    while True:
        linha = random.randint(0, TAMANHO - 1)
        coluna = random.randint(0, TAMANHO - 1)
        direcao = random.choice(["horizontal", "vertical"])

        if posicao_valida(tabuleiro, linha, coluna, tamanho_navio, direcao):
            for passo in range(tamanho_navio):
                if direcao == "horizontal":
                    tabuleiro[linha][coluna + passo] = NAVIO
                else:
                    tabuleiro[linha + passo][coluna] = NAVIO
            break


def posicionar_navios(tabuleiro):
    for tamanho_navio in TAMANHOS_NAVIOS:
        posicionar_navio(tabuleiro, tamanho_navio)


def pedir_coordenada(mensagem):
    while True:
        try:
            valor = int(input(mensagem))
            if 0 <= valor < TAMANHO:
                return valor
            print(f"Digite um numero entre 0 e {TAMANHO - 1}.")
        except ValueError:
            print("Entrada invalida. Digite um numero inteiro.")


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
    contador = 0
    for linha in tabuleiro:
        for posicao in linha:
            if posicao == NAVIO:
                contador += 1
    return contador


def turno_jogador(nome_jogador, tabuleiro_inimigo):
    print(f"\nTurno de {nome_jogador}")
    linha = pedir_coordenada("Digite a linha do tiro: ")
    coluna = pedir_coordenada("Digite a coluna do tiro: ")

    resultado = realizar_tiro(tabuleiro_inimigo, linha, coluna)

    if resultado == "acerto":
        print("Acertou um navio!")
    elif resultado == "agua":
        print("Tiro na agua!")
    else:
        print("Voce ja atirou nessa posicao.")


def turno_computador(tabuleiro_inimigo, nome="Computador"):
    linha, coluna = computador_escolhe_tiro(tabuleiro_inimigo)
    print(f"\n{nome} atirou em ({linha}, {coluna})")
    resultado = realizar_tiro(tabuleiro_inimigo, linha, coluna)

    if resultado == "acerto":
        print(f"{nome} acertou um navio!")
    else:
        print(f"{nome} atingiu a agua.")


def preparar_jogo():
    tabuleiro_1 = criar_tabuleiro()
    tabuleiro_2 = criar_tabuleiro()
    posicionar_navios(tabuleiro_1)
    posicionar_navios(tabuleiro_2)
    return tabuleiro_1, tabuleiro_2


def jogo_jogador_vs_jogador():
    tabuleiro_1, tabuleiro_2 = preparar_jogo()

    while True:
        print("\nTabuleiro do Jogador 2")
        exibir_tabuleiro(tabuleiro_2, esconder_navios=True)
        turno_jogador("Jogador 1", tabuleiro_2)
        if contar_navios_restantes(tabuleiro_2) == 0:
            print("\nJogador 1 venceu!")
            break
        input("Pressione Enter para passar o turno.")
        limpar_tela()

        print("\nTabuleiro do Jogador 1")
        exibir_tabuleiro(tabuleiro_1, esconder_navios=True)
        turno_jogador("Jogador 2", tabuleiro_1)
        if contar_navios_restantes(tabuleiro_1) == 0:
            print("\nJogador 2 venceu!")
            break
        input("Pressione Enter para passar o turno.")
        limpar_tela()


def jogo_computador_vs_computador():
    tabuleiro_1, tabuleiro_2 = preparar_jogo()
    rodada = 1

    while True:
        print(f"\nRodada {rodada}")
        print("\nTabuleiro do Computador 1")
        exibir_tabuleiro(tabuleiro_1)
        print("\nTabuleiro do Computador 2")
        exibir_tabuleiro(tabuleiro_2)

        turno_computador(tabuleiro_2, "Computador 1")
        if contar_navios_restantes(tabuleiro_2) == 0:
            print("\nComputador 1 venceu!")
            break
        time.sleep(1)

        turno_computador(tabuleiro_1, "Computador 2")
        if contar_navios_restantes(tabuleiro_1) == 0:
            print("\nComputador 2 venceu!")
            break
        time.sleep(1)
        rodada += 1

    print("\nTabuleiro final do Computador 1")
    exibir_tabuleiro(tabuleiro_1)
    print("\nTabuleiro final do Computador 2")
    exibir_tabuleiro(tabuleiro_2)


def jogo_computador_vs_jogador():
    tabuleiro_computador, tabuleiro_jogador = preparar_jogo()

    while True:
        print("\nSeu alvo")
        exibir_tabuleiro(tabuleiro_computador, esconder_navios=True)
        turno_jogador("Jogador", tabuleiro_computador)
        if contar_navios_restantes(tabuleiro_computador) == 0:
            print("\nParabens! Voce venceu o computador!")
            break

        print("\nTabuleiro do jogador")
        exibir_tabuleiro(tabuleiro_jogador)
        input("Pressione Enter para o computador jogar.")
        turno_computador(tabuleiro_jogador)
        if contar_navios_restantes(tabuleiro_jogador) == 0:
            print("\nO computador venceu!")
            break


def menu():
    while True:
        print("\n=== BATALHA NAVAL ===")
        print(f"Navios em jogo: {TAMANHOS_NAVIOS}")
        print("1. Jogador vs Jogador")
        print("2. Computador vs Computador")
        print("3. Computador vs Jogador")
        print("4. Sair")

        opcao = input("Escolha uma modalidade: ")

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
            print("Encerrando o jogo.")
            print("Obrigado por jogar!")
            print("Criado por Guilherme Bettio e Gabriel Kulik")
            break
        else:
            print("Opcao invalida. Tente novamente.")

menu()