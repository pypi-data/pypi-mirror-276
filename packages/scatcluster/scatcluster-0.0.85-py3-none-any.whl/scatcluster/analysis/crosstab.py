"""Cross-Tab analysis module."""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.axes import Axes
from scipy.cluster import hierarchy
from sklearn.metrics import fowlkes_mallows_score

from scatcluster.analysis.dendrogram import get_leaves
from scatcluster.helper import COLORS


class SSNCrossTabAnalysis:
    """ScatCluster Add-on to run cross-analysis of different clusterings
    """

    def __init__(
        self,
        data_savepath: str = '/home/jovyan/shared/users/zerafa/data/sds.chris/scatcluster-sds/',
        data_network: str = 'ET',
        data_station: str = 'SOE0',
        data_location: str = '',
        network_sampling_rate_banks_pooling: str = '50_4_4_2_7_1_1_avg',
        ica_number: int = 10,
    ):
        """
        Initializes an instance of the SSNCrossTabAnalysis class.

        Parameters:
            data_savepath (str): The path to the directory where the data is saved.
                Defaults to '/home/jovyan/shared/users/zerafa/data/sds.chris/scatcluster-sds/'.
            data_network (str): The network name. Defaults to 'ET'.
            data_station (str): The station name. Defaults to 'SOE0'.
            data_location (str): The location name. Defaults to ''.
            network_sampling_rate_banks_pooling (str): The network sampling rate and banks pooling.
                Defaults to '50_4_4_2_7_1_1_avg'.
            ica_number (int): The number of ICA components. Defaults to 10.
        """
        self.data_savepath = data_savepath
        self.data_network = data_network
        self.data_station = data_station
        self.data_location = data_location
        self.network_sampling_rate_banks_pooling = network_sampling_rate_banks_pooling
        self.ica_number = ica_number

    def _get_predictions(self, win_size, num_clusters):
        """
        Retrieves predictions from a file based on provided window size and number of clusters.

        Parameters:
            self: SSNCrossTabAnalysis object
            win_size (int): Size of the window
            num_clusters (int): Number of clusters

        Returns:
            numpy array: Predictions from the file
        """
        file_path = (f'{self.data_savepath}clustering/{self.data_network}_{self.data_station}_{self.data_location}_'
                     f'{win_size}_{win_size}_{self.network_sampling_rate_banks_pooling}_ICA_{self.ica_number}_clusters_'
                     f'{num_clusters}.npz')
        return np.load(file_path)['predictions']

    def _build_crosstab_data(self,
                             cluster_1=3600,
                             num_clusters_1=10,
                             cluster_2=60,
                             num_clusters_2=10,
                             normalization=None):
        """
        Builds a crosstab data table based on the given parameters.

        Parameters:
            cluster_1 (int): The size of the first window cluster. Defaults to 3600.
            num_clusters_1 (int): The number of clusters for the first window cluster. Defaults to 10.
            cluster_2 (int): The size of the second window cluster. Defaults to 60.
            num_clusters_2 (int): The number of clusters for the second window cluster. Defaults to 10.
            normalization (str): The normalization option. Defaults to None.

        Returns:
            ct_data (pandas DataFrame): The crosstab data table.
            factor_difference (int): The factor difference between the two window clusters.
            fowlkes_mallows_score (float): The Fowlkes-Mallows score.
        """
        preds_1 = self._get_predictions(cluster_1, num_clusters_1)
        preds_2 = self._get_predictions(cluster_2, num_clusters_2)
        factor_difference = int(len(preds_2) / len(preds_1))

        print(
            f'Factor difference between predictions "{cluster_1}s window, {num_clusters_1} clusters" and "{cluster_2}s '
            f'window, {num_clusters_2} clusters": {factor_difference} \n')

        preds_1_modified = np.repeat(preds_1, factor_difference)

        df_preds = pd.DataFrame({'predictions_1': preds_1_modified, 'predictions_2': preds_2})

        normalization_options = ('all', 'index', 'columns')
        if normalization is None:
            ct_data = pd.crosstab(df_preds.predictions_1, df_preds.predictions_2)
        elif normalization in normalization_options:
            ct_data = pd.crosstab(df_preds.predictions_1, df_preds.predictions_2, normalize=normalization)
            ct_data = ct_data * 100
        else:
            raise ValueError(
                f"Provided Normalization is not valid. This can be 'None' or [{normalization_options}]. Kindly see "
                f'https://pandas.pydata.org/docs/reference/api/pandas.crosstab.html for more info.')
        ct_data = ct_data.sort_index(ascending=False)
        return ct_data, factor_difference, fowlkes_mallows_score(df_preds.predictions_1, df_preds.predictions_2)

    def plot_clustering_crosstab(self,
                                 cluster_1=3600,
                                 num_clusters_1=10,
                                 cluster_2=60,
                                 num_clusters_2=10,
                                 normalization=None,
                                 **kwargs):
        """
        Generates a clustering crosstab plot based on the provided parameters.

        Args:
            cluster_1 (int, optional): The size of the first window cluster. Defaults to 3600.
            num_clusters_1 (int, optional): The number of clusters in the first window cluster. Defaults to 10.
            cluster_2 (int, optional): The size of the second window cluster. Defaults to 60.
            num_clusters_2 (int, optional): The number of clusters in the second window cluster. Defaults to 10.
            normalization (str, optional): The type of normalization to apply to the crosstab data.
                Can be 'None', 'all', 'index', or 'columns'. Defaults to None.
            **kwargs: Additional keyword arguments to be passed to the `plt.subplots` function.

        Raises:
            ValueError: If the provided normalization is not one of the valid options.

        Note:
            This function generates a heatmap plot using the `sns.heatmap` function from the seaborn library.
            The heatmap shows the crosstab data between the two window clusters. The x-axis label indicates the size
            and number of clusters in the second window cluster, while the y-axis label indicates the size and number
            of clusters in the first window cluster. The title of the plot includes the Fowlkes-Mallows similarity
            score between the two clusterings. The plot is saved as a PNG file with a filename based on the provided
            parameters.
        """

        ct_data, _, fws = self._build_crosstab_data(cluster_1, num_clusters_1, cluster_2, num_clusters_2, normalization)

        _, ax = plt.subplots(figsize=(7, 7), **kwargs)
        _fmt = '.0f'
        if normalization is not None:
            _fmt = '.1f'
        s = sns.heatmap(ct_data, cmap='YlGnBu', annot=True, cbar=False, fmt=_fmt, linewidth=.5, ax=ax)
        _norm_title = ''
        if normalization is not None:
            for t in s.texts:
                t.set_text(t.get_text() + ' %')
            _norm_title = f'\nNormalization: {normalization}'
        ax.set_xlabel(f'{cluster_2}s window, {num_clusters_2} clusters')
        ax.set_ylabel(f'{cluster_1}s window, {num_clusters_1} clusters')
        ax.set_title(f'Comparison of Clusterings Predictions\nFWS similarity {fws * 100:.2f}%{_norm_title}')
        ax.xaxis.set_ticks_position('top')
        ax.xaxis.set_label_position('top')

        _norm_fname = ''
        if normalization is not None:
            _norm_fname = f'_Normalization_{normalization}'
        plt.savefig(
            f'{self.data_savepath}figures/{self.data_network}_{self.data_station}_{self.data_location}_'
            f'{self.network_sampling_rate_banks_pooling}_ICA_{self.ica_number}_crosstab_{_norm_fname}_{cluster_1}_'
            f'{num_clusters_1}_{cluster_2}_{num_clusters_2}.png')

    def _custom_dendrogram_crosstab(self, linkage: np.array, ax: Axes, depth: int = 30, orientation='left', factor=1):
        """
        Generate a custom dendrogram for a crosstab plot.

        Args:
            linkage (np.array): The linkage array generated by the hierarchical clustering algorithm.
            ax (Axes): The matplotlib Axes object to plot the dendrogram on.
            depth (int, optional): The depth of the dendrogram to display. Defaults to 30.
            orientation (str, optional): The orientation of the dendrogram. Can be 'left' or 'bottom'.
                Defaults to 'left'.
            factor (int, optional): A factor to multiply the population labels. Defaults to 1.

        Description:
            This function generates a custom dendrogram for a crosstab plot using the linkage array generated by the
             hierarchical clustering algorithm. The dendrogram is plotted on the provided matplotlib Axes object. The
             depth of the dendrogram, the orientation, and the population labels can be customized.

        Notes:
            - The dendrogram is generated using the `hierarchy.dendrogram` function from the `scipy.cluster.hierarchy`
                module.
            - The coordinates and population labels of the leaf nodes are extracted from the dendrogram information.
            - The leaf nodes are plotted on the Axes object using a scatter plot.
            - The population labels are formatted and displayed next to the leaf nodes.
        """
        with plt.rc_context({'lines.linewidth': 0.7}):
            dendrogram_infos = hierarchy.dendrogram(linkage,
                                                    p=depth,
                                                    truncate_mode='lastp',
                                                    color_threshold=0,
                                                    ax=ax,
                                                    orientation=orientation,
                                                    above_threshold_color='0.3',
                                                    count_sort=True,
                                                    labels=None,
                                                    show_leaf_counts=False)

            R = hierarchy.dendrogram(
                linkage,
                p=depth,
                truncate_mode='lastp',
                color_threshold=0,
                no_plot=True,
                orientation=orientation,
                above_threshold_color='0.3',
                count_sort=True,
                labels=None,
            )

        # Extract information
        coordinates, _ = get_leaves(dendrogram_infos, ax)

        # leave population
        pops = list(R['ivl'])

        # Plot leave nodes
        node_style = {'ms': 5, 'mec': '0.3', 'mew': 0.7, 'clip_on': False}
        for coordinate, color, pop in zip(coordinates, COLORS, pops):
            if orientation == 'left':
                ax.plot(0, coordinate, 'o', mfc=color, **node_style)
                index = int((coordinate - 5) / 10) + 1
                label = f"{index:d}\n{pop}\n{'[' + str(int(pop.replace('(', '').replace(')', '')) * factor) + ']'}"
                ax.text(-0.1, coordinate, label, color=color, va='center')
            if orientation == 'bottom':
                ax.plot(coordinate, 0, 'o', mfc=color, **node_style)
                index = int((coordinate - 5) / 10) + 1
                label = f'{index:d}\n{pop}'
                ax.text(coordinate, -0.1, label, color=color, ha='center')

    def _get_linkage(self, win_size):
        """
        Retrieves the linkage matrix from a file based on the provided window size.

        Parameters:
            win_size (int): The size of the window.

        Returns:
            numpy.ndarray: The linkage matrix.
        """
        return np.load(
            f'{self.data_savepath}clustering/{self.data_network}_{self.data_station}_{self.data_location}_{win_size}_'
            f'{win_size}_{self.network_sampling_rate_banks_pooling}_linkage.npy')

    def plot_crosstab_dendrograms(self,
                                  cluster_1=3600,
                                  num_clusters_1=10,
                                  cluster_2=60,
                                  num_clusters_2=10,
                                  normalization=None,
                                  **kwargs):
        """
        Plot crosstab dendrograms to compare clusterings predictions.

        Args:
            cluster_1 (int, optional): The size of the first window. Defaults to 3600.
            num_clusters_1 (int, optional): The number of clusters for the first window. Defaults to 10.
            cluster_2 (int, optional): The size of the second window. Defaults to 60.
            num_clusters_2 (int, optional): The number of clusters for the second window. Defaults to 10.
            normalization (str, optional): The type of normalization to apply. Defaults to None.
            **kwargs: Additional keyword arguments to be passed to plt.subplots().

        This function plots crosstab dendrograms to compare clusterings predictions. It first builds the crosstab data
        using the _build_crosstab_data() method. Then it creates a subplot with two rows and two columns using
            plt.subplots().
        The crosstab data is plotted using sns.heatmap() with the specified parameters. The x-axis label, y-axis label,
        and title of the subplot are set accordingly. The dendrogram for the first window is plotted using the
        _custom_dendrogram_crosstab() method. The dendrogram for the second window is plotted using the same method
        """

        ct_data, factor, fws = self._build_crosstab_data(cluster_1, num_clusters_1, cluster_2, num_clusters_2,
                                                         normalization)

        _, ax = plt.subplots(2,
                             2,
                             gridspec_kw={
                                 'width_ratios': [1, 8],
                                 'height_ratios': [8, 1]
                             },
                             figsize=(8, 8),
                             **kwargs)
        _fmt = '.0f'
        if normalization is not None:
            _fmt = '.1f'
        s = sns.heatmap(ct_data, cmap='YlGnBu', annot=True, cbar=False, fmt=_fmt, linewidth=.5, ax=ax[0, 1])
        _norm_title = ''
        if normalization is not None:
            for t in s.texts:
                t.set_text(t.get_text() + ' %')
            _norm_title = f'\nNormalization: {normalization}'
        ax[0, 1].set_xlabel(f'{cluster_2}s window, {num_clusters_2} clusters')
        ax[0, 1].set_ylabel(f'{cluster_1}s window, {num_clusters_1} clusters')
        ax[0, 1].set_title(f'Comparison of Clusterings Predictions\nFWS similarity {fws * 100:.2f}%{_norm_title}')
        ax[0, 1].xaxis.set_ticks_position('top')
        ax[0, 1].xaxis.set_label_position('top')
        ax[0, 1].yaxis.set_ticks_position('right')
        ax[0, 1].yaxis.set_label_position('right')

        linkage_1 = self._get_linkage(win_size=cluster_1)
        self._custom_dendrogram_crosstab(linkage=linkage_1, ax=ax[0, 0], depth=num_clusters_1, factor=factor)
        linkage_2 = self._get_linkage(win_size=cluster_2)
        self._custom_dendrogram_crosstab(linkage=linkage_2, ax=ax[1, 1], depth=num_clusters_2, orientation='bottom')

        ax[1, 0].set_axis_off()
        _norm_fname = ''
        if normalization is not None:
            _norm_fname = f'_Normalization_{normalization}'
        plt.savefig(
            f'{self.data_savepath}figures/{self.data_network}_{self.data_station}_{self.data_location}_'
            f'{self.network_sampling_rate_banks_pooling}_ICA_{self.ica_number}_crosstab_dendrogram_{_norm_fname}_'
            f'{cluster_1}_{num_clusters_1}_{cluster_2}_{num_clusters_2}.png')
