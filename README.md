# Batalha Naval

Uma implementação clássica de **Batalha Naval** em Python, para jogar no terminal.

## Sobre
Este projeto oferece uma versão simples e divertida do jogo Batalha Naval, com três modos de jogo:
- Jogador vs Jogador
- Computador vs Computador
- Computador vs Jogador

O código é escrito em Python puro e não depende de bibliotecas externas além da biblioteca padrão.

## Como jogar
1. Abra um terminal no diretório do projeto.
2. Execute o jogo com:

```bash
python batalhaNaval.py
```

3. Escolha uma modalidade no menu.
4. Informe as coordenadas de linha e coluna para realizar os tiros.

## Regras do jogo
- O tabuleiro tem tamanho `10x10`.
- Os navios são posicionados automaticamente pelo programa.
- Os símbolos usados no tabuleiro são:
  - `~`: água
  - `N`: navio (visível apenas quando não está escondido)
  - `O`: tiro na água
  - `X`: tiro acertou navio
- O objetivo é acertar todas as posições de navio do oponente.

## Modo de jogo
- **Jogador vs Jogador**: dois jogadores alternam turnos para atacar o tabuleiro do adversário.
- **Computador vs Computador**: duas inteligências artificiais jogam automaticamente até haver um vencedor.
- **Computador vs Jogador**: o jogador ataca o computador e depois o computador ataca o jogador.

## Estrutura do código
- `batalhaNaval.py`: jogo principal e toda a lógica do tabuleiro, disparo, posicionamento de navios e menu.

## Observações
- O jogo foi desenvolvido para rodar em terminais Windows e Unix.
- A tela é limpa automaticamente entre turnos para melhorar a experiência de jogo.

## Autor
Desenvolvido como um projeto de lógica algorítmica em Python.
