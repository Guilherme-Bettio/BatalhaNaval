import random
import os
import time

# Challenge Mode Ships Definition
NAVIOS_DESAFIO = [
    {"id": "P", "nome": "Porta-aviões", "tamanho": 5},
    {"id": "T", "nome": "Navio-tanque", "tamanho": 4},
    {"id": "C", "nome": "Contratorpedeiro", "tamanho": 3},
    {"id": "S", "nome": "Submarino", "tamanho": 2},
    {"id": "D", "nome": "Destroier", "tamanho": 1}
]

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

def criar_tabuleiro(linhas, colunas):
    tabuleiro = []
    for _ in range(linhas):
        linha = []
        for _ in range(colunas):
            linha.append(0)
        tabuleiro.append(linha)
    return tabuleiro

def exibir_tabuleiro(tabuleiro, titulo, embarcacoes_restantes):
    print(f"\n{titulo}")
    for linha in tabuleiro:
        print(linha)
    print("-" * 30)
    print(f"Embarcações restantes: {embarcacoes_restantes}")

def pedir_coordenada_tiro(linhas, colunas, tabuleiro_feedback):
    while True:
        try:
            linha = int(input("Qual linha deseja atacar? "))
            coluna = int(input("Qual coluna deseja atacar? "))
            
            if not (1 <= linha <= linhas and 1 <= coluna <= colunas):
                print(f"Coordenadas inválidas! Escolha linha de 1 a {linhas} e coluna de 1 a {colunas}.")
                continue
                
            r, c = linha - 1, coluna - 1
            if tabuleiro_feedback[r][c] in ('X', 'O'):
                print("Você já atacou essa posição! Escolha outra.")
                continue
                
            return r, c
        except ValueError:
            print("Entrada inválida. Digite valores inteiros.")

def pedir_coordenada_tiro_nomeado(jogador, linhas, colunas, tabuleiro_feedback):
    while True:
        try:
            linha = int(input(f"{jogador}: Qual linha deseja atacar? "))
            coluna = int(input(f"{jogador}: Qual coluna deseja atacar? "))
            
            if not (1 <= linha <= linhas and 1 <= coluna <= colunas):
                print(f"Coordenadas inválidas! Escolha linha de 1 a {linhas} e coluna de 1 a {colunas}.")
                continue
                
            r, c = linha - 1, coluna - 1
            if tabuleiro_feedback[r][c] in ('X', 'O'):
                print("Você já atacou essa posição! Escolha outra.")
                continue
                
            return r, c
        except ValueError:
            print("Entrada inválida. Digite valores inteiros.")

def computador_escolhe_tiro(linhas, colunas, tabuleiro_feedback):
    while True:
        r = random.randint(0, linhas - 1)
        c = random.randint(0, colunas - 1)
        if tabuleiro_feedback[r][c] not in ('X', 'O'):
            return r, c

def posicionar_jogador_simplificado(linhas, colunas):
    tabuleiro = criar_tabuleiro(linhas, colunas)
    print("\n--- POSICIONANDO SUAS EMBARCAÇÕES (Modo Simplificado) ---")
    print("Você deve posicionar 5 de suas embarcações (cada uma ocupando 1 posição) no seu tabuleiro.")
    
    for i in range(1, 6):
        while True:
            try:
                print(f"\nEmbarcação {i}:")
                linha = int(input(f"Digite a linha (1-{linhas}): "))
                coluna = int(input(f"Digite a coluna (1-{colunas}): "))
                
                if not (1 <= linha <= linhas and 1 <= coluna <= colunas):
                    print(f"Coordenadas inválidas! A linha deve ser entre 1-{linhas} e a coluna entre 1-{colunas}.")
                    continue
                    
                r, c = linha - 1, coluna - 1
                if tabuleiro[r][c] == 1:
                    print("Você já colocou uma embarcação nessa posição! Escolha outra.")
                    continue
                    
                tabuleiro[r][c] = 1
                break
            except ValueError:
                print("Entrada inválida. Digite valores inteiros.")
    return tabuleiro

def posicionar_computador_simplificado(linhas, colunas):
    tabuleiro = criar_tabuleiro(linhas, colunas)
    posicionados = 0
    while posicionados < 5:
        r = random.randint(0, linhas - 1)
        c = random.randint(0, colunas - 1)
        if tabuleiro[r][c] == 0:
            tabuleiro[r][c] = 1
            posicionados += 1
    return tabuleiro

def validar_posicionamento(tabuleiro, r, c, tamanho, direcao, linhas, colunas):
    posicoes = []
    for i in range(tamanho):
        nr, nc = r, c
        if direcao == 'H':
            nc += i
        else:
            nr += i
            
        if not (0 <= nr < linhas and 0 <= nc < colunas):
            return False, []
            
        if tabuleiro[nr][nc] != 0:
            return False, []
            
        posicoes.append((nr, nc))
    return True, posicoes

def posicionar_jogador_desafio(linhas, colunas):
    tabuleiro = criar_tabuleiro(linhas, colunas)
    status_navios = {}
    
    print("\n--- POSICIONANDO SUAS EMBARCAÇÕES (Modo Desafio) ---")
    for navio in NAVIOS_DESAFIO:
        navio_id = navio["id"]
        nome = navio["nome"]
        tamanho = navio["tamanho"]
        
        while True:
            try:
                print(f"\nPosicionando {nome} (Tamanho: {tamanho})")
                linha = int(input(f"Digite a linha inicial (1-{linhas}): "))
                coluna = int(input(f"Digite a coluna inicial (1-{colunas}): "))
                direcao = input("Digite a direção (H para Horizontal, V para Vertical): ").strip().upper()
                
                if direcao not in ('H', 'V'):
                    print("Direção inválida! Escolha H ou V.")
                    continue
                    
                if not (1 <= linha <= linhas and 1 <= coluna <= colunas):
                    print(f"Coordenadas iniciais inválidas! A linha deve ser entre 1-{linhas} e a coluna entre 1-{colunas}.")
                    continue
                    
                r, c = linha - 1, coluna - 1
                valido, posicoes = validar_posicionamento(tabuleiro, r, c, tamanho, direcao, linhas, colunas)
                if not valido:
                    print("Posicionamento inválido! O navio ultrapassa os limites do tabuleiro ou sobrepõe outra embarcação.")
                    continue
                    
                for nr, nc in posicoes:
                    tabuleiro[nr][nc] = navio_id
                    
                status_navios[navio_id] = {
                    "nome": nome,
                    "posicoes": posicoes
                }
                break
            except ValueError:
                print("Entrada inválida. Digite valores inteiros para linha e coluna.")
                
    return tabuleiro, status_navios

def posicionar_computador_desafio(linhas, colunas):
    tabuleiro = criar_tabuleiro(linhas, colunas)
    status_navios = {}
    
    for navio in NAVIOS_DESAFIO:
        navio_id = navio["id"]
        nome = navio["nome"]
        tamanho = navio["tamanho"]
        
        while True:
            r = random.randint(0, linhas - 1)
            c = random.randint(0, colunas - 1)
            direcao = random.choice(['H', 'V'])
            
            valido, posicoes = validar_posicionamento(tabuleiro, r, c, tamanho, direcao, linhas, colunas)
            if valido:
                for nr, nc in posicoes:
                    tabuleiro[nr][nc] = navio_id
                status_navios[navio_id] = {
                    "nome": nome,
                    "posicoes": posicoes
                }
                break
    return tabuleiro, status_navios

def exibir_fim_jogo(mensagem_vitoria):
    print("\n" + "=" * 50)
    print(mensagem_vitoria)
    print("Jogo desenvolvido por: Guilherme Bettio e Gabriel Kulik.")
    print("Obrigada por jogar nosso jogo!")
    print("=" * 50 + "\n")

