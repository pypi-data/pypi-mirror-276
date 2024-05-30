'''
Class to preprocessing data
'''

#pylint: disable=too-many-instance-attributes

import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler
from google.cloud import bigquery

client = bigquery.Client()


class PreprocesingData:
    """
    Class to preprocessing data.
    """
    def __init__(
            self,
            data,
            sqrt_col = [],
            log_default = [],
            extensive_log = [],
            boxcox_zero = [],
            log_x_divide_2 = [],
            no_transform = []
            ):

        self.transform_data = data.copy()
        self.data_client = self.transform_data['id_client']
        self.sqrt_col = sqrt_col
        self.log_default = log_default
        self.extensive_log = extensive_log
        self.boxcox_zero = boxcox_zero
        self.log_x_divide_2 = log_x_divide_2
        self.no_transform = no_transform

    def sqrt_transformation(self, column):
        """Sqrt transformation

        Parameters
        ----------
        column : list
            List of column to transform.
        """
        self.transform_data[column] = np.sqrt(self.transform_data[column])

    def log_default_transformation(self, column, value_add):
        """Log transformation

        Parameters
        ----------
        column : list
            List of column to transform.
        """
        self.transform_data[column] = np.log(self.transform_data[column] + value_add)

    def ihs_transformation(self, column):
        """IHS transformation

        Parameters
        ----------
        column : list
            List of column to transform.
        """
        self.transform_data[column] = np.arcsinh(self.transform_data[column])

    def extensive_log_transformation(self, column):
        """Extensive log transformation

        Parameters
        ----------
        column : list
            List of column to transform.
        """
        min_data = self.transform_data[column].min()
        self.transform_data[column] = self.transform_data[column].apply(
            lambda x: np.log(x - (min_data - 1)))

    def boxcox_zero_transformation(self, column):
        """Boxcox transformation

        Parameters
        ----------
        column : list
            List of column to transform.
        """
        posdata = self.transform_data[self.transform_data[column] > 0][column]
        bcdata, lam = stats.boxcox(posdata)
        boxcox = np.empty_like(self.transform_data[column])
        boxcox[self.transform_data[column] > 0] = bcdata
        boxcox[self.transform_data[column] == 0] = -1/lam
        self.transform_data[column] = boxcox

    def log_x_divide_2_transformation(self, column):
        """Log transformation

        Parameters
        ----------
        column : list
            List of column to transform.
        """
        min_non_zero = self.transform_data[self.transform_data[column]>0][column].min()
        self.transform_data[column] = np.log(self.transform_data[column]+(min_non_zero/2))

    def func_transform_data(self):
        """ Function to transform all data. 

        Returns
        -------
        pd.Dataframe
            Transformed dataframe.
        """
        for column in self.log_default:
            if column in self.transform_data.columns:
                self.log_default_transformation(column, 0.01)
        for column in self.sqrt_col:
            if column in self.transform_data.columns:
                self.sqrt_transformation(column)
        for column in self.extensive_log:
            if column in self.transform_data.columns:
                self.extensive_log_transformation(column)
        for column in self.boxcox_zero:
            if column in self.transform_data.columns:
                self.boxcox_zero_transformation(column)
        for column in self.log_x_divide_2:
            if column in self.transform_data.columns:
                self.log_x_divide_2_transformation(column)
        return self.transform_data

    def standardization(self):
        """ Standarization 

        Returns
        -------
        pd.Dataframe
            Transformed dataframe.
        """
        scaler = StandardScaler()
        dataframe_no_client = self.transform_data.drop('id_client', axis=1)
        self.transform_data = pd.DataFrame(scaler.fit_transform(dataframe_no_client),
                                           index=dataframe_no_client.index,
                                           columns=dataframe_no_client.columns)
        self.transform_data = pd.concat([self.data_client, self.transform_data], axis=1)
        return self.transform_data
