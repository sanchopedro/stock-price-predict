from fastapi import FastAPI
import numpy as np
from tensorflow.keras.models import load_model  # type: ignore
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import sys
import os

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

app = FastAPI()


@app.get("/")
def read_root():
    return "Bem-vindo à API de previsão de ações!"


@app.get("/predict/{ticker}")
def predict_stock(ticker: str):
    try:
        model = load_model(f"models/{ticker}.keras")
    except Exception as e:
        return {"error": f"Modelo não encontrado. Erro: {str(e)}"}

    try:
        # Carregar os dados locais a partir do CSV
        df = pd.read_csv(f"data/{ticker}.csv")
        df.rename(columns={df.columns[1]: "Close"}, inplace=True)
    except Exception as e:
        return {
            "error": f"Erro ao carregar os dados do CSV para {ticker}. Erro: {str(e)}"
        }

    try:
        # Selecionar apenas os preços de fechamento
        df_close = df["Close"].values.reshape(-1, 1)  # type: ignore
        dates = df["Date"].values  # Pegamos as datas para exibição no gráfico
    except KeyError as e:
        return {
            "error": f"Coluna 'Close' ou 'Date' não encontrada no CSV. Erro: {str(e)}"
        }

    # Normalizar os preços de fechamento
    try:
        scaler = MinMaxScaler()
        close_price_scaled = scaler.fit_transform(df_close)

        # Pegar os últimos 20 dias para exibição no gráfico
        last_20_days = close_price_scaled[-20:].reshape(1, 20, 1)

        # Fazer a previsão para o próximo dia
        prediction_scaled = model.predict(last_20_days)
        prediction = scaler.inverse_transform(prediction_scaled)[0][0]

        # Calcular o desvio padrão dos últimos 20 preços reais
        std_dev = np.std(df_close[-20:])
        lower_bound = round(float(prediction - std_dev), 2)
        upper_bound = round(float(prediction + std_dev), 2)

    except Exception as e:
        return {"error": f"Erro ao processar a previsão para {ticker}. Erro: {str(e)}"}

    return {
        "ticker": ticker,
        "real_prices": [round(float(price), 2) for price in df_close[-20:].flatten()],
        "dates": dates[-20:].tolist(),
        "predicted_price": round(float(prediction), 2),
        "prediction_range": {"lower": lower_bound, "upper": upper_bound},
    }