def escolher_tamanho_tabuleiro():
    while True:
        print("\n=== Escolha o tamanho do tabuleiro ===")
        print("1. 5x10 (Padrão recomendado)")
        print("2. 10x10")
        opcao = input("Opção: ").strip()
        if opcao == "1":
            return 5, 10
        elif opcao == "2":
            return 10, 10
        else:
            print("Opção inválida. Digite 1 ou 2.")

def jogo_simplificado(linhas, colunas):
    tabuleiro_pos_jogador = posicionar_jogador_simplificado(linhas, colunas)
    tabuleiro_pos_computador = posicionar_computador_simplificado(linhas, colunas)
    
    tabuleiro_fb_jogador = criar_tabuleiro(linhas, colunas)
    tabuleiro_fb_computador = criar_tabuleiro(linhas, colunas)
    
    embarcacoes_jogador = 5
    embarcacoes_computador = 5
    
    limpar_tela()
    print("Bem vindo ao Batalha Naval!")
    
    while True:
        # Exibe os tabuleiros
        exibir_tabuleiro(tabuleiro_fb_computador, "Tabuleiro do Computador", embarcacoes_computador)
        exibir_tabuleiro(tabuleiro_fb_jogador, "Tabuleiro do Jogador", embarcacoes_jogador)
        
        # Turno do Jogador
        r, c = pedir_coordenada_tiro(linhas, colunas, tabuleiro_fb_computador)
        
        if tabuleiro_pos_computador[r][c] == 1:
            tabuleiro_fb_computador[r][c] = 'X'
            embarcacoes_computador -= 1
            print(f"\nParabéns! Você acertou! Restam {embarcacoes_computador} embarcações inimigas.\n")
        else:
            tabuleiro_fb_computador[r][c] = 'O'
            print("\nNão houve acerto em nenhuma embarcação inimiga.\n")
            
        if embarcacoes_computador == 0:
            exibir_tabuleiro(tabuleiro_fb_computador, "Tabuleiro do Computador", embarcacoes_computador)
            exibir_tabuleiro(tabuleiro_fb_jogador, "Tabuleiro do Jogador", embarcacoes_jogador)
            exibir_fim_jogo("Parabéns! Você afundou todas as embarcações do inimigo!")
            break
            
        # Turno do Computador
        r_comp, c_comp = computador_escolhe_tiro(linhas, colunas, tabuleiro_fb_jogador)
        print(f"Computador escolheu a linha {r_comp + 1}")
        print(f"Computador escolheu a coluna {c_comp + 1}")
        
        if tabuleiro_pos_jogador[r_comp][c_comp] == 1:
            tabuleiro_fb_jogador[r_comp][c_comp] = 'X'
            embarcacoes_jogador -= 1
            print(f"Computador acertou! Restam {embarcacoes_jogador} embarcações no seu tabuleiro.\n")
        else:
            tabuleiro_fb_jogador[r_comp][c_comp] = 'O'
            print("Computador errou! Não houve acerto em nenhuma de suas embarcações.\n")
            
        if embarcacoes_jogador == 0:
            exibir_tabuleiro(tabuleiro_fb_computador, "Tabuleiro do Computador", embarcacoes_computador)
            exibir_tabuleiro(tabuleiro_fb_jogador, "Tabuleiro do Jogador", embarcacoes_jogador)
            exibir_fim_jogo("O computador afundou todas as suas embarcações! Você perdeu.")
            break
            
        input("Pressione Enter para continuar...")
        limpar_tela()

