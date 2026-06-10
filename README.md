# Batalha Naval

Uma implementação clássica e robusta de **Batalha Naval** em Python para rodar diretamente no terminal. Este projeto foi totalmente atualizado para atender de forma estrita às especificações acadêmicas da disciplina de Raciocínio Algorítmico da PUCPR.

---

## 👥 Desenvolvedores
* **Guilherme Bettio**
* **Gabriel Kulik**

---

## 🎮 Modos de Jogo

O jogo é disputado no formato **Humano vs Computador**, oferecendo duas modalidades distintas que podem ser selecionadas a partir do menu principal:

### 1. Batalha Naval Simplificado
* **Tabuleiros**: Tamanho ajustável de `5x10` (padrão recomendado) ou `10x10`.
* **Embarcações**: Cada jogador possui exatamente 5 embarcações de tamanho 1 (ocupando um único espaço da matriz).
* **Posicionamento**:
  * **Jogador**: Informa manualmente a linha e coluna (coordenadas baseadas em 1) para posicionar cada uma de suas 5 embarcações.
  * **Computador**: Posiciona suas 5 embarcações de maneira totalmente aleatória.
* **Turnos**: Alternados de forma simples.

### 2. Batalha Naval Original (Modo Desafio)
* **Tabuleiros**: Tamanho ajustável de `5x10` ou `10x10`.
* **Embarcações**: Frota tradicional com 5 embarcações de múltiplos tamanhos:
  * **Porta-aviões**: ocupa 5 posições.
  * **Navio-tanque**: ocupa 4 posições.
  * **Contratorpedeiro**: ocupa 3 posições.
  * **Submarino**: ocupa 2 posições.
  * **Destroier**: ocupa 1 posição.
* **Posicionamento**:
  * **Jogador**: Posiciona manualmente cada navio informando a coordenada inicial (linha e coluna) e a direção desejada (`H` para Horizontal ou `V` para Vertical).
  * **Computador**: Posiciona a frota inteira de forma aleatória nas direções horizontal ou vertical.
  * *Validações de limites e sobreposição de navios impedem posicionamentos ilegais.*
* **Mecânica de Dano**: Um navio de tamanho maior só é considerado **afundado** quando todas as suas coordenadas forem atingidas.
* **Regra de Turno Extra**: Ao conseguir afundar totalmente uma das embarcações inimigas, o jogador (ou computador) ganha o direito de realizar um **ataque extra** no mesmo turno.

---

## 🖥️ Interface Visual do Tabuleiro

Conforme especificado nas orientações de design, os tabuleiros não revelam os barcos ocultos. Eles exibem apenas o feedback visual de ataques no console em formato de listas de Python, facilitando a leitura de coordenadas:
* `0`: Célula desconhecida (água sem ataques).
* `'O'`: Tiro realizado que atingiu a água (erro).
* `'X'`: Tiro realizado que atingiu um navio (acerto).

**Exemplo de Exibição:**
```text
Tabuleiro do Computador
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
['X', 0, 0, 'O', 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
------------------------------
Embarcações restantes: 4
```

---

## 🚀 Como Executar

### Pré-requisitos
* Ter o **Python 3.x** instalado.
* Não há dependências de bibliotecas de terceiros (usa bibliotecas padrão do Python: `random`, `os`, `time`).

### Passo a Passo
1. Abra seu terminal ou prompt de comando na pasta do projeto.
2. Execute o jogo usando:
   ```bash
   python batalhaNaval.py
   ```
3. Utilize as opções numéricas apresentadas no menu para navegar e jogar.

---

## 🛠️ Validações Integradas no Código
* **Tratamento de Exceções**: O jogo não quebra se você digitar letras ou símbolos inválidos nas coordenadas ou no menu; ele exibe uma mensagem instrutiva e solicita o dado novamente.
* **Tiros Repetidos**: O jogo detecta se o jogador já tentou atirar em uma célula anteriormente e solicita uma nova coordenada.
* **Limites do Mapa**: Navios posicionados manualmente ou tiros disparados fora dos limites do tabuleiro (como linha 6 em um tabuleiro 5x10) são interceptados e impedidos pelas regras de validação.
