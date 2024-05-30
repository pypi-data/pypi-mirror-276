from pathlib import Path
from typing import Any, Tuple

import joblib
import numpy as np
import pandas as pd


def read_csv(path: Path | str) -> pd.DataFrame:
    return pd.read_csv(path, index_col=0)


def save_csv(df: pd.DataFrame, path: Path | str) -> None:
    path = Path(path) if isinstance(path, str) else path
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path)


def cv_electrode_generator(df: pd.DataFrame):
    for electrode in df["electrode"].unique():
        df_train, df_eval = (
            df[df["electrode"] != electrode],
            df[df["electrode"] == electrode],
        )
        yield df_train, df_eval


def save_model(model: Any, path: Path):
    path.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)


def prepare_for_training(
    df: pd.DataFrame, target: str
) -> Tuple[np.ndarray, np.ndarray]:
    return df.drop(columns=[target]).values, df[target].values
