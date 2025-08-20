from __future__ import annotations
import os
import pandas as pd
import matplotlib.pyplot as plt

FIG_DIR = "reports/figures"

def ensure_fig_dir():
    os.makedirs(FIG_DIR, exist_ok=True)

def plot_churn_distribution(df: pd.DataFrame, churn_col: str = "churn"):
    ensure_fig_dir()
    counts = df[churn_col].value_counts(dropna=False)
    ax = counts.plot(kind="bar")
    ax.set_title("Distribuição de Evasão (Churn)")
    ax.set_xlabel("Churn")
    ax.set_ylabel("Quantidade")
    plt.tight_layout()
    path = os.path.join(FIG_DIR, "churn_distribution.png")
    plt.savefig(path, dpi=150)
    plt.close()
    return path

def plot_churn_by_categoricals(df: pd.DataFrame, churn_col: str = "churn", max_unique: int = 20):
    ensure_fig_dir()
    paths = []
    cat_cols = [c for c in df.columns if df[c].dtype == "object" or df[c].dtype.name == "category"]
    for c in cat_cols:
        if c == churn_col: 
            continue
        if df[c].nunique(dropna=False) > max_unique:
            continue
        ct = pd.crosstab(df[c], df[churn_col], normalize="index")
        ax = ct.plot(kind="bar", stacked=True)
        ax.set_title(f"Churn por {c}")
        ax.set_xlabel(c)
        ax.set_ylabel("Proporção")
        plt.tight_layout()
        path = os.path.join(FIG_DIR, f"churn_by_{c}.png")
        plt.savefig(path, dpi=150)
        plt.close()
        paths.append(path)
    return paths

def plot_numeric_by_churn(df: pd.DataFrame, churn_col: str = "churn"):
    ensure_fig_dir()
    paths = []
    num_cols = [c for c in df.columns if df[c].dtype.kind in "biufc"]
    for c in num_cols:
        if c == churn_col:
            continue
        # Boxplot por churn
        ax = df.boxplot(column=c, by=churn_col)
        plt.title(f"{c} por {churn_col}")
        plt.suptitle("")
        plt.xlabel("Churn")
        plt.ylabel(c)
        plt.tight_layout()
        path = os.path.join(FIG_DIR, f"{c}_by_{churn_col}.png")
        plt.savefig(path, dpi=150)
        plt.close()
        paths.append(path)
    return paths