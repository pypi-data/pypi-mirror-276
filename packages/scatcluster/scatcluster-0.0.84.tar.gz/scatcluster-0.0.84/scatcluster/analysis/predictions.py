"""Predictions analysis module."""
import os

import matplotlib.pyplot as plt
import numpy as np
import obspy
import pandas as pd
from matplotlib import dates as mdates
from scipy.spatial.distance import euclidean
from tqdm import tqdm

from scatcluster.helper import COLORS


class Predictions:

    def identify_predicted_cluster_from_time_window(self, time_window: str) -> int:
        """Identify the predicted cluster from a provided Time Window

        Args:
            time_window (str): Time window in "YYYY-MM-DD HH-MM-SSSS"

        Raises:
            ValueError: Incorrect time window provided

        Returns:
            int: Predicted cluster id
        """
        time_window_num = mdates.date2num(obspy.UTCDateTime(time_window))
        position_in_time = len(self.dendrogram_timestamps[
            self.dendrogram_timestamps <= time_window_num,
        ])
        if position_in_time > 1:
            return self.dendrogram_predictions[position_in_time - 1]
        else:
            raise ValueError('Provided time_window is not valid')

    def df_times_for_predictions(self, n_clusters, cluster_rank=False) -> pd.DataFrame:
        """
        Get a pandas dataframe with columns {'times','predictions'} for the windowed seismograms
        and associated prediction

        Args:
            n_clusters (_type_): The number of clusters for the predition
            cluster_rank (bool, optional): Whether to calculate the inter-cluster rank. Defaults to False.

        Returns:
            _type_: A pandas dataframe with columns {'times','predictions'} for the windowed seismograms and predictions
        """
        self.load_data_times()

        # load cluster predictions
        clusters_path = (f'{self.data_savepath}clustering/{self.data_network}_{self.data_station}_{self.data_location}_'
                         f'{self.network_name}_ICA_{self.ica.n_components}_clusters_{n_clusters}.npz')
        if not os.path.exists(clusters_path):
            raise ValueError(
                f'Clusters of size {n_clusters} does not exist. Kindly choose another n_clusters or compute using'
                f' "single_dendrogram"')
        p = np.load(clusters_path)
        self.dendrogram_predictions = p['predictions']

        pd_times_preds = pd.DataFrame({
            'times_unix': self.data_times,
            'times_YYYYMMDD': [mdates.num2date(x) for x in self.data_times],
            'predictions': self.dendrogram_predictions
        })

        if cluster_rank is True:
            print('Calculating inter-cluster rank')
            pd_times_preds['cluster_rank'] = 0
            for cluster in np.unique(self.dendrogram_predictions):
                # Extract clusters
                within_cluster = self.dendrogram_predictions == cluster
                cluster_samples = self.ica_features[within_cluster]
                cluster_times = self.dendrogram_timestamps[within_cluster]

                # Centroid
                centroid = np.median(cluster_samples, axis=0)
                distances = []
                for sample in cluster_samples:
                    distances.append(euclidean(sample, centroid))
                distances = np.array(distances)

                # Sort times based on within cluster Euclidean distance
                distances_argsort = np.argsort(distances)
                sorted_times = cluster_times[distances_argsort]
                print(f'Processing cluster {cluster} of size {len(sorted_times)}')
                for st_enum, st in tqdm(enumerate(sorted_times)):
                    pd_times_preds.loc[pd_times_preds.times_unix == st, 'cluster_rank'] = st_enum

        self.pd_times_preds = pd_times_preds

        return self.pd_times_preds

    def plot_prediction_occurance(self, n_clusters):
        """
        Plots the occurrence of predictions in a scatter plot.

        Parameters:
            n_clusters (int): The number of clusters.

        """
        if self.data_times is None or self.dendrogram_predictions is None:
            self.pd_times_preds = self.df_times_for_predictions(n_clusters)

        df_preds = pd.DataFrame({
            'DATES': [mdates.num2date(x) for x in self.data_times],
            'predictions': self.dendrogram_predictions
        })
        for clust in np.unique(df_preds['predictions']):
            dt = df_preds.loc[
                df_preds['predictions'] == clust,
            ]
            plt.vlines(dt['DATES'], clust - 0.5, clust + 0.5, color=COLORS[clust])
        plt.yticks(range(1, df_preds['predictions'].max() + 1))
        plt.ylabel('Cluster')
        plt.show()

    def preload_predictions(self, ica_n_components, n_clusters):
        """
        Load precomputed predictions from a NumPy file.

        Parameters:
            ica_n_components (int): The number of ICA components used for prediction.
            n_clusters (int): The number of clusters used for prediction.

        Returns:
            numpy.ndarray: The loaded predictions.

        Raises:
            FileNotFoundError: If the specified file does not exist.
        """
        file_path = (f'{self.data_savepath}clustering/{self.data_network}_{self.data_station}_{self.data_location}_'
                     f'{self.network_name}_ICA_{ica_n_components}_clusters_{n_clusters}.npz')
        return np.load(file_path)
