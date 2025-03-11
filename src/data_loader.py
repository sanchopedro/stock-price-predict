import yfinance as yf
import pandas as pd
import os
from datetime import datetime

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


def get_stock_data(ticker: str, start: str) -> pd.DataFrame:
    try:
        ticker_yf = ticker + ".SA"
        # Download dos dados (removendo o parâmetro 'end' para pegar os dados mais recentes)
        df = yf.download(ticker_yf, start=start, auto_adjust=False)

        if df.empty:  # type: ignore
            print(f"Erro: Nenhum dado encontrado para {ticker}")
            return pd.DataFrame()

        # Extrair apenas a coluna de preço ajustado
        prices = df["Adj Close"].copy()  # type: ignore

        # Criar um DataFrame com apenas os preços
        clean_df = pd.DataFrame(prices)

        # Garantir que a pasta 'data' exista
        os.makedirs("data", exist_ok=True)

        # Caminho do arquivo
        file_path = f"data/{ticker}.csv"

        # Salvar apenas os dados necessários
        clean_df.to_csv(file_path)

        print(f"Arquivo {file_path} salvo com sucesso!")
        return clean_df

    except Exception as e:
        print(f"Erro ao baixar dados de {ticker}: {e}")
        return pd.DataFrame()


if __name__ == "__main__":
    start_date = "2015-01-01"  # Data fixa de início

    for ticker in ticker_ibov:
        print(f"Downloading {ticker} data...")
        get_stock_data(ticker, start=start_date)