def jogo_desafio(linhas, colunas):
    tabuleiro_pos_jogador, status_jogador = posicionar_jogador_desafio(linhas, colunas)
    tabuleiro_pos_computador, status_computador = posicionar_computador_desafio(linhas, colunas)
    
    tabuleiro_fb_jogador = criar_tabuleiro(linhas, colunas)
    tabuleiro_fb_computador = criar_tabuleiro(linhas, colunas)
    
    embarcacoes_jogador = 5
    embarcacoes_computador = 5
    
    tiros_jogador = set()
    tiros_computador = set()
    
    limpar_tela()
    print("Bem vindo ao Batalha Naval (Modo Desafio)!")
    
    turno_do_jogador = True
    
    while True:
        # Exibe os tabuleiros
        exibir_tabuleiro(tabuleiro_fb_computador, "Tabuleiro do Computador", embarcacoes_computador)
        exibir_tabuleiro(tabuleiro_fb_jogador, "Tabuleiro do Jogador", embarcacoes_jogador)
        
        if turno_do_jogador:
            # Turno do Jogador
            r, c = pedir_coordenada_tiro(linhas, colunas, tabuleiro_fb_computador)
            tiros_jogador.add((r, c))
            
            navio_atingido = tabuleiro_pos_computador[r][c]
            jogar_novamente = False
            
            if navio_atingido != 0:
                tabuleiro_fb_computador[r][c] = 'X'
                posicoes_navio = status_computador[navio_atingido]["posicoes"]
                nome_navio = status_computador[navio_atingido]["nome"]
                
                if all(pos in tiros_jogador for pos in posicoes_navio):
                    embarcacoes_computador -= 1
                    print(f"\nParabéns! Você afundou o {nome_navio}! Restam {embarcacoes_computador} embarcações inimigas.")
                    if embarcacoes_computador > 0:
                        print("Você ganhou o direito de atacar novamente!\n")
                        jogar_novamente = True
                else:
                    print(f"\nParabéns! Você acertou uma parte do {nome_navio}! Restam {embarcacoes_computador} embarcações inimigas.\n")
            else:
                tabuleiro_fb_computador[r][c] = 'O'
                print("\nNão houve acerto em nenhuma embarcação inimiga.\n")
                
            if embarcacoes_computador == 0:
                exibir_tabuleiro(tabuleiro_fb_computador, "Tabuleiro do Computador", embarcacoes_computador)
                exibir_tabuleiro(tabuleiro_fb_jogador, "Tabuleiro do Jogador", embarcacoes_jogador)
                exibir_fim_jogo("Parabéns! Você afundou todas as embarcações do inimigo!")
                break
                
            if jogar_novamente:
                input("Pressione Enter para continuar sua jogada...")
                limpar_tela()
                continue
            else:
                turno_do_jogador = False
                input("Pressione Enter para passar a vez ao Computador...")
                limpar_tela()
        else:
            # Turno do Computador
            r_comp, c_comp = computador_escolhe_tiro(linhas, colunas, tabuleiro_fb_jogador)
            tiros_computador.add((r_comp, c_comp))
            print(f"Computador escolheu a linha {r_comp + 1}")
            print(f"Computador escolheu a coluna {c_comp + 1}")
            
            navio_atingido = tabuleiro_pos_jogador[r_comp][c_comp]
            jogar_novamente = False
            
            if navio_atingido != 0:
                tabuleiro_fb_jogador[r_comp][c_comp] = 'X'
                posicoes_navio = status_jogador[navio_atingido]["posicoes"]
                nome_navio = status_jogador[navio_atingido]["nome"]
                
                if all(pos in tiros_computador for pos in posicoes_navio):
                    embarcacoes_jogador -= 1
                    print(f"Computador afundou seu {nome_navio}! Restam {embarcacoes_jogador} embarcações no seu tabuleiro.")
                    if embarcacoes_jogador > 0:
                        print("Computador joga novamente!\n")
                        jogar_novamente = True
                else:
                    print(f"Computador acertou uma parte do {nome_navio}! Restam {embarcacoes_jogador} embarcações no seu tabuleiro.\n")
            else:
                tabuleiro_fb_jogador[r_comp][c_comp] = 'O'
                print("Computador errou! Não houve acerto em nenhuma de suas embarcações.\n")
                
            if embarcacoes_jogador == 0:
                exibir_tabuleiro(tabuleiro_fb_computador, "Tabuleiro do Computador", embarcacoes_computador)
                exibir_tabuleiro(tabuleiro_fb_jogador, "Tabuleiro do Jogador", embarcacoes_jogador)
                exibir_fim_jogo("O computador afundou todas as suas embarcações! Você perdeu.")
                break
                
            if jogar_novamente:
                time.sleep(1.5)
                continue
            else:
                turno_do_jogador = True
                input("Pressione Enter para iniciar seu turno...")
                limpar_tela()

