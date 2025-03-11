from tensorflow.keras.models import load_model  # type: ignore
from tensorflow.keras.losses import MeanSquaredError  # type: ignore
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import sys
import os

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# Importando a função create_sequences do arquivo src/train.py
from src.train import create_sequences

ticker_ibov = [
    "PETR4",
    "VALE3",
    "ITUB4",
    "BBDC4",
    "ABEV3",
    "B3SA3",
    "MGLU3",
    "WEGE3",
    "TAEE11",
    "USIM5",
]

# Carregar modelo base
base_model = load_model(
    "models/base_model.keras", custom_objects={"mse": MeanSquaredError()}
)

for ticker in ticker_ibov:
    print(f"Ajustando modelo para {ticker}...")

    # Carregar os dados do ticker
    df = pd.read_csv(f"data/{ticker}.csv")

    # Renomear a coluna de preço ajustado
    df.rename(columns={df.columns[1]: ticker}, inplace=True)

    # Acessar a coluna renomeada com o nome correto
    df_close = df[ticker].values.reshape(-1, 1)  # type: ignore

    # Escalar os dados
    scaler = MinMaxScaler()
    df_close_scaled = scaler.fit_transform(df_close)

    # Criar sequências para o modelo
    X, y = create_sequences(df_close_scaled)

    # Treinar o modelo ajustado
    base_model.fit(X, y, epochs=10, batch_size=16)

    # Salvar o modelo ajustado
    base_model.save(f"models/{ticker}.keras")
