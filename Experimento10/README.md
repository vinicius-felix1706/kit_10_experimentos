# Experimento: Comunicação entre Tarefas com Fila

## Objetivo do experimento

Entender como um buffer finito e diferentes velocidades de produção e consumo afetam a latência e o backlog em sistemas de tempo real.

---

## Descrição

O experimento utiliza uma fila (*queue*) para representar a comunicação entre duas tarefas concorrentes:

- **Produtor:** gera dados periodicamente e os insere na fila.
- **Consumidor:** remove os dados da fila e realiza o processamento.

A fila possui tamanho limitado (*buffer finito*), simulando uma situação comum em sistemas embarcados e sistemas operacionais de tempo real (RTOS).

Para analisar o impacto da velocidade de consumo, o consumidor foi alterado para utilizar:

```python
time.sleep(random.uniform(0.08, 0.15))