def jogo_simplificado_vs_jogador(linhas, colunas):
    print("\n--- POSICIONAMENTO JOGADOR 1 ---")
    tabuleiro_pos_jogador1 = posicionar_jogador_simplificado(linhas, colunas)
    
    input("\nPressione Enter e passe o controle para o Jogador 2...")
    limpar_tela()
    
    print("\n--- POSICIONAMENTO JOGADOR 2 ---")
    tabuleiro_pos_jogador2 = posicionar_jogador_simplificado(linhas, colunas)
    
    tabuleiro_fb_jogador1 = criar_tabuleiro(linhas, colunas)
    tabuleiro_fb_jogador2 = criar_tabuleiro(linhas, colunas)
    
    embarcacoes_jogador1 = 5
    embarcacoes_jogador2 = 5
    
    limpar_tela()
    print("Bem vindo ao Batalha Naval (Jogador vs Jogador)!")
    
    turno_jogador1 = True
    
    while True:
        if turno_jogador1:
            # Turno do Jogador 1
            exibir_tabuleiro(tabuleiro_fb_jogador2, "Tabuleiro do Jogador 2", embarcacoes_jogador2)
            exibir_tabuleiro(tabuleiro_fb_jogador1, "Seu Tabuleiro (Jogador 1)", embarcacoes_jogador1)
            
            r, c = pedir_coordenada_tiro_nomeado("Jogador 1", linhas, colunas, tabuleiro_fb_jogador2)
            
            if tabuleiro_pos_jogador2[r][c] == 1:
                tabuleiro_fb_jogador2[r][c] = 'X'
                embarcacoes_jogador2 -= 1
                print(f"\nParabéns! Você acertou! Restam {embarcacoes_jogador2} embarcações inimigas.\n")
            else:
                tabuleiro_fb_jogador2[r][c] = 'O'
                print("\nNão houve acerto em nenhuma embarcação inimiga.\n")
                
            if embarcacoes_jogador2 == 0:
                exibir_tabuleiro(tabuleiro_fb_jogador2, "Tabuleiro do Jogador 2", embarcacoes_jogador2)
                exibir_tabuleiro(tabuleiro_fb_jogador1, "Tabuleiro do Jogador 1", embarcacoes_jogador1)
                exibir_fim_jogo("Parabéns Jogador 1! Você afundou todas as embarcações do adversário!")
                break
                
            turno_jogador1 = False
            input("Pressione Enter para passar a vez ao Jogador 2...")
            limpar_tela()
        else:
            # Turno do Jogador 2
            exibir_tabuleiro(tabuleiro_fb_jogador1, "Tabuleiro do Jogador 1", embarcacoes_jogador1)
            exibir_tabuleiro(tabuleiro_fb_jogador2, "Seu Tabuleiro (Jogador 2)", embarcacoes_jogador2)
            
            r, c = pedir_coordenada_tiro_nomeado("Jogador 2", linhas, colunas, tabuleiro_fb_jogador1)
            
            if tabuleiro_pos_jogador1[r][c] == 1:
                tabuleiro_fb_jogador1[r][c] = 'X'
                embarcacoes_jogador1 -= 1
                print(f"\nParabéns! Você acertou! Restam {embarcacoes_jogador1} embarcações inimigas.\n")
            else:
                tabuleiro_fb_jogador1[r][c] = 'O'
                print("\nNão houve acerto em nenhuma embarcação inimiga.\n")
                
            if embarcacoes_jogador1 == 0:
                exibir_tabuleiro(tabuleiro_fb_jogador1, "Tabuleiro do Jogador 1", embarcacoes_jogador1)
                exibir_tabuleiro(tabuleiro_fb_jogador2, "Tabuleiro do Jogador 2", embarcacoes_jogador2)
                exibir_fim_jogo("Parabéns Jogador 2! Você afundou todas as embarcações do adversário!")
                break
                
            turno_jogador1 = True
            input("Pressione Enter para passar a vez ao Jogador 1...")
            limpar_tela()

