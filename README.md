# Prova Técnica - Desenvolvedor Python (Integrações)

Candidato: Everton Narciso

---

## 🧩 Exercício 1 - Processamento Assíncrono de Pedidos

Foi implementado um sistema de processamento de pedidos utilizando:

- Fila assíncrona com asyncio.Queue
- Workers concorrentes
- Integração com API externa (Fake Store API)
- Cálculo de total e desconto
- Geração de hash único
- Persistência em SQLite
- Prevenção de duplicidade (INSERT OR IGNORE)
- Logs e tentativas de retry

---

## 🔧 Exercício 2 - Execução Dinâmica de Funções

Foi implementado um sistema dinâmico que permite executar funções com base no nome informado:

Funções disponíveis:
- soma
- subtracao
- maiuscula_para_minuscula

Utiliza `getattr` para permitir escalabilidade sem alteração do código principal.

---

## 🏗️ Exercício 3 - Arquitetura de Integração

Foi proposta uma arquitetura baseada em eventos (event-driven):

- Elimina o uso de polling
- Permite processamento em tempo real
- Utiliza message broker (ex: RabbitMQ)
- Workers escaláveis
- Camada de transformação de dados
- Conectores para diferentes ERPs
- Suporte a multitenant
- Retry automático e Dead Letter Queue

---

## ▶️ Como executar

### Exercício 1
```
python processamento_pedidos.py
````
### Exercício 2
```
python main.py
```

### Exercício 3

```
Arquitetura baseada em eventos (event-driven)

Componentes:

- Fracttal (emissor de eventos)
- Message Broker (RabbitMQ / Kafka)
- Workers assíncronos
- Camada de transformação
- Conectores ERP
- Banco de logs
- Dead Letter Queue (DLQ)

Fluxo:

Fracttal → Fila → Workers → Transformação → ERP

Benefícios:

- Tempo real
- Escalabilidade
- Reutilização de código
- Redução de carga na API


```

## 📦 Requisitos
```
pip install -r requirements.txt
```

