# Experimento 3 — Sobrecarga de CPU e Impacto Temporal

## Objetivo

Demonstrar que uma carga computacional excessiva pode aumentar o atraso de execução, introduzir variações temporais (jitter) e causar perdas de prazo (deadline misses).

---

## Parte 1 — CPU Overload

### Figura 1 – Execução do script de sobrecarga

![CPU Overload](overload_saida04.png)

O script executa uma operação computacional intensiva (10 milhões de iterações) a cada ciclo. Embora o período configurado seja de 20 ms, os tempos observados ficaram entre aproximadamente 1,5 s e 1,9 s por execução.

### Análise

Os resultados demonstram uma condição de sobrecarga da CPU. O tempo necessário para concluir cada ciclo é muito superior ao período desejado, impossibilitando o cumprimento dos requisitos temporais da tarefa.

---

## Parte 2 — Simulador de Jitter

### Figura 2 – Simulação com carga média de CPU de 20%

![Simulador](lab04.png)

Nesta configuração foi utilizada uma carga média de CPU de 20%. O simulador registrou 0 deadline misses.

### Análise

Com baixa utilização da CPU, o sistema possui capacidade suficiente para executar as tarefas dentro dos limites temporais definidos. Não foram observadas perdas de prazo, indicando um comportamento temporal estável.

---

## Conclusão

O experimento mostrou que a carga computacional influencia diretamente o comportamento temporal de um sistema. O script de sobrecarga apresentou tempos de execução muito superiores ao período desejado, caracterizando uma situação de processamento excessivo. Já no simulador, com apenas 20% de utilização média da CPU, não foram observadas perdas de prazo, evidenciando que cargas mais baixas favorecem a previsibilidade e o cumprimento dos requisitos temporais.
