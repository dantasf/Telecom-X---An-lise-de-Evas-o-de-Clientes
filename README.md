# Telecom X — Análise de Evasão de Clientes (Churn)

Projeto completo de ETL + EDA para o desafio **Telecom X - Churn**.

## 🎯 Objetivo
Coletar dados da API (JSON no GitHub), tratar inconsistências, criar a coluna `Contas_Diarias`, realizar Análise Exploratória de Dados (EDA) e gerar um relatório com insights e recomendações para reduzir a evasão.

## 🧱 Estrutura do Repositório
```
telecomx_churn_project/
├── data/
│   ├── raw/                # dados brutos baixados da API
│   └── processed/          # dados tratados e prontos para análise
├── notebooks/
│   └── 01_telecomx_churn_eda.ipynb  # notebook principal com o relatório
├── reports/
│   └── figures/            # gráficos exportados
├── src/
│   ├── etl.py              # funções utilitárias para ETL
│   └── viz.py              # funções utilitárias para gráficos
├── requirements.txt
└── README.md
```

## 🚀 Como executar localmente
1. **Clone o repositório** (após subir para o seu GitHub):
   ```bash
   git clone https://github.com/dantasf/telecomx_churn_project.git
   cd telecomx_churn_project
   ```
2. **Crie e ative um ambiente virtual (opcional, recomendado):**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```
3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Abra o Jupyter e rode o notebook principal:**
   ```bash
   jupyter notebook notebooks/01_telecomx_churn_eda.ipynb
   ```

## 🔗 Fonte da API (JSON)
- Repositório: `ingridcristh/challenge2-data-science`
- Arquivo: `TelecomX_Data.json`
- **Raw URL** utilizada no notebook:  
  `https://raw.githubusercontent.com/ingridcristh/challenge2-data-science/main/TelecomX_Data.json`

> ⚠️ Caso o dicionário de dados esteja disponível no mesmo repositório, você pode informar a URL na variável `DICT_URL` no notebook para enriquecer a documentação das colunas.

## 📊 O que o notebook faz
- **Extração**: Baixa o JSON direto da API (GitHub Raw) e salva em `data/raw/`.
- **Transformação**: Normaliza nomes de colunas, tipa variáveis, trata ausentes/duplicados/categorias, cria `Contas_Diarias`.
- **(Opcional) Padronização**: Converte rótulos tipo "Sim/Não" para binários, traduz colunas.
- **Carga & Análise**: Estatísticas descritivas, gráficos de distribuição da evasão, churn por variáveis categóricas e numéricas.
- **Relatório**: Gera um sumário com principais insights e recomendações baseadas nos achados.

## 🧪 Testado com
- Python 3.10+

## 📝 Licença
Uso educacional.