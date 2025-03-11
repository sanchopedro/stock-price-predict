import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model  # type: ignore
from sklearn.preprocessing import MinMaxScaler
import yfinance as yf


def predict_stock(ticker):
    try:
        model = load_model(f"models/{ticker}.keras")
    except:
        return {"error": "Modelo não encontrado"}

    # Carregar os dados do ticker
    df = pd.read_csv(f"data/{ticker}.csv")

    # Renomear a coluna de preço ajustado
    df.rename(columns={df.columns[1]: ticker}, inplace=True)

    # Acessar a coluna renomeada com o nome correto
    df_close = df[ticker].values.reshape(-1, 1)  # type: ignore

    scaler = MinMaxScaler()
    df_close_scaled = scaler.fit_transform(df_close)

    prediction = model.predict(df_close_scaled[-10:].reshape(1, 10, 1))
    return scaler.inverse_transform(prediction).tolist()


if __name__ == "__main__":
    ticker = input("Digite o ticker da ação (ex: PETR4): ")
    print(f"Previsão para {ticker}: {predict_stock(ticker)}")
