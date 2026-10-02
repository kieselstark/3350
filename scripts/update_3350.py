"""Lädt die täglichen Metaplanet-Schlusskurse (3350.T) (Yahoo Finance via yfinance) nach data/3350.json.

Format: {"updated": "YYYY-MM-DD", "rows": [["YYYY-MM-DD", close], ...]}
Kurse sind splitbereinigt.
Bricht ab, ohne etwas zu ändern, wenn die Quelle leer oder deutlich kürzer als der Bestand ist.
"""
import datetime as dt
import json
import pathlib
import sys

import pandas as pd
import yfinance as yf

START = '2018-01-01'
OUT = pathlib.Path(__file__).resolve().parents[1] / 'data' / '3350.json'

df = yf.download('3350.T', start=START, interval='1d', progress=False, auto_adjust=False)
close = df['Close']
if isinstance(close, pd.DataFrame):
    close = close.iloc[:, 0]
close = close.dropna()
if close.empty:
    sys.exit('Keine Daten erhalten – data/3350.json bleibt unverändert')

rows = [[ts.strftime('%Y-%m-%d'), round(float(v), 2)] for ts, v in close.items()]

if OUT.exists():
    old = json.loads(OUT.read_text(encoding='utf-8'))['rows']
    if len(rows) < len(old) * 0.95:
        sys.exit(f'Nur {len(rows)} statt {len(old)} Kurse erhalten – Abbruch')

OUT.parent.mkdir(exist_ok=True)
OUT.write_text(json.dumps({'updated': rows[-1][0], 'rows': rows}, separators=(',', ':')), encoding='utf-8')
print(f'{len(rows)} Kurse bis {rows[-1][0]}')