def jogo_desafio_vs_jogador(linhas, colunas):
    print("\n--- POSICIONAMENTO JOGADOR 1 ---")
    tabuleiro_pos_jogador1, status_jogador1 = posicionar_jogador_desafio(linhas, colunas)
    
    input("\nPressione Enter e passe o controle para o Jogador 2...")
    limpar_tela()
    
    print("\n--- POSICIONAMENTO JOGADOR 2 ---")
    tabuleiro_pos_jogador2, status_jogador2 = posicionar_jogador_desafio(linhas, colunas)
    
    tabuleiro_fb_jogador1 = criar_tabuleiro(linhas, colunas)
    tabuleiro_fb_jogador2 = criar_tabuleiro(linhas, colunas)
    
    embarcacoes_jogador1 = 5
    embarcacoes_jogador2 = 5
    
    tiros_jogador1 = set()
    tiros_jogador2 = set()
    
    limpar_tela()
    print("Bem vindo ao Batalha Naval Desafio (Jogador vs Jogador)!")
    
    turno_jogador1 = True
    
    while True:
        if turno_jogador1:
            # Turno do Jogador 1
            exibir_tabuleiro(tabuleiro_fb_jogador2, "Tabuleiro do Jogador 2", embarcacoes_jogador2)
            exibir_tabuleiro(tabuleiro_fb_jogador1, "Seu Tabuleiro (Jogador 1)", embarcacoes_jogador1)
            
            r, c = pedir_coordenada_tiro_nomeado("Jogador 1", linhas, colunas, tabuleiro_fb_jogador2)
            tiros_jogador1.add((r, c))
            
            navio_atingido = tabuleiro_pos_jogador2[r][c]
            jogar_novamente = False
            
            if navio_atingido != 0:
                tabuleiro_fb_jogador2[r][c] = 'X'
                posicoes_navio = status_jogador2[navio_atingido]["posicoes"]
                nome_navio = status_jogador2[navio_atingido]["nome"]
                
                if all(pos in tiros_jogador1 for pos in posicoes_navio):
                    embarcacoes_jogador2 -= 1
                    print(f"\nParabéns! Você afundou o {nome_navio}! Restam {embarcacoes_jogador2} embarcações inimigas.")
                    if embarcacoes_jogador2 > 0:
                        print("Você ganhou o direito de atacar novamente!\n")
                        jogar_novamente = True
                else:
                    print(f"\nParabéns! Você acertou uma parte do {nome_navio}! Restam {embarcacoes_jogador2} embarcações inimigas.\n")
            else:
                tabuleiro_fb_jogador2[r][c] = 'O'
                print("\nNão houve acerto em nenhuma embarcação inimiga.\n")
                
            if embarcacoes_jogador2 == 0:
                exibir_tabuleiro(tabuleiro_fb_jogador2, "Tabuleiro do Jogador 2", embarcacoes_jogador2)
                exibir_tabuleiro(tabuleiro_fb_jogador1, "Tabuleiro do Jogador 1", embarcacoes_jogador1)
                exibir_fim_jogo("Parabéns Jogador 1! Você afundou todas as embarcações do adversário!")
                break
                
            if jogar_novamente:
                input("Pressione Enter para continuar sua jogada...")
                limpar_tela()
                continue
            else:
                turno_jogador1 = False
                input("Pressione Enter para passar a vez ao Jogador 2...")
                limpar_tela()
        else:
            # Turno do Jogador 2
            exibir_tabuleiro(tabuleiro_fb_jogador1, "Tabuleiro do Jogador 1", embarcacoes_jogador1)
            exibir_tabuleiro(tabuleiro_fb_jogador2, "Seu Tabuleiro (Jogador 2)", embarcacoes_jogador2)
            
            r, c = pedir_coordenada_tiro_nomeado("Jogador 2", linhas, colunas, tabuleiro_fb_jogador1)
            tiros_jogador2.add((r, c))
            
            navio_atingido = tabuleiro_pos_jogador1[r][c]
            jogar_novamente = False
            
            if navio_atingido != 0:
                tabuleiro_fb_jogador1[r][c] = 'X'
                posicoes_navio = status_jogador1[navio_atingido]["posicoes"]
                nome_navio = status_jogador1[navio_atingido]["nome"]
                
                if all(pos in tiros_jogador2 for pos in posicoes_navio):
                    embarcacoes_jogador1 -= 1
                    print(f"\nParabéns! Você afundou o {nome_navio}! Restam {embarcacoes_jogador1} embarcações inimigas.")
                    if embarcacoes_jogador1 > 0:
                        print("Você ganhou o direito de atacar novamente!\n")
                        jogar_novamente = True
                else:
                    print(f"\nParabéns! Você acertou uma parte do {nome_navio}! Restam {embarcacoes_jogador1} embarcações inimigas.\n")
            else:
                tabuleiro_fb_jogador1[r][c] = 'O'
                print("\nNão houve acerto em nenhuma embarcação inimiga.\n")
                
            if embarcacoes_jogador1 == 0:
                exibir_tabuleiro(tabuleiro_fb_jogador1, "Tabuleiro do Jogador 1", embarcacoes_jogador1)
                exibir_tabuleiro(tabuleiro_fb_jogador2, "Tabuleiro do Jogador 2", embarcacoes_jogador2)
                exibir_fim_jogo("Parabéns Jogador 2! Você afundou todas as embarcações do adversário!")
                break
                
            if jogar_novamente:
                input("Pressione Enter para continuar sua jogada...")
                limpar_tela()
                continue
            else:
                turno_jogador1 = True
                input("Pressione Enter para passar a vez ao Jogador 1...")
                limpar_tela()

