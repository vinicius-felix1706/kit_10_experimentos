# Experimento: Simulador Gantt Interativo — Programação em Tempo Real

## Objetivo do experimento

Usar um diagrama de Gantt simples para relacionar **release**, **execução**, **deadline** e **utilização** de tarefas periódicas, comparando as políticas de escalonamento **Rate Monotonic (RM)** e **Earliest Deadline First (EDF)**.

---

## Descrição

O experimento simula três tarefas periódicas em um sistema de tempo real. O simulador permite configurar os parâmetros de cada tarefa (tempo de computação C, período T e deadline D) e gera:

- Uma tabela com as tarefas e a utilização individual e total da CPU.
- Um diagrama de Gantt com releases, execuções e deadlines ao longo do tempo.
- Uma timeline detalhada tick a tick indicando qual tarefa estava em execução.

As duas políticas foram testadas com o mesmo conjunto de tarefas:

| Tarefa | C | T | D | Utilização |
|--------|---|---|---|-----------|
| T1 | 2 | 4 | 4 | 0.5000 |
| T2 | 2 | 6 | 6 | 0.3333 |
| T3 | 1 | 8 | 8 | 0.1250 |

**Utilização total da CPU: U = 0.9583**

---

## Resultados Obtidos

### Figura 1 – Diagrama de Gantt com política RM (Rate Monotonic)

![Diagrama de Gantt — Política RM](gantt_rm.png)

*Figura 1. Diagrama de Gantt gerado com a política Rate Monotonic. As prioridades são fixas e baseadas no período: T1 (maior prioridade) > T2 > T3. Os pontos pretos indicam os releases de cada tarefa. T3 só executa quando T1 e T2 liberam a CPU. Deadline misses = 0.*

---

### Figura 2 – Diagrama de Gantt com política EDF (Earliest Deadline First)

![Diagrama de Gantt — Política EDF](gantt_edf.png)

*Figura 2. Diagrama de Gantt gerado com a política EDF. As prioridades são dinâmicas: a tarefa com deadline absoluta mais próxima é escolhida a cada instante. Neste conjunto, o padrão de execução coincidiu com o do RM, pois as deadlines são iguais aos períodos. Deadline misses = 0.*

---

## Análise

### Teste de escalonabilidade — Liu & Layland (RM)

O limite de utilização para n = 3 tarefas é:

> **U_bound = 3 × (2^(1/3) − 1) ≈ 0.7798**

Como U = 0.9583 > 0.7798, o conjunto **não passa no teste suficiente do RM**. Porém, esse teste é suficiente mas não necessário. A escalonabilidade real foi verificada pelo **Response Time Analysis (RTA)**:

- **T1:** R = 2 ≤ D₁ = 4 ✅
- **T2:** R = 2 + ⌈2/4⌉×2 = 4 ≤ D₂ = 6 ✅
- **T3:** R = 1 + ⌈1/4⌉×2 + ⌈1/6⌉×2 = 5 ≤ D₃ = 8 ✅

Portanto, **RM é escalonável** para este conjunto mesmo com U acima do limite de Liu & Layland.

### Comparação entre RM e EDF

| Aspecto | RM | EDF |
|---|---|---|
| Tipo de prioridade | Estática (baseada no período) | Dinâmica (baseada na deadline absoluta) |
| Deadline misses | 0 | 0 |
| Escalonável quando U ≤ ? | U_bound ≈ 0.78 (condição suficiente) | U ≤ 1.0 (condição necessária e suficiente) |
| Overhead de implementação | Menor | Maior (recalcula prioridades a cada tick) |
| Comportamento neste experimento | Idêntico ao EDF | Idêntico ao RM |

Neste experimento os dois diagramas produziram a **mesma timeline** porque as deadlines coincidem com os períodos (D = T), o que faz as prioridades EDF e RM convergirem para a mesma ordem de execução.

---

## Respostas das perguntas do experimento

### 1. Como ler um Gantt?

O diagrama possui três elementos visuais principais:

- **Ponto preto (•)**: *release* — momento em que a tarefa foi liberada para execução (início do período).
- **Barra colorida**: intervalo em que a tarefa efetivamente ocupou a CPU.
- **"R" no topo do eixo**: marcação de release no eixo do tempo.
- **Eixo X**: tempo em ticks. **Eixo Y**: cada tarefa em sua própria faixa.

Leitura exemplo: *"T1 foi liberada no tick 0, executou nos ticks 0–1, foi liberada novamente no tick 4, executou nos ticks 4–5…"*

### 2. Onde aparecem releases e deadline misses?

| Evento | Onde aparece no Gantt |
|---|---|
| **Release** | Ponto preto (•) + marcação "R" — indica o início do novo período |
| **Deadline miss** | A barra de execução ultrapassa o próximo release sem ter terminado — visualmente a barra "invade" o período seguinte |
| **Deadline met** | A barra termina antes do próximo release da mesma tarefa |

Neste experimento, **deadline misses = 0** em ambas as políticas — todas as barras terminam antes do próximo release de cada tarefa.

### 3. O que o Gantt mostra que uma tabela não mostra?

A tabela informa **o quê** (C, T, D, U), mas o Gantt mostra **o quando e o porquê**:

- **Preempção**: no tick 2, T1 cede a CPU para T2 — a tabela não revela isso.
- **Ordem de execução real**: T3 só executa quando T1 e T2 liberam espaço; a utilização 0.125 na tabela não deixa claro *quando* ela roda.
- **Diferença entre RM e EDF**: com U = 0.9583 ambos têm 0 misses na tabela, mas o Gantt evidencia que em RM a prioridade de T3 é sempre a mais baixa (estática), enquanto em EDF ela pode ser recalculada dinamicamente.
- **Padrão de repetição (hiperperíodo)**: o Gantt mostra visualmente que o ciclo se repete a cada **lcm(4, 6, 8) = 24 ticks** — informação inexistente na tabela.

---

## Conclusão

O experimento demonstrou como interpretar um diagrama de Gantt de tempo real e relacionar seus elementos visuais com os conceitos de release, execução e deadline. A comparação entre RM e EDF evidenciou que, para este conjunto com U = 0.9583, ambas as políticas são escalonáveis — RM confirmado via RTA e EDF por satisfazer U ≤ 1.0. O Gantt se mostrou essencial para visualizar comportamentos temporais como preempção, ociosidade e o hiperperíodo do sistema, que uma tabela de parâmetros simplesmente não consegue transmitir.
