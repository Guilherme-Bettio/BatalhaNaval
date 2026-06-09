import random

# Configurações do jogo
TAMANHO = 5
NUM_NAVIOS = 3

def criar_tabuleiro():
    # Cria uma matriz (lista de listas) preenchida com "~" (água)
    return [["~" for _ in range(TAMANHO)] for _ in range(TAMANHO)]

def exibir_tabuleiro(tabuleiro):
    # Imprime os números das colunas
    print("\n  0 1 2 3 4")
    for i, linha in enumerate(tabuleiro):
        # Imprime o número da linha e o conteúdo da matriz unido por espaços
        print(f"{i} {' '.join(linha)}")

def posicionar_navios():
    # Cria uma lista de coordenadas (vetores) para os navios
    navios = []
    while len(navios) < NUM_NAVIOS:
        linha = random.randint(0, TAMANHO - 1)
        coluna = random.randint(0, TAMANHO - 1)
        if (linha, coluna) not in navios:
            navios.append((linha, coluna))
    return navios

def iniciar_jogo():
    tabuleiro = criar_tabuleiro()
    coordenadas_navios = posicionar_navios()
    acertos = 0

    print("=== BATALHA NAVAL SIMPLIFICADA ===")
    print(f"Existem {NUM_NAVIOS} navios escondidos no mar 5x5.")

    while acertos < NUM_NAVIOS:
        exibir_tabuleiro(tabuleiro)
        
        try:
            # Pede a entrada do usuário
            lin = int(input("\nEscolha a linha (0-4): "))
            col = int(input("Escolha a coluna (0-4): "))

            # Verifica se acertou um navio
            if (lin, col) in coordenadas_navios:
                if tabuleiro[lin][col] == "X":
                    print("Você já acertou esta posição!")
                else:
                    print("BOOM! Você acertou um navio!")
                    tabuleiro[lin][col] = "X" # X indica acerto
                    acertos += 1
            else:
                print("Água... tente novamente.")
                tabuleiro[lin][col] = "O" # O indica erro (tiro na água)
        
        except (ValueError, IndexError):
            print("Erro: Digite apenas números entre 0 e 4.")

    exibir_tabuleiro(tabuleiro)
    print("\nParabéns! Você afundou toda a frota!")

if __name__ == "__main__":
    iniciar_jogo()