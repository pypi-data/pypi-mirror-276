import os

import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn import metrics

from config import TrainConfig, init_train_config
from data.data_manager import read_csv, prepare_for_training, save_csv
from logger import (
    get_basic_logger,
    get_file_handler,
    get_console_handler,
)

LOGGER = get_basic_logger(logger_name=__name__)
LOGGER.addHandler(get_file_handler(os.path.basename(__file__).split(".")[0]))
LOGGER.addHandler(get_console_handler())


def _cv_electrode_generator(df: pd.DataFrame):
    df["index"] = [i.split(" ")[-1].split("|")[0] for i in df.index.values.tolist()]
    for id in df["index"].unique():
        LOGGER.info(f"Cross-validation for electrode {id}")
        df_train, df_eval = (
            df[df["index"] != id],
            df[df["index"] == id],
        )
        yield id, df_train.drop(columns=["index"]), df_eval.drop(columns=["index"])


def main(config: TrainConfig):
    df = read_csv(config.data_path)

    model = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("svm", SVR(kernel="rbf")),
        ]
    )
    score_df = pd.DataFrame()
    for id, df_train, df_eval in _cv_electrode_generator(df):
        x_train, y_train = prepare_for_training(df_train, config.target)
        x_eval, y_eval = prepare_for_training(df_eval, config.target)

        model.fit(x_train, y_train)

        y_pred = model.predict(x_eval)

        rmse = metrics.root_mean_squared_error(y_eval, y_pred)
        LOGGER.info(f"Evaluation RMSE: {rmse}")

        score_df = pd.concat(
            [score_df, pd.DataFrame({"id": [id], "rmse": [rmse]})], axis=0
        )
        save_csv(score_df, config.score_path)


if __name__ == "__main__":
    _config = init_train_config()
    main(_config)
