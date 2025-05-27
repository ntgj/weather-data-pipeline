# Weather Data Pipeline

Pipeline de coleta e armazenamento de dados climáticos, utilizando:

- **Python** para coleta via WeatherAPI.
- **PostgreSQL** para armazenamento.
- **Airflow** para orquestração.
- **Docker Compose** para facilitar deploy.

---

## Visão geral

Este projeto coleta dados climáticos a partir da lista definida na variável cidades, armazena em um banco PostgreSQL hospedado na Render (Banco de Dados gratuito e útil para testes, cases e portfólio), e é orquestrado por uma DAG do Apache Airflow.

---

## Tecnologias utilizadas

- Python 3.10
- Requests
- Psycopg2
- Dotenv
- Apache Airflow 2.7
- PostgreSQL
- Docker e Docker Compose

---

## Estrutura do projeto

```plaintext
weather-data-pipeline/
├── dags/
│   └── extract_weather_dag.py
├── scripts/
│   └── coleta_clima.py
├── .env.example
├── docker-compose.yaml
├── requirements.txt
├── README.md
└── logs/ (não versionado)
```
## Como rodar localmente

1. **Clone o repositório:**

```bash
git clone https://github.com/ntgj/weather-data-pipeline.git
cd weather-data-pipeline
```
2. **Configure as variáveis de ambiente:**
Copie .env.example para .env
```bash
cp .env.example .env
```
Preencha com sua WeatherAPI, DATABASE_URL do PostgreSQL e credenciais.

3. **Suba os containers com o Docker Compose:**
```bash
docker compose up -d
```
4. **Acesse o Airflow Web UI:**
http://localhost:8080

**Usuário:** airflow

**Senha:** airflow

(Se configurado assim)

5. **Ative e rode a DAG:**
Acesse o menu "DAGs" no Airflow.
Ative a DAG coleta_clima_dag.
Clique em "Trigger" para executá-la manualmente ou aguarde a execução agendada.
