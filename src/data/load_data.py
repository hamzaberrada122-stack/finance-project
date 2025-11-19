import yfinance as yf
import pandas as pd
import os

def download_stocks(tickers, start_date="2020-01-01", folder="data/raw"):
    """
    Télécharge les données historiques pour les tickers donnés
    et les sauvegarde dans data/raw/.
    """
    os.makedirs(folder, exist_ok=True)

    for t in tickers:
        print(f"Downloading {t} ...")
        df = yf.download(t, start=start_date)
        file_path = f"{folder}/{t}.csv"
        df.to_csv(file_path)
        print(f"Saved: {file_path}")

if __name__ == "__main__":
    tickers = ["MSFT", "NVDA", "AMD", "GOOG"]
    download_stocks(tickers)
