"""Waveform Correlations Analysis module."""
import datetime
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from obspy import UTCDateTime
from obspy.signal.cross_correlation import correlate, xcorr_max
from tqdm import tqdm

# EXAMPLE
# calculate_waveform_correlations(sort_type ='distance_filter', sort_filter=100, envelope=True)
# plot_correlation_waveforms(correlations=correlations_waveforms_distance_100, sort_type ='distance_filter',
# sort_filter=100, envelope=False)


class WaveformCorrelations:

    def process_cluster_trace_correlation(self,
                                          df_preds: pd.DataFrame,
                                          cluster: int = 1,
                                          sort_type: str = 'all',
                                          sort_filter: int = None,
                                          time_second: int = 60,
                                          channel: str = 'HHZ',
                                          envelope: bool = False):
        """
        Calculate the waveform trace correlation for a given cluster.

        Args:
            df_preds (pd.DataFrame): The DataFrame containing the predictions.
            cluster (int, optional): The cluster number. Defaults to 1.
            sort_type (str, optional): The type of sorting to apply. Options are 'all', 'xcorr_filter', and
                'distance_filter'. Defaults to 'all'.
            sort_filter (int, optional): The filter value for sorting. Defaults to None.
            time_second (int, optional): The time window in seconds. Defaults to 60.
            channel (str, optional): The channel to use. Defaults to 'HHZ'.
            envelope (bool, optional): Whether to use the envelope. Defaults to False.

        Returns:
            dict: A dictionary containing the centre waveform time, centre waveform, and correlations.
        """
        # sort_type = ['all', 'xcorr_filter', 'distance_filter']

        df_times = df_preds.loc[df_preds.predictions == cluster, ['cluster_rank', 'times_YYYYMMDD']]
        time_list = df_times.sort_values(by='cluster_rank')['times_YYYYMMDD'].to_list()

        if sort_type == 'distance_filter':
            if sort_filter is None:
                msg = ("If using \'sort_type\' => distance_filter, you need to supply \'sort_filter\' of type integer. "
                       "\n This will be used to take the waveforms up to the n\'th based on the Euclidean distance \n "
                       'from the cluster centroid.')
                raise ValueError(msg)
            time_list = time_list[:sort_filter + 1]

        wvf0_time = time_list.pop(0)

        wvf0 = self.get_waveform(start_time=str(wvf0_time), time_second=time_second, channel=channel, envelope=envelope)
        if len(wvf0) < 1:
            print(f'  Waveform cross-correlations cannot be computed for Cluster {cluster}.\n' +
                  '  The waveform in the centre of the cluster contains no traces. This \n' +
                  '  is most likely a cluster of damaged/missing data.')
            # return None
        else:
            time_per_sample = 1 / wvf0[0].stats.sampling_rate
            wvf0 = wvf0.select(component='Z')[0].data

            corr = []
            for st_enum, st in tqdm(enumerate(time_list)):
                wvf1 = self.get_waveform(start_time=str(st),
                                         time_second=time_second,
                                         channel=channel,
                                         envelope=envelope)
                if len(wvf1) > 0:
                    wvf1 = wvf1.select(component='Z')[0].data
                    cc = correlate(wvf0, wvf1, len(wvf0))
                    shift, value = xcorr_max(cc)
                    _sort_filter = 0
                    if sort_type == 'xcorr_filter':
                        if sort_filter > 1:
                            msg = ('If using \'sort_type\' => xcorr_filter, you need to \'supply sort_filter\' \n'
                                   'of type float corresponding to the absolute maximum cross-correlation \n'
                                   'coefficient to include in analysis.')
                            raise ValueError(msg)
                        _sort_filter = sort_filter
                    if abs(value) >= _sort_filter:
                        time_start2 = UTCDateTime(str(st)) + datetime.timedelta(seconds=-1 * shift * time_per_sample)
                        shifted_correlated_waveform = [-1 if value < 0 else 1] * self.get_waveform(
                            start_time=time_start2, envelope=envelope)[0].data
                        corr.append({
                            'cluster_rank': st_enum + 1,
                            'correlation_value': value,
                            'correlation_shift': shift,
                            'waveform_time': str(st),
                            'waveform': wvf1,
                            'shifted_correlated_waveform_time': str(time_start2),
                            'shifted_correlated_waveform': shifted_correlated_waveform
                        })

            return {'centre_waveform_time': str(wvf0_time), 'centre_waveform': wvf0, 'correlations': corr}

    def calculate_waveform_correlations(self,
                                        df_preds: pd.DataFrame,
                                        sort_type='distance_filter',
                                        sort_filter=100,
                                        time_second=60,
                                        channel='HHZ',
                                        envelope=False):
        """
        Calculate the waveform correlations for each cluster based on the input DataFrame of predictions.

        Args:
            df_preds (pd.DataFrame): The DataFrame containing the predictions.
            sort_type (str, optional): The type of sorting to apply. Defaults to 'distance_filter'.
            sort_filter (int, optional): The filter value for sorting. Defaults to 100.
            time_second (int, optional): The time window in seconds. Defaults to 60.
            channel (str, optional): The channel to use. Defaults to 'HHZ'.
            envelope (bool, optional): Whether to use the envelope. Defaults to False.

        Returns:
            dict: A dictionary containing the waveform correlations for each cluster.
        """

        correlations = {}
        for cluster in set(df_preds.predictions):
            corr = self.process_cluster_trace_correlation(df_preds, cluster, sort_type, sort_filter, time_second,
                                                          channel, envelope)
            correlations[cluster] = corr

        _wvf_type = 'waveform'
        if envelope:
            _wvf_type = 'envelope'
        save_file = (f'{self.data_savepath}data/{self.data_network}_{self.data_station}_{self.data_location}_'
                     f'{self.network_name}_ICA_{self.ica.n_components}_clustering_{self.ica.n_components}_{_wvf_type}_'
                     f'correlations_{sort_type}_{sort_filter}.pkl')
        with open(save_file, 'wb') as handle:
            pickle.dump(correlations, handle, protocol=pickle.HIGHEST_PROTOCOL)

        return correlations

    def load_correlations(self, sort_type='distance_filter', sort_filter=100, envelope=False):
        """
        Load the waveform correlations from a pickle file.

        Args:
            sort_type (str, optional): The type of sorting to be applied to the correlations.
                Defaults to 'distance_filter'.
            sort_filter (int, optional): The filter to be applied to the sorted correlations. Defaults to 100.
            envelope (bool, optional): Whether to use the envelope of the waveform. Defaults to False.

        Returns:
            dict: A dictionary containing the waveform correlations.
        """
        _wvf_type = 'waveform'
        if envelope:
            _wvf_type = 'envelope'
        save_file = (f'{self.data_savepath}data/{self.data_network}_{self.data_station}_{self.data_location}_'
                     f'{self.network_name}_ICA_{self.ica.n_components}_clustering_{self.ica.n_components}_{_wvf_type}_'
                     f'correlations_{sort_type}_{sort_filter}.pkl')
        with open(save_file, 'rb') as handle:
            correlations = pickle.load(handle)

        return correlations

    def stack_correlations(self, correlations, cluster):
        """
        Calculate the stacked correlations for a given cluster.

        Parameters:
            correlations (dict): A dictionary containing the correlations for different clusters.
            cluster (int): The cluster number.

        Returns:
            numpy.ndarray or None: The stacked correlations for the given cluster, or None if the cluster is not
                present in the correlations' dictionary.
        """
        if correlations[cluster] is None:
            return None
        else:
            waveforms = [x['shifted_correlated_waveform'] for x in correlations[cluster]['correlations']]
            return np.mean(waveforms, axis=0)

    def process_waveform_correlations_stacked_waveform(self,
                                                       df_preds,
                                                       correlations,
                                                       sort_type,
                                                       sort_filter,
                                                       envelope=False):
        """
        Process the waveform correlations and stack the correlated waveforms for each cluster.

        Args:
            df_preds (pandas.DataFrame): The DataFrame containing the predictions.
            correlations (dict): A dictionary containing the correlations for different clusters.
            sort_type (str): The type of sorting to apply.
            sort_filter (int): The filter value for sorting.
            envelope (bool, optional): Whether to use the envelope. Defaults to False.

        Returns:
            dict: A dictionary containing the stacked correlated waveforms for each cluster.

        This function iterates over the unique clusters in the predictions DataFrame and calculates the stacked
        correlated waveforms for each cluster using the `stack_correlations` method. The resulting stacked correlated
        waveforms are stored in the `correlation_waveform` dictionary.

        The `_wvf_type` variable is set to 'waveform' by default. If the `envelope` parameter is True, `_wvf_type` is
        set to 'envelope'.

        The `correlation_waveform` dictionary is then saved as a NumPy binary file using the `np.save` function. The
        file name is constructed using various attributes of the instance (`self`) and the input parameters.

        Finally, the `correlation_waveform` dictionary is returned.
        """
        correlation_waveform = {}
        for cluster in set(df_preds.predictions):
            correlation_waveform[cluster] = self.stack_correlations(correlations, cluster)

        _wvf_type = 'waveform'
        if envelope:
            _wvf_type = 'envelope'
        np.save(
            f'{self.data_savepath}data/{self.data_network}_{self.data_station}_{self.data_location}_'
            f'{self.network_name}_ICA_{self.ica.n_components}_clustering_{self.ica.n_components}_{_wvf_type}_'
            f'correlations_stacked_waveform_{sort_type}_{sort_filter}.npy', correlation_waveform)

        return correlation_waveform

    def plot_correlation_waveforms(self, df_preds, correlations, sort_type, sort_filter, envelope=False):
        """
        Plot the correlation waveforms for each cluster.

        Parameters:
            df_preds (pandas.DataFrame): The DataFrame containing the predictions.
            correlations (dict): A dictionary containing the correlations for different clusters.
            sort_type (str): The type of sorting to apply.
            sort_filter (int): The filter value for sorting.
            envelope (bool, optional): Whether to use the envelope. Defaults to False.

        This function plots the correlation waveforms for each cluster. It first calculates the correlation waveform
        using the `process_waveform_correlations_stacked_waveform` method. Then, it creates a figure with subplots for
        each cluster. If the cluster has no correlations, the subplot title is set to 'Cluster {cluster_number} -
        Empty Traces'. Otherwise, it plots the shifted and corrected waveforms, the centroid waveform, and the
        correlation waveform for that cluster. The subplot title includes the number of traces, the average
        cross-correlation coefficient, and the type of waveform. The figure legend includes labels for the shifted and
        corrected waveforms, the centroid waveform, and the correlation waveform. The figure is saved as a PNG image
        with a unique file name based on the data network, station, location, network name, ICA components, clustering
        method, and waveform type. The plot is displayed using `plt.show()`.
        """

        correlation_waveform = self.process_waveform_correlations_stacked_waveform(df_preds, correlations, sort_type,
                                                                                   sort_filter, envelope)

        fig, ax = plt.subplots(len(set(df_preds.predictions)), 1, figsize=(20, 10), sharex=True, sharey=True)
        for clust_enum, cluster in enumerate(correlations.keys()):
            if correlations[cluster] is None:
                ax[clust_enum].set_title(f'Cluster {clust_enum + 1} - Empty Traces')
            else:
                lines = []
                num_traces = len(correlations[cluster]['correlations'])
                avg_xcorr = np.mean([x['correlation_value'] for x in correlations[cluster]['correlations']])
                ax[clust_enum].set_title(
                    f'Cluster {clust_enum + 1}: Number of Traces {num_traces}: Avg. Cross-correlation Coeff. '
                    f'{avg_xcorr:.3}')
                for x in correlations[cluster]['correlations'][:100]:
                    lines += ax[clust_enum].plot(x['shifted_correlated_waveform'],
                                                 color='b',
                                                 alpha=0.2,
                                                 linewidth=1,
                                                 label='shifted_correlated_waveforms')

                centre_waveform = correlations[cluster]['centre_waveform']
                centre_waveform_shift = np.mean(np.abs(centre_waveform)) * .5
                lines += ax[clust_enum].plot(centre_waveform,
                                             color='k',
                                             alpha=0.3,
                                             linewidth=1,
                                             label='centre_waveform')
                ax[clust_enum].set_ylim(
                    [min(centre_waveform) - centre_waveform_shift,
                     max(centre_waveform) + centre_waveform_shift])

                lines += ax[clust_enum].plot(correlation_waveform[cluster],
                                             color='r',
                                             linewidth=0.5,
                                             label='correlation_waveform')

        _wvf_type = 'Waveform'
        if envelope:
            _wvf_type = 'Envelope'

        fig.legend(lines[-3:],
                   [f'Shifted and corrected {_wvf_type}s', f'Centroid {_wvf_type}', f'Correlation {_wvf_type}'],
                   loc='upper center',
                   ncol=3,
                   bbox_to_anchor=(0.5, -0.01))
        ax[0].margins(x=0)

        file_name = (f'{self.data_network}_{self.data_station}_{self.data_location}_{self.network_name}_ICA_'
                     f'{self.ica.n_components}_clustering_{self.ica.n_components}_{_wvf_type}_Correlations_{sort_type}'
                     f'_{sort_filter}')
        plt.suptitle(file_name)
        plt.savefig(f'{self.data_savepath}figures/{file_name}.png', bbox_inches='tight')
        plt.show()

    def plot_correlation_frequency(self, df_preds, correlations_waveforms_distance_all):
        """
        Plot the correlation frequency for each cluster.

        Parameters:
            df_preds (pandas.DataFrame): The DataFrame containing the predictions.
            correlations_waveforms_distance_all (dict): A dictionary containing the correlations and waveforms distance
            for different clusters.

        This function plots the correlation frequency for each cluster. It creates a figure with subplots for each
        cluster. If the cluster has no correlations, the subplot title is set to 'Cluster {cluster_number} - Empty
        Traces'. Otherwise, it calculates the absolute value of the correlation_value for each correlation in the
        cluster and plots a histogram of the data using seaborn. The subplot title includes the cluster number.
        The figure is displayed using `plt.show()`.
        """
        _, ax = plt.subplots(len(set(df_preds.predictions)), 1, figsize=(20, 10), sharex=True, sharey=True)
        for clust_enum, cluster in enumerate(correlations_waveforms_distance_all.keys()):
            if correlations_waveforms_distance_all[cluster] is None:
                ax[clust_enum].set_title(f'Cluster {clust_enum + 1} - Empty Traces')
            else:
                data = [
                    np.abs(xcor['correlation_value'])
                    for xcor in correlations_waveforms_distance_all[cluster]['correlations']
                ]
                sns.histplot(data, ax=ax[clust_enum])
                ax[clust_enum].set_title(f'Cluster {clust_enum + 1} ')

        plt.show()

    def plot_correlation_shift(self, correlations: dict, clusters: list, within_cluster_number: int = None):
        """
        Plot the correlation shift for each cluster.

        Parameters:
            correlations (dict): A dictionary containing the correlations for each cluster.
            clusters (list): A list of clusters.
            within_cluster_number (int, optional): The number of correlations to plot within each cluster.
                Defaults to None.

        """

        _within_cluster_number = 100 if within_cluster_number is None else within_cluster_number

        _, ax = plt.subplots(2, len(clusters), figsize=(20, 10), sharex=True, sharey=True)
        for cluster_enum, cluster in enumerate(clusters):
            ax[0, cluster_enum].plot(correlations[cluster]['centre_waveform'], 'k')
            for x_enum, x in enumerate(correlations[cluster]['correlations'][:_within_cluster_number]):
                ax[1, cluster_enum].plot(x['waveform'] + ((x_enum + 1) * 0.0000001), 'b', alpha=0.2)
            plt.title(f'Cluster {cluster}')

        file_name = (f'{self.data_network}_{self.data_station}_{self.data_location}_{self.network_name}_ICA_'
                     f'{self.ica.n_components}_clustering_{self.ica.n_components}_{self._wvf_type}_Correlations')
        plt.suptitle(f'{file_name}\nWaveform Correlations')
        plt.savefig(f'{self.data_savepath}figures/{file_name}_Cluster_waveform_correlations.png', bbox_inches='tight')
        plt.show()
