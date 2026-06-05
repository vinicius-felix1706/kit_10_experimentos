# Experimento: Loop de Controle em Tempo Real com Overrun

## Objetivo do experimento

Entender por que uma malha de controle precisa de período fixo e o que significa overrun.

---

## Descrição

O experimento simula uma malha de controle em tempo real com execução periódica, composta por:

- Geração de um sinal de referência (senoidal)
- Leitura de uma medição com ruído
- Cálculo de controle proporcional (P)
- Atualização da variável de estado do sistema
- Simulação de carga computacional variável

O sistema tenta executar o controle com período fixo de 20 ms (0.02 s), porém pode ocorrer sobrecarga de execução.

Durante a simulação são observados:

- A referência (ref)
- A saída do sistema (x)
- O sinal de controle (u)
- O número de overruns

---

## Resultado Obtido

### Figura 1 – Saída do sistema de controle

![Saída do sistema](controle_output.png)

*Figura 1. Saída do loop de controle em tempo real. Observa-se a evolução da referência senoidal (ref), da saída do sistema (x), do controle aplicado (u) e o acúmulo de overruns ao longo das iterações.*

---

## Análise

O sistema foi executado com os seguintes parâmetros:

- Período de controle: 0.02 s (20 ms)
- Número de iterações: 200
- Carga computacional variável aleatória (até 10 ms)

A saída observada apresenta:

- A referência (ref) variando de forma senoidal
- A saída (x) tentando acompanhar a referência com atraso e suavização
- O controle (u) ajustando o sistema continuamente
- Crescimento constante do contador de overruns

No experimento, foram observados **200 overruns**, indicando que praticamente todos os ciclos violaram o tempo esperado.

---

## Perguntas do experimento

### 1. Por que overrun é perigoso em controle?

Overrun é perigoso porque significa que o sistema não conseguiu executar o ciclo de controle dentro do tempo previsto. Isso pode causar atrasos na atualização do atuador, perda de sincronização com o sistema físico e degradação do desempenho do controle.

Em sistemas críticos, isso pode resultar em comportamento incorreto ou inseguro.

---

### 2. Todo overrun implica instabilidade?

Não. Um overrun não implica necessariamente instabilidade imediata.

Pequenos ou ocasionais overruns podem apenas degradar o desempenho do sistema. No entanto, overruns frequentes ou acumulados podem sim levar à instabilidade, dependendo da sensibilidade da malha de controle.

---

### 3. Qual seria uma estratégia de mitigação?

Algumas estratégias de mitigação incluem:

- Redução da carga computacional por ciclo
- Otimização do algoritmo de controle
- Uso de RTOS para melhor escalonamento de tarefas
- Aumento do período de amostragem (quando possível)
- Priorização de tarefas críticas no sistema

---

## Conclusão

O experimento demonstra a importância da execução periódica em sistemas de controle em tempo real. O overrun representa a violação do período de amostragem, o que pode comprometer a precisão e o desempenho do sistema.

Mesmo em simulações simples, fica evidente que a temporização é um fator crítico para sistemas embarcados e de controle.
