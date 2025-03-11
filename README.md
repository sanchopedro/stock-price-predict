# Stock Price Predict

Este projeto tem como objetivo prever os preços das ações do IBOVESPA utilizando dados históricos, um modelo de machine learning e uma interface web interativa com Streamlit.

## Funcionalidades

- **Download de Dados:** Utiliza o [yfinance](https://pypi.org/project/yfinance/) para baixar dados históricos até o dia de ontem.

- **Previsão:** Processa os últimos 20 dias de preços para prever o valor do próximo dia, com cálculo de intervalo de incerteza.

- **API Back-end:** Disponibiliza uma API desenvolvida com FastAPI. **Observação:** A API está hospedada no Railway, o que facilita o acesso sem a necessidade de rodá-la localmente.

- **Interface Web (Front-end):** Exibe um gráfico interativo com Plotly para acompanhar o histórico de preços e a previsão. A interface já está hospedada e pode ser acessada [aqui](https://ibov-stock-price-predict.streamlit.app/).

- **Treinamento e Ajuste do Modelo:** Possui scripts para treinamento, fine-tuning e predição do modelo.

- **Gerenciamento de Modelos:** Os modelos treinados são salvos na pasta **models** para facilitar o versionamento e a reutilização.

- **Licença:** Consulte o arquivo [LICENSE](LICENSE) para informações sobre a licença deste projeto.

## Estrutura de Pastas

```
stock-price-predict/
├── api/
│   └── main.py            # API FastAPI responsável pela previsão (back-end hospedado no Railway)
├── data/                  # Arquivos CSV gerados com os dados históricos
├── models/                # Modelos treinados e pesos salvos
├── src/
│   ├── data_loader.py     # Script para download e armazenamento dos dados via yfinance
│   ├── train.py           # Script para treinar o modelo de previsão
│   ├── fine_tune.py       # Script para ajuste (fine-tuning) e otimização do modelo
│   └── predict.py         # Script para realizar predições diretamente sem a API
├── web/
│   └── app.py             # Interface web com Streamlit para exibição dos dados e previsão
├── LICENSE                # Arquivo de licença do projeto
├── requirements.txt       # Dependências do projeto
└── README.md              # Este arquivo
```

## Como Usar (Para Desenvolvimento Local)

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

### 4. API (Back-end)
A API foi desenvolvida com FastAPI e está hospedada no Railway.  

**Para fins de desenvolvimento local**, você pode iniciar a API com:
```
uvicorn api.main:app --reload
```
No entanto, para utilização em produção, utilize o endpoint disponibilizado pelo Railway: [stock-price-predict.up.railway.app](https://stock-price-predict.up.railway.app/)

### 5. Interface Web (Front-end)
A interface web foi criada com Streamlit e já está hospedada.  

Acesse a interface em: [https://ibov-stock-price-predict.streamlit.app/](https://ibov-stock-price-predict.streamlit.app/)

## Observações

- Certifique-se de que, em ambiente de desenvolvimento, a API esteja em execução para que a interface web (caso esteja rodando localmente) consiga obter os dados de previsão.

- O modelo de previsão (implementado em `api/main.py`, `src/train.py` e `src/fine_tune.py`) utiliza os dados dos últimos 20 dias para realizar a predição. Caso o modelo não esteja treinado ou ajustado, execute os scripts correspondentes.

- Os modelos treinados são armazenados na pasta **models** e podem ser reutilizados em futuras predições sem a necessidade de re-treinamento.

- Consulte o arquivo [LICENSE](LICENSE) para mais informações sobre os termos de uso deste projeto.

---

Este projeto foi desenvolvido para demonstrar a integração entre o download de dados históricos, o processamento e ajuste de modelos de previsão, e a visualização interativa com Streamlit e Plotly.