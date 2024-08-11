import logging
from typing import Tuple

import numpy as np
import pandas as pd

from src.logger import logger_dpf


class XiCorr:
    """
    A class to compute the XiCorr correlation between a target column and a list of features.

    **Attributes**:
        data (pd.DataFrame): The data containing the target column.
        target_col (str): The target column to compute the correlation against.
        date_col (str): The column containing the date.
        external_data (pd.DataFrame): The data containing the features.
    """

    def __init__(
        self,
        data: pd.DataFrame,
        target_col: str,
        date_col: str,
        external_data: pd.DataFrame,
    ):
        self.data = data
        self.target_col = target_col
        self.date_col = date_col
        self.external_data = external_data
        self._Y: np.ndarray = None
        self._x: np.ndarray = None
        self._n: int = None
        self._feature_name: str = None
        self._logger = logger_dpf()

    @property
    def Y(self) -> np.ndarray:
        """
        Vectorize the target column.
        """
        if self._Y is None:
            self._Y = self._vectorize(self.data, self.date_col)
        return self._Y

    @property
    def x(self) -> np.ndarray:
        """
        Vectorize the feature column.
        """
        if self._x is None and self._feature_name is not None:
            external_features = self.external_data[[self.date_col, self._feature_name]]
            self._x = self._vectorize(external_features, self.date_col).flatten()
        return self._x

    @property
    def n(self) -> int:
        """
        Get the length of the target column.
        """
        if self._n is None:
            self._n = len(self._x)
        return self._n

    def _vectorize(self, data: pd.DataFrame, date_col: str) -> np.ndarray:
        """
        Internal method to vectorize the data.
        """
        return data.set_index(date_col).sort_index().fillna(0.0).to_numpy()

    def _compute_li(self):
        """
        Internal method to compute the Li values.
        """
        # Initiate vectors
        Y = self.Y
        x = self.x

        # Compute Li values
        x_sorted = np.argsort(x)
        li = np.array([sum(y >= Y[x_sorted]) for y in Y[x_sorted]])

        return li

    def compute_xicorr(self, feature_name: str) -> Tuple[str, float]:
        """
        Compute the XiCorr correlation between the target column and a feature column.

        :param feature_name: The name of the feature column.
        :type feature_name: str
        :return: The feature name and the XiCorr correlation.
        :rtype: Tuple[str, float]
        """
        self._feature_name = feature_name

        li = self._compute_li()
        r = li.copy()
        n = self.n

        # Converge the ties
        for j in range(n):
            if sum([r[j] == r[i] for i in range(n)]) > 1:
                tie_index = np.array([r[j] == r[i] for i in range(n)])
                r[tie_index] = np.random.choice(
                    r[tie_index] - np.arange(0, sum([r[j] == r[i] for i in range(n)])),
                    sum(tie_index),
                    replace=False,
                )

        # Compute the XiCorr correlation
        try:
            xi_corr = 1 - n * sum(abs(r[1:] - r[: n - 1])) / (2 * sum(li * (n - li)))
        except ZeroDivisionError:
            xi_corr = 0.0
        except Exception as e:
            self._logger.log(logging.ERROR, f"ERROR COMPUTING XICORR FOR {self._feature_name} FEATURE: {e}")

        return feature_name, xi_corr[0]