def menu():
    while True:
        print("\n=== BATALHA NAVAL ===")
        print("1. Jogar Batalha Naval Simplificado (Humano vs Computador)")
        print("2. Jogar Batalha Naval Original - DESAFIO (Humano vs Computador)")
        print("3. Jogar Batalha Naval Simplificado (Jogador vs Jogador)")
        print("4. Jogar Batalha Naval Original - DESAFIO (Jogador vs Jogador)")
        print("5. Sair")
        
        opcao = input("Escolha uma modalidade: ").strip()
        
        if opcao == "1":
            linhas, colunas = escolher_tamanho_tabuleiro()
            limpar_tela()
            jogo_simplificado(linhas, colunas)
        elif opcao == "2":
            linhas, colunas = escolher_tamanho_tabuleiro()
            limpar_tela()
            jogo_desafio(linhas, colunas)
        elif opcao == "3":
            linhas, colunas = escolher_tamanho_tabuleiro()
            limpar_tela()
            jogo_simplificado_vs_jogador(linhas, colunas)
        elif opcao == "4":
            linhas, colunas = escolher_tamanho_tabuleiro()
            limpar_tela()
            jogo_desafio_vs_jogador(linhas, colunas)
        elif opcao == "5":
            print("\nEncerrando o jogo.")
            print("Obrigado por jogar!")
            print("Criado por Guilherme Bettio e Gabriel Kulik.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()