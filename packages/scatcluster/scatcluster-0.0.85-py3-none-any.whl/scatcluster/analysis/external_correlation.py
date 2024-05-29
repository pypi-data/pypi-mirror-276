"""External Correlation analysis module."""
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import Lasso
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from scatcluster.helper import COLORS


class ExternalCorrelation:

    def plot_external_correlation(self,
                                  df_predictions: pd.DataFrame,
                                  df_external: pd.DataFrame,
                                  metric_list: List[str],
                                  title: str = None,
                                  **kwargs):
        """
        Plot external correlation between predictions and external data for each metric in the list.

        Parameters:
            df_predictions (pd.DataFrame): DataFrame containing predictions.
            df_external (pd.DataFrame): DataFrame containing external data.
            metric_list (List[str]): List of metrics to plot.
            title (str, optional): Title of the plot. Defaults to None.
            **kwargs: Additional keyword arguments for plt.subplots.
        """

        gs = {'height_ratios': [1] + [0.2] * len(metric_list)}
        _, axs = plt.subplots(len(metric_list) + 1, 1, figsize=(12, 10), sharex=True, gridspec_kw=gs, **kwargs)

        num_clusters = np.unique(df_predictions['predictions'])
        for clust in num_clusters:
            dt = df_predictions.loc[
                df_predictions['predictions'] == clust,
            ]
            axs[0].vlines(dt['dates'], clust - 0.5, clust + 0.5, color=COLORS[clust])
        axs[0].set_yticks(range(1, df_predictions['predictions'].max() + 1))
        axs[0].set_ylabel('Cluster')

        for metric_enum, metric in enumerate(metric_list):
            metric_enum += 1
            axs[metric_enum].plot(df_external['dates'], df_external[metric])
            axs[metric_enum].set_ylabel(metric, rotation=30)

        _title = '01_pre_truncate' if title is None else title
        plot_name = (f'{self.data_network}_{self.data_station}_{self.data_location}_{self.network_name}_ICA_'
                     f'{self.ica.n_components}_clusters_{num_clusters}_ExternalCorrelation_{_title}')
        plt.suptitle(plot_name)
        plt.savefig(f'{self.data_savepath}figures/{plot_name}.png')

    def merge_same_time_duration(
        self,
        df_predictions: pd.DataFrame,
        df_external: pd.DataFrame,
    ):
        """
        Merge two dataframes based on the same time duration.

        Parameters:
            df_predictions (pd.DataFrame): The dataframe containing the predictions.
            df_external (pd.DataFrame): The dataframe containing the external data.

        Returns:
            pd.DataFrame: The merged dataframe with the same time duration.

        This function takes two dataframes, `df_predictions` and `df_external`, and merges them based on the same time
        duration. It first determines the start and end dates of the common time duration by finding the maximum and
        minimum dates in both dataframes. Then, it truncates the dataframes to the same time duration by selecting only
        the rows within the common time duration. Finally, it merges the truncated dataframes on the 'dates' column,
        using a left join to include all rows from `df_predictions_same`. The merged dataframe is returned.
        """

        # Truncate data to the same time duration
        date_start = max(df_external.DATES.min(), df_predictions.DATES.min())
        date_end = min(df_external.DATES.max(), df_predictions.DATES.max())

        df_predictions_same = df_predictions.loc[
            ((df_predictions.DATES >= date_start) & (df_predictions.DATES <= date_end)),
        ]
        df_external_same = df_external.loc[
            ((df_external.DATES >= date_start) & (df_external.DATES <= date_end)),
        ]

        df_merge = pd.merge(left=df_predictions_same[['dates', 'predictions']],
                            left_on='dates',
                            right=df_external_same,
                            right_on='dates',
                            how='left')

        return df_merge

    def interpolate_missing_values(self, df_merge: pd.DataFrame, target_cols):
        """
        Interpolate missing values in the specified columns of a merged dataframe.

        Parameters:
            df_merge (pd.DataFrame): The merged dataframe containing the target columns.
            target_cols (List[str], optional): The list of columns to interpolate missing values for.
                Defaults to ['outTemp', 'outHumidity', 'barometer', 'windSpeed', 'windDir', 'windGust', 'windGustDir',
                'rain', 'rainRate', 'dewpoint'].

        Returns:
            pd.DataFrame: The merged dataframe with interpolated missing values in the specified columns.
        """
        if target_cols is None:
            target_cols = [
                'outTemp', 'outHumidity', 'barometer', 'windSpeed', 'windDir', 'windGust', 'windGustDir', 'rain',
                'rainRate', 'dewpoint'
            ]

        df_merge[target_cols] = df_merge[target_cols].interpolate(method='spline',
                                                                  limit_direction='both',
                                                                  order=1,
                                                                  axis=0)
        return df_merge

    def detection_rate(self,
                       df_merge: pd.DataFrame,
                       rolling_window_size: int = 48,
                       plot_detection: bool = True,
                       title: str = None):
        """
        Calculate the detection rate of clusters against weather data.

        Parameters:
            df_merge (pd.DataFrame): The merged dataframe containing the clusters and weather data.
            rolling_window_size (int, optional): The size of the rolling window for smoothing the data. Defaults to 48.
            plot_detection (bool, optional): Whether to plot the detection rate. Defaults to True.
            title (str, optional): The title of the plot. Defaults to None.

        Returns:
            pd.DataFrame: The dataframe containing the detection rate for each cluster.
        """
        # Use Detection Rate to determine the quality of Fit against Weather Data

        # Cluster OHE & Smoothing
        cluster_transformer = Pipeline(steps=[('encoder', OneHotEncoder(handle_unknown='ignore'))])
        df_clusters_OHE = cluster_transformer.fit_transform(np.array(df_merge.predictions).reshape(-1, 1))
        df_clusters_OHE = pd.DataFrame(df_clusters_OHE.todense(), columns=range(1, 11))
        df_detection_rate = df_clusters_OHE.rolling(rolling_window_size).mean()[rolling_window_size - 1:]

        if plot_detection:
            _, axs = plt.subplots(1, 1, figsize=(10, 5), sharex=True)
            num_clusters = np.unique(df_merge['predictions'])
            for clust in num_clusters:
                dt = df_merge.loc[
                    df_merge['predictions'] == clust,
                ]
                axs.vlines(dt['dates'], clust - 0.5, clust + 0.5, color=COLORS[clust])
                axs.plot(df_merge['dates'][rolling_window_size - 1:],
                         df_detection_rate[clust].values + clust - 0.5,
                         'k',
                         linewidth=0.5)
            axs.set_yticks(range(1, df_merge['predictions'].max() + 1))
            axs.set_ylabel('Cluster')

            _title = '03_cluster_detection' if title is None else title
            plot_name = (f'{self.data_network}_{self.data_station}_{self.data_location}_{self.network_name}_ICA_'
                         f'{self.ica.n_components}_clusters_{num_clusters}_ExternalCorrelation_{_title}')
            plt.suptitle(plot_name)
            plt.savefig(f'{self.data_savepath}figures/{plot_name}.png')
            plt.show()

        return df_detection_rate

    def external_data_smoothing_scaling(self,
                                        df_merge: pd.DataFrame,
                                        target_cols: List[str],
                                        rolling_window_size: int = 48,
                                        plot_external_data_smoothing: bool = True,
                                        title: str = None):
        """
        Applies smoothing and scaling to external data.

        Args:
            df_merge (pd.DataFrame): The merged dataframe containing the external data.
            target_cols (List[str]): The columns of the external data to be smoothed and scaled.
            rolling_window_size (int, optional): The size of the rolling window for smoothing. Defaults to 48.
            plot_external_data_smoothing (bool, optional): Whether to plot the smoothed and scaled data.
                Defaults to True.
            title (str, optional): The title for the plot. Defaults to None.

        Returns:
            pd.DataFrame: The smoothed and scaled external data.
        """
        # Weather Smoothing & Scaling
        df_weather_smoothed = df_merge[target_cols].rolling(rolling_window_size).mean()[rolling_window_size - 1:]
        weather_transformer = Pipeline(steps=[('scaler', StandardScaler())])
        df_weather_smoothed_scaled = pd.DataFrame(weather_transformer.fit_transform(df_weather_smoothed),
                                                  columns=df_weather_smoothed.columns)

        if plot_external_data_smoothing:
            _, axs = plt.subplots(len(df_weather_smoothed_scaled.columns), 1, figsize=(12, 10), sharex=True)
            for metric_enum, metric in enumerate(df_weather_smoothed_scaled.columns):
                axs[metric_enum].plot(df_merge['dates'], df_merge[metric])
                axs[metric_enum].plot(df_weather_smoothed_scaled['dates'], df_weather_smoothed_scaled[metric], 'k')
                axs[metric_enum].set_ylabel(metric, rotation=30)

            _title = '04_weather_smoothed' if title is None else title
            plot_name = (f'{self.data_network}_{self.data_station}_{self.data_location}_{self.network_name}_ICA_'
                         f'{self.ica.n_components}_clusters_{self.num_clusters}_ExternalCorrelation_{_title}')
            plt.suptitle(plot_name)
            plt.savefig(f'{self.data_savepath}figures/{plot_name}.png')
            plt.show()

        return df_weather_smoothed_scaled

    def external_correlation(self, df_clusters_smoothed, df_weather_smoothed_scaled, target_cols):
        """
        Calculates the external correlation between the smoothed and scaled clusters and the weather data.

        Parameters:
            df_clusters_smoothed (pd.DataFrame): The smoothed-clusters data.
            df_weather_smoothed_scaled (pd.DataFrame): The smoothed and scaled weather data.
            target_cols (list): The list of target columns to calculate the correlation for.

        Returns:
            tuple: A tuple containing two dictionaries. The first dictionary contains the scores of each target column,
                and the second dictionary contains the regression models for each target column.

        """
        # REGRESSION
        # LASSO = L1 : Lasso(fit_intercept=False, alpha=0.00001)
        # RIDGE = L2 : Ridge(fit_intercept=False, alpha=0.00001)
        # regression = LinearRegression(fit_intercept=False)

        SCORE = {}
        REGRESSION = {}
        for col in target_cols:
            regression = Lasso(fit_intercept=False, alpha=0.00001)
            regression.fit(df_clusters_smoothed, df_weather_smoothed_scaled[col])
            score = regression.score(df_clusters_smoothed, df_weather_smoothed_scaled[col])
            print(f'>>> {col} - score: {score}')
            REGRESSION[col] = regression
            SCORE[col] = score
        print(f'>> Best performing weather data {[k for k in SCORE.items() if k == max(SCORE.values())]}')
        print('\n')

        return SCORE, REGRESSION

    def min_max_vector(self, vector):
        """
        Normalizes a vector by scaling its values between 0 and 1.

        Parameters:
            vector (numpy.ndarray): The vector to be normalized.

        Returns:
            numpy.ndarray: The normalized vector.
        """
        x_min = vector.min()
        x_max = vector.max()
        return (vector - x_min) / (x_max - x_min)

    def plot_external_data_predicted_actual(self, df_clusters_smoothed, df_weather_smoothed_scaled, REGRESSION,
                                            target_cols):
        """
        Plot the actual and predicted weather data for each target column.

        Parameters:
            df_clusters_smoothed (DataFrame): The smoothed-clusters data.
            df_weather_smoothed_scaled (DataFrame): The smoothed and scaled weather data.
            REGRESSION (dict): A dictionary containing the regression models for each target column.
            target_cols (list): A list of target columns.

        """

        _, axs = plt.subplots(1, 1, figsize=(10, 6), sharex=True)
        for clust_enum, col in enumerate(target_cols):
            weather_mm = self.min_max_vector(df_weather_smoothed_scaled[col].values)
            prediction_weather = REGRESSION[col].predict(df_clusters_smoothed)
            prediction_mm = self.min_max_vector(prediction_weather)

            axs.plot(weather_mm + clust_enum, 'k', linewidth=0.5)
            axs.plot(prediction_mm + clust_enum, 'r', linewidth=0.5)
        axs.set_yticks(range(len(target_cols)))
        axs.set_yticklabels(target_cols)
        axs.legend(['Actual', 'Predicted'], loc='upper center', ncols=2, bbox_to_anchor=(0.5, -0.05))

        plot_name = (f'{self.data_network}_{self.data_station}_{self.data_location}_{self.network_name}_ICA_'
                     f'{self.ica.n_components}_clusters_{self.num_clusters}')
        plt.title(f'{plot_name}\nPredicted vs Actual Weather Data')
        plt.savefig(f'{self.data_savepath}figures/{plot_name}_05_pred_actual_weather.png')
        plt.show()

    def plot_detection_actual_prediction(
        self,
        target_cols,
        df_clusters_smoothed,
        df_weather_smoothed_scaled,
        REGRESSION,
    ):
        """
        Plot the actual and predicted detection rate data for each target column.

        Parameters:
            target_cols (list): A list of target columns.
            df_clusters_smoothed (DataFrame): The smoothed-clusters data.
            df_weather_smoothed_scaled (DataFrame): The smoothed and scaled weather data.
            REGRESSION (dict): A dictionary containing the regression models for each target column.

        """
        for col in target_cols:
            weather_mm = self.min_max_vector(df_weather_smoothed_scaled[col].values)
            prediction_weather = REGRESSION[col].predict(df_clusters_smoothed)
            prediction_mm = self.min_max_vector(prediction_weather)

            _, axs = plt.subplots(1, 1, figsize=(10, 6), sharex=True)
            for clust_enum, clust in enumerate(range(1, 11)):
                axs.plot(df_clusters_smoothed[clust] + clust_enum, 'b', linewidth=0.5)
                axs.plot(weather_mm + clust_enum, 'k', linewidth=0.5)
                axs.plot(prediction_mm + clust_enum, 'r', linewidth=0.5)
            axs.set_yticks(range(10))
            axs.set_yticklabels([x + 1 for x in range(10)])
            axs.legend(['Detection Rate', 'Actual', 'Predicted'],
                       loc='upper center',
                       ncols=3,
                       bbox_to_anchor=(0.5, -0.05))

            plot_name = (f'{self.data_network}_{self.data_station}_{self.data_location}_{self.network_name}_ICA_'
                         f'{self.ica.n_components}_clusters_{self.num_clusters}')
            plt.title(f'{plot_name}\n{col} - {self.SCORE[col]}')
            plt.savefig(f'{self.data_savepath}figures/{plot_name}_06_all_overlay_{col}.png')
            plt.show()

    def plot_regression_coefficients_contributions(self, target_cols, REGRESSION):
        """
        Plots the regression coefficients contributions for the specified target columns.

        Parameters:
            - self: the instance of the class
            - target_cols: a list of target columns
            - REGRESSION: the regression model

        """
        fig, ax = plt.subplots(figsize=[10, 5])

        regression_coefficients = np.abs(
            [np.array(np.array(REGRESSION[col].sparse_coef_.todense())[0]) for col in target_cols]).T
        cc = ax.imshow(regression_coefficients, aspect='auto', cmap='RdYlBu_r')

        fig.colorbar(cc, ax=ax, location='right')
        plt.xticks(range(10), target_cols, rotation=90)
        plt.xlabel('Weather data')
        plt.yticks(range(10))
        plt.ylabel('Cluster')

        plot_name = (f'{self.data_network}_{self.data_station}_{self.data_location}_{self.network_name}_ICA_'
                     f'{self.ica.n_components}_clusters_{self.num_clusters}')
        plt.title(f'{plot_name}\nRegression Coefficient Contribution of Weather Data')
        plt.savefig(f'{self.data_savepath}figures/{plot_name}_07_Reg_Coeff.png')
        plt.show()

    def plot_regression_coefficients(self, df_clusters_smoothed, df_weather_smoothed_scaled, REGRESSION, SCORE,
                                     target_cols):
        """
        Plots the regression coefficients for the specified target columns.

        Parameters:
            df_clusters_smoothed (DataFrame): The smoothed-clusters data.
            df_weather_smoothed_scaled (DataFrame): The smoothed and scaled weather data.
            REGRESSION (dict): A dictionary containing the regression models for each target column.
            SCORE (dict): A dictionary containing the scores for each regression model.
            target_cols (list): A list of target columns.

        """
        _, axs = plt.subplots(5, 2, figsize=(8, 8), sharex=True, sharey=True)
        ROW = 0
        COL = -1
        for col_enum, col in enumerate(target_cols):
            weather_mm = self.min_max_vector(df_weather_smoothed_scaled[col].values)
            prediction_weather = REGRESSION[col].predict(df_clusters_smoothed)
            prediction_mm = self.min_max_vector(prediction_weather)

            COL += 1
            if col_enum % 2 == 0 and col_enum > 0:
                ROW += 1
                COL = 0

            axs[ROW, COL].scatter(weather_mm, prediction_mm, s=0.2)
            axs[ROW, COL].set_title(f'{col}-{round(SCORE[col], 4)}')

            if COL == 0:
                axs[ROW, COL].set_ylabel('Weather Predicted')
            if ROW == 4:
                axs[ROW, COL].set_xlabel('Weather Actual')

        plot_name = (f'{self.data_network}_{self.data_station}_{self.data_location}_{self.network_name}_ICA_'
                     f'{self.ica.n_components}_clusters_{self.num_clusters}')
        plt.suptitle(f'{plot_name}\nCorrelation of Weather data')
        plt.savefig(f'{self.data_savepath}figures/{plot_name}_08_weather_corr.png')
        plt.show()
