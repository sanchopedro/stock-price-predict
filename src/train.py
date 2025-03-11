# %%
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential  # type: ignore
from tensorflow.keras.layers import LSTM, Dense  # type: ignore
from sklearn.preprocessing import MinMaxScaler

# %% Carregar dados de PETR4 como base

df = pd.read_csv("data/PETR4.csv")
df.rename(columns={df.columns[1]: df.columns[1].replace(".SA", "")}, inplace=True)
df.head()

# %% Reshape dos dados
df_close = df["PETR4"].values.reshape(-1, 1)  # type: ignore

# %% Scaler
scaler = MinMaxScaler()
df_close_scaled = scaler.fit_transform(df_close)


# %% Criar dados de entrada
def create_sequences(data, seq_length=10):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i : i + seq_length])
        y.append(data[i + seq_length])
    return np.array(X), np.array(y)


# %%
X, y = create_sequences(df_close_scaled)
# %% Criar modelo base
model = Sequential(
    [LSTM(50, return_sequences=True, input_shape=(X.shape[1], 1)), LSTM(50), Dense(1)]
)

model.compile(optimizer="adam", loss="mse")
model.fit(X, y, epochs=50, batch_size=32)

# Salvar modelo base
model.save("models/base_model.keras")
