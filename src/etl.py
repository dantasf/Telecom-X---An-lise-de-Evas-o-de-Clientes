from __future__ import annotations
import os
import re
import json
from typing import Optional, List, Tuple, Dict
import pandas as pd
import numpy as np
import requests

RAW_DIR = "data/raw"
PROC_DIR = "data/processed"

def ensure_dirs():
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(PROC_DIR, exist_ok=True)

def fetch_json_to_df(url: str, save_as: str = "telecomx_raw.json") -> pd.DataFrame:
    ensure_dirs()
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    data = r.json()
    with open(os.path.join(RAW_DIR, save_as), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    # Normaliza em DF
    if isinstance(data, dict) and "data" in data:
        df = pd.json_normalize(data["data"])
    else:
        df = pd.json_normalize(data)
    return df

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    def clean(col):
        col = col.strip()
        col = re.sub(r"\s+", "_", col)
        col = col.replace("%","pct").replace("$","dolar")
        return col.lower()
    df = df.rename(columns={c: clean(c) for c in df.columns})
    return df

def coerce_numeric(df: pd.DataFrame, candidates: Optional[List[str]] = None) -> pd.DataFrame:
    work = df.copy()
    if candidates is None:
        candidates = [c for c in work.columns if work[c].dtype == "object"]
    for c in candidates:
        # tenta converter strings numéricas (com vírgula/ponto)
        try:
            work[c] = (
                work[c]
                .astype(str)
                .str.replace(r"[R$\s]", "", regex=True)
                .str.replace(".", "", regex=False)
                .str.replace(",", ".", regex=False)
            )
            work[c] = pd.to_numeric(work[c], errors="ignore")
        except Exception:
            pass
    return work

def summarize_missing(df: pd.DataFrame) -> pd.DataFrame:
    miss = df.isna().sum().to_frame("missing")
    miss["pct_missing"] = (miss["missing"] / len(df)).round(4)
    miss = miss.sort_values("pct_missing", ascending=False)
    return miss

def treat_basic(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, dict]]:
    report = {}
    work = df.copy()
    # Duplicatas
    dup_count = work.duplicated().sum()
    work = work.drop_duplicates()
    report["duplicates_removed"] = int(dup_count)

    # Tipagem
    work = coerce_numeric(work)

    # Valores ausentes
    miss = summarize_missing(work)
    report["missing"] = miss.to_dict(orient="index")

    # Preenchimento simples (numérico -> mediana; categórico -> "Desconhecido")
    for c in work.columns:
        if work[c].dtype.kind in "biufc":
            if work[c].isna().any():
                work[c] = work[c].fillna(work[c].median())
        else:
            if work[c].isna().any():
                work[c] = work[c].fillna("Desconhecido")

    # Normalização de rótulos Sim/Não
    yes_no_map = {"Sim":1, "Não":0, "Yes":1, "No":0, "Y":1, "N":0, "S":1, "NÃO":0, "NAO":0}
    for c in work.columns:
        if work[c].dtype == "object":
            uniques = set(map(str, work[c].dropna().unique()))
            if uniques & set(yes_no_map.keys()):
                work[c] = work[c].map(yes_no_map).fillna(work[c])

    return work, report

def create_contas_diarias(df: pd.DataFrame, monthly_col: str = "monthlycharges") -> pd.DataFrame:
    work = df.copy()
    if monthly_col in work.columns:
        work["contas_diarias"] = work[monthly_col] / 30.0
    return work

def save_processed(df: pd.DataFrame, name: str = "telecomx_processed.parquet"):
    ensure_dirs()
    path = os.path.join(PROC_DIR, name)
    df.to_parquet(path, index=False)
    return path