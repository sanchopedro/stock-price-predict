# Stock Price Predict

Este projeto tem como objetivo prever os preços das ações do IBOVESPA utilizando dados históricos, um modelo de machine learning e uma interface web interativa com Streamlit.

## Funcionalidades

- **Download de Dados:** Utiliza o [yfinance](https://pypi.org/project/yfinance/) para baixar dados históricos até o dia de ontem.
- **Previsão:** Processa os últimos 20 dias de preços para prever o valor do próximo dia, com cálculo de intervalo de incerteza.
- **API:** Disponibiliza uma API (FastAPI) que retorna os dados de previsão.
- **Interface Web:** Exibe um gráfico interativo com Plotly para acompanhar o histórico de preços e a previsão.
- **Treinamento e Ajuste do Modelo:** Possui scripts para treinamento, fine-tuning e predição do modelo.
- **Gerenciamento de Modelos:** Os modelos treinados são salvos na pasta **models** para facilitar o versionamento e a reutilização.

## Estrutura de Pastas

```
stock-price-predict/
├── api/
│   └── main.py            # API FastAPI responsável pela previsão
├── data/                  # Arquivos CSV gerados com os dados históricos
├── models/                # Modelos treinados e pesos salvos
├── src/
│   ├── data_loader.py     # Script para download e armazenamento dos dados via yfinance
│   ├── train.py           # Script para treinar o modelo de previsão
│   ├── fine_tune.py       # Script para ajuste (fine-tuning) e otimização do modelo
│   └── predict.py         # Script para realizar predições diretamente sem a API
├── web/
│   └── app.py             # Interface web com Streamlit para exibição dos dados e previsão
├── requirements.txt       # Dependências do projeto
└── README.md              # Este arquivo
```

## Como Usar

### 1. Instalação
- Clone o repositório:
  ```
  git clone https://sanchopedro.com/stock-price-predict.git
  ```
- Navegue até a pasta do projeto:
  ```
  cd stock-price-predict
  ```
- Instale as dependências (recomendado criar um ambiente virtual):
  ```
  python3 -m venv venv
  source venv/bin/activate  # No macOS/Linux
  venv\Scripts\activate     # No Windows
  pip install -r requirements.txt
  ```

### 2. Baixar Dados Históricos
Utilize o script para baixar os dados históricos (os dados serão salvos na pasta `data/`):
```
python src/data_loader.py
```

### 3. Treinamento e Ajuste do Modelo
- Para treinar o modelo, execute:
  ```
  python src/train.py
  ```
- Para realizar fine-tuning e otimizar o desempenho do modelo, execute:
  ```
  python src/fine_tune.py
  ```
- Você também pode testar predições diretamente via script (sem utilizar a API):
  ```
  python src/predict.py
  ```

### 4. Iniciar a API
A API utiliza FastAPI. Para iniciar o servidor, execute:
```
uvicorn api.main:app --reload
```
A API ficará disponível em [http://127.0.0.1:8000](http://127.0.0.1:8000).

### 5. Rodar a Interface Web
Na pasta do projeto, execute o seguinte comando para iniciar o Streamlit:
```
streamlit run web/app.py
```
A interface web será aberta no navegador, exibindo o gráfico interativo e as informações de previsão.

## Observações

- Certifique-se de que a API esteja em execução para que a interface web consiga obter os dados de previsão.
- O modelo de previsão (implementado em `api/main.py`, `src/train.py` e `src/fine_tune.py`) espera uma entrada de 20 dias para realizar a predição. Caso o modelo não esteja treinado ou ajustado, apenas execute os scripts de treinamento e fine-tuning.
- Os modelos treinados são armazenados na pasta **models** e podem ser reutilizados para futuras predições sem a necessidade de re-treinamento.

---

Este projeto foi desenvolvido para demonstrar a integração entre download de dados históricos, treinamento e ajuste de modelos de previsão, e visualização interativa com Streamlit e Plotly.