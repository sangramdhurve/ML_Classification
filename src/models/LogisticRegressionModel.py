import logging
import numpy as np
import pandas as pd

from typing import List
from config.common_config import options
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression

try:
    from ScoringModel import ScoringModel
except ModuleNotFoundError:
    from .ScoringModel import ScoringModel


class LogisticRegressionModel(ScoringModel):
    def __init__(self, logger: logging = None, verbose=False):
        self.__verbose = verbose
        self.__logger = logger
        self.__min_max_scaler_params = {'clip': False, 'copy': True, 'feature_range': (0, 1)}
        self.__min_max_scaler_attributes = {'scaler_min_': [0., 0., 0.],
                                            'scaler_scale_': [0.0070922, 0.01818182, 0.00044014],
                                            'n_samples_seen_': 4417,
                                            'data_max_': [141., 55., 2272.],
                                            'data_min_': [0., 0., 0.],
                                            '_data_range_': [141., 55., 2272.],
                                            'feature_names_in_': options["numerical_cols"],
                                            'n_features_in_': 3,
                                            'scale_': [0.0070922, 0.01818182, 0.00044014],
                                            'min_': [0., 0., 0.]}

        self.__model_params = {'C': 1.0,
                               'class_weight': None,
                               'dual': False,
                               'fit_intercept': True,
                               'intercept_scaling': 1,
                               'l1_ratio': None,
                               'max_iter': 100,
                               'multi_class': 'auto',
                               'n_jobs': None,
                               'penalty': 'l2',
                               'random_state': None,
                               'solver': 'lbfgs',
                               'tol': 0.0001,
                               'verbose': 0,
                               'warm_start': False}

        self.__model_attributes = {'classes_': np.array([0., 1.]),
                                   'coef_': np.array([[-1.98655013, 3.0616236, -5.98924944, -0.52942288, 0.52859832,
                                                       0.56618498, 0.44400794, -0.42360187, 0.41134003, -0.49263594,
                                                       -0.63640495, -0.42874172, 0.44369051, -0.77200963]]),
                                   'intercept_': np.array([-0.21073904]),
                                   'n_features_in_': 14,
                                   'n_iter_': [30]}
        self.__min_max_scaler = MinMaxScaler()
        self.__init_scaler()
        self.__model = self.__load_model()

    def __load_model(self):
        model = LogisticRegression()
        model.set_params(**self.__model_params)

        for attr_name, attr_value in self.__model_attributes.items():
            setattr(model, attr_name, attr_value)

        return model

    def __init_scaler(self):
        self.__min_max_scaler.set_params(**self.__min_max_scaler_params)
        for attribute_name, attribute_value in self.__min_max_scaler_attributes.items():
            setattr(self.__min_max_scaler, attribute_name, attribute_value)
            if self.__logger:
                self.__logger.info(f"set attribute {attribute_name} to {attribute_value} for min max scaler")

    def __preprocess_data(self, data: dict) -> pd.DataFrame:
        cols = options["all_cols_reqd_by_model"]
        df_data = [[0] * len(cols)]  # set all column value to zero
        df = pd.DataFrame(data=df_data, columns=cols)

        total_visits = data.get("total_visits", 0)
        total_time_spent_on_website = data.get("total_time_spent_on_website", 0)
        page_views_per_vist = data.get("page_views_per_visit", 0)
        scaled_values = self.__min_max_scaler.transform([[total_visits, total_time_spent_on_website,
                                                          page_views_per_vist]])

        df.loc[0:0, ["total_visits", "total_time_spent_on_website", "page_views_per_visit"]] = scaled_values[0]

        final_categorical_cols = options["categorical_cols"]
        for col_name, col_values in final_categorical_cols.items():
            col_value_in_data = data[col_name]

            if col_value_in_data in col_values:
                if self.__logger:
                    self.__logger.info(f"{col_value_in_data} is present for column {col_name}")
                col_name_in_df = "_".join([col_name, col_value_in_data])
                # if a column's value is present in the data then set that corresponding column's value to 1 in df
                df.at[0, col_name_in_df] = 1

        if self.__verbose:
            print("df: ")
            print(df.loc[0])
            print()
        return df

    def predict(self, data: dict, **kwargs) -> int:
        pred_df = self.__preprocess_data(data)
        values_to_predict = pred_df.loc[0].values.flatten().tolist()
        score = self.__model.predict([values_to_predict])
        return score[0]

    def predict_score(self, data: dict, **kwargs) -> List[float]:
        pred_df = self.__preprocess_data(data)
        values_to_predict = pred_df.loc[0].values.flatten().tolist()
        scores = self.__model.predict_proba([values_to_predict])
        return list(scores[0])


if __name__ == '__main__':
    test_predict_data = {
        "total_visits": 15,
        "total_time_spent_on_website": 753,
        "page_views_per_visit": 15,
        "lead_source": None,
        "last_activity": None,
        "specialization": None,
        "search": None,
        "newspaper": "Yes",
        "last_notable_activity": None
    }

    scorer = LogisticRegressionModel(verbose=False)
    print(scorer.predict(test_predict_data))
    print()
    print(scorer.predict_score(test_predict_data))
