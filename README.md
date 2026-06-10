# Batalha Naval

Implementação do jogo Batalha Naval em Python (terminal), desenvolvida como atividade somativa da disciplina de Raciocínio Algorítmico — PUCPR.

**Equipe:** Guilherme Bettio e Gabriel Kulik

---

## Como executar

```bash
python batalhaNaval.py
```

> Requer Python 3.x. Sem dependências externas.

---

## Requisitos atendidos

| # | Requisito | Nota |
|---|-----------|------|
| 1 | Respeita as regras do jogo (modo Humano vs Computador, tabuleiro oculto, turnos alternados) | 2,0 |
| 2 | Funciona do início ao fim sem quebrar, com tratamento de entradas inválidas | 3,0 |
| 3 | Código modularizado em funções | 1,5 |
| 4 | Tabuleiros implementados com matrizes | 1,0 |
| 5 | Mínimo de 5 embarcações por tabuleiro | 0,5 |
| 6 | Feedback correto ao jogador (acerto, erro, embarcações restantes) | 2,0 |
| 7 | **Desafio:** Modo original com Porta-aviões (5), Navio-tanque (4), Contratorpedeiro (3), Submarino (2) e Destroier (1) — navio só afunda quando todas as posições são atingidas, e o jogador ataca novamente ao afundar | +3,3 |

---

## Funcionalidades

- **Menu principal** com dois modos de jogo e escolha de tamanho (5x10 ou 10x10)
- **Modo Simplificado:** 5 embarcações de 1 posição; jogador posiciona manualmente, computador posiciona aleatoriamente
- **Modo Desafio:** frota clássica com tamanhos variados; posicionamento com direção (H/V); turno extra ao afundar navio
- **Dois tabuleiros por jogador:** um interno (com posições dos navios) e um de feedback (exibido no console, preenchido com `0`, `X` e `O`)
- **Validações:** coordenadas fora do limite, tiro repetido, sobreposição de navios no posicionamento
- **Encerramento:** exibe nome dos integrantes e mensagem de agradecimento
