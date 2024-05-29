"""Analysis Waveforms module."""
import datetime
from glob import glob
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import obspy
import pandas as pd
from matplotlib import dates as mdates
from obspy.core import UTCDateTime
from scipy.spatial.distance import euclidean

from scatcluster.helper import COLORS, is_gpu_available


class Waveforms:

    def plot_waveforms_per_cluster(self, clusters: List[int] = None, waveforms_n_samples: int = None, **kwargs):
        """
        Visualise Waveforms for All or a select number of clusters.

        Args:
            clusters (List[int], optional): If specified, only plot waveforms for clusters in list of integers.
            For example, clusters = [1,3] will produce waveforms for cluster 1 and 3 only.
            Defaults to None will produce waveforms for all clusters.
            waveforms_n_samples (int, optional): Number of waveforms to plot. Defaults to None.
            **kwargs: Additional keyword arguments to pass to plt.subplots().
        """
        # get channel list from plotting
        stream = self.load_data(starttime=UTCDateTime(self.data_sample_starttime),
                                endtime=UTCDateTime(self.data_sample_endtime),
                                channel=self.data_channel)
        channel_list = sorted(trace.stats.channel for trace in stream)

        if clusters is not None:
            classes = clusters
        else:
            # Calculate centroid
            classes = np.unique(self.dendrogram_predictions)

        for cluster in classes:

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

            # Extract the best waveforms timestamps
            _waveforms_n_samples = 5 if waveforms_n_samples is None else waveforms_n_samples
            distances_argsort = np.argsort(distances)
            sorted_times = cluster_times[distances_argsort][:_waveforms_n_samples]
            sorted_times = mdates.num2date(sorted_times)
            kwargs['figsize'] = (20, 8) if kwargs.get('figsize') is None else kwargs.get('figsize')
            _, ax = plt.subplots(1, 4, gridspec_kw={'width_ratios': [2, 2, 2, 1]}, **kwargs)
            for ch, channel in enumerate(channel_list):
                yticks = []
                for index, t in enumerate(sorted_times):
                    start = obspy.UTCDateTime(t)
                    end = start + self.network_segment
                    stream = self.load_data(starttime=start, endtime=end, channel=self.data_channel)
                    if len(stream) > 0:
                        trace = stream[0]
                        data = trace.data
                        data /= np.abs(data).max()
                        ax[ch].plot(trace.times(), data + index, lw=0.3)
                        yticks.append(start)
                    else:
                        print(f'Trace is not available between {start}-{end} for supplied parametrization')
                ax[ch].set_title(f'channel {channel}')
            ax[0].set_yticks(range(len(yticks)), [x.strftime('%Y-%m-%d %H:%M:%S') for x in yticks])
            self.show_dendrogram_waveforms(linkage=self.dendrogram_linkage,
                                           ax=ax[3],
                                           depth=len(np.unique(self.dendrogram_predictions)))
            ax[3].set_title('Dendrogram')
            self._set_share_axes(axs=ax[:2], sharex=True, sharey=True)
            plt.suptitle(f'{self.data_network}_{self.data_station}_{self.data_location}_{self.network_name}_ICA_'
                         f'{self.ica.n_components}_clustering_{clusters}\nCluster {cluster}')

            plt.savefig(
                f'{self.data_savepath}figures/{self.data_network}_{self.data_station}_{self.data_location}_'
                f'{self.network_name}_ICA_{self.ica.n_components}_clustering_{clusters}_waveforms_cluster_{cluster}.png'
            )

            plt.show()

    def plot_all_waveforms(self, channel='HHZ', waveforms_n_samples=3, **kwargs):
        """
        Plots waveforms for all or a select number of clusters.

        Args:
            channel (str, optional): The channel to plot waveforms for. Defaults to 'HHZ'.
            waveforms_n_samples (int, optional): The number of waveforms to plot. Defaults to 3.
            **kwargs: Additional keyword arguments to pass to plt.subplots().

        Prints:
            Trace is not available between {start}-{end} for supplied parametrization

        Saves:
            A figure of waveforms for all clusters as a PNG file.

        """
        classes = np.unique(self.dendrogram_predictions)
        _waveforms_n_samples = 5 if waveforms_n_samples is None else waveforms_n_samples
        kwargs['figsize'] = (20, 8) if kwargs.get('figsize') is None else kwargs.get('figsize')
        _, ax = plt.subplots(
            _waveforms_n_samples,
            len(classes),
            # sharey=True,
            sharex=True,
            #  gridspec_kw={'width_ratios': [2, 2, 2, 1]},
            **kwargs)

        for cluster_enum, cluster in enumerate(classes):
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

            # Extract the best waveforms timestamps

            distances_argsort = np.argsort(distances)
            sorted_times = cluster_times[distances_argsort][:_waveforms_n_samples]
            sorted_times = mdates.num2date(sorted_times)

            for index, t in enumerate(sorted_times):
                start = obspy.UTCDateTime(t)
                end = start + self.network_segment
                stream = self.load_data(starttime=start, endtime=end, channel=channel)
                if len(stream) > 0:
                    trace = stream[0]
                    stream_data = trace.data
                    ax[index, cluster_enum].plot(trace.times(), stream_data, lw=0.3, color=COLORS[cluster_enum])
                    ax[index, cluster_enum].annotate(start.strftime('%Y/%m/%d %H:%M:%S'),
                                                     xy=(0, 1),
                                                     xycoords='axes fraction',
                                                     horizontalalignment='left',
                                                     verticalalignment='top')
                else:
                    print(f'Trace is not available between {start}-{end} for supplied parametrization')

            ax[0, cluster_enum].set_title(f'Cluster {cluster}')
        _ = [axc.set_axis_off() for axr in ax for axc in axr]
        plt.subplots_adjust(wspace=0, hspace=0)
        plt.suptitle(f'{self.data_network}_{self.data_station}_{self.data_location}_{self.network_name}_ICA_'
                     f'{self.ica.n_components}_clustering_{len(classes)}')

        plt.savefig(
            f'{self.data_savepath}figures/{self.data_network}_{self.data_station}_{self.data_location}_'
            f'{self.network_name}_ICA_{self.ica.n_components}_clustering_{len(classes)}_all_clusters_waveforms.png')

        plt.show()

    def get_waveform(self, start_time='2022-01-01T00:00:00+00:00', time_second=60, channel='HHZ', envelope=False):
        """
        Retrieves a waveform from the data source within a specified time range and channel.

        Args:
            start_time (str, optional): The start time of the waveform in ISO format.
                Defaults to '2022-01-01T00:00:00+00:00'.
            time_second (int, optional): The duration of the waveform in seconds. Defaults to 60.
            channel (str, optional): The channel of the waveform. Defaults to 'HHZ'.
            envelope (bool, optional): Whether to process the waveform with the envelope function. Defaults to False.

        Returns:
            obspy.core.stream.Stream: The waveform data as an ObsPy Stream object.
        """
        time_start = UTCDateTime(str(start_time))
        time_end = UTCDateTime(str(start_time)) + datetime.timedelta(seconds=time_second)
        wvf = self.load_data(starttime=time_start, endtime=time_end, channel=channel)
        if envelope:
            wvf = self.process_stream_envelope(wvf)
        return wvf

    def retreive_scat_vector(self,
                             scat_coef_vectorized,
                             scat_coef_vectorized_index,
                             num_channels=3,
                             scat_vec_size_first_order=16,
                             scat_vec_size_second_order=(16, 7)):
        """
        Retrieves the scattering vector from the given `scat_coef_vectorized` array at the specified
            `scat_coef_vectorized_index`.

        Args:
            scat_coef_vectorized (ndarray): The array containing the scattering coefficients.
            scat_coef_vectorized_index (int): The index of the scattering coefficient vector to retrieve.
            num_channels (int, optional): The number of channels. Defaults to 3.
            scat_vec_size_first_order (int, optional): The size of the first-order scattering vector. Defaults to 16.
            scat_vec_size_second_order (tuple, optional): The size of the second-order scattering vector.
                Defaults to (16, 7).

        Returns:
            tuple: A tuple containing the first-order scattering vector and the second-order scattering vector.
        """
        scat_vec = scat_coef_vectorized[scat_coef_vectorized_index, :]
        scat_vec_first_order = scat_vec[:(num_channels * scat_vec_size_first_order)].reshape(
            num_channels, scat_vec_size_first_order)
        scat_vec_second_order = scat_vec[(num_channels * scat_vec_size_first_order):].reshape(
            num_channels, scat_vec_size_second_order[0], scat_vec_size_second_order[1])
        return scat_vec_first_order, scat_vec_second_order

    def process_waveforms_envelopes_scat_coefficients(self, df_preds):
        """
        Process waveforms, envelopes, and scattering coefficients.

        This function takes in a DataFrame `df_preds` containing predictions and processes waveforms, envelopes, and
        scattering coefficients. It loads the scattering coefficient vectorized data using the
        `load_scat_coef_vectorized` method. It then retrieves the scattering coefficient file list based on the data
        savepath, data network, data station, data location, and network name. It loads the first scattering coefficient
         file from the file list and prints the shape of the first-order and second-order scattering coefficient arrays.

        It calculates the number of channels, first-order scattering vector size, and second-order scattering vector
        size based on the shape of the scattering coefficient arrays.

        It creates a list of scattering vectors by iterating over the indices of `df_preds` and calling the
        `retreive_scat_vector` method with the scattering coefficient vectorized data, the current index, the number of
        channels, first-order scattering vector size, and second-order scattering vector size.

        It creates a DataFrame `df_scat_vec` with columns 'scat_vec_first_order' and 'scat_vec_second_order', where the
        values are obtained from the scattering vector list by extracting the first-order and second-order scattering
        vectors respectively.

        Finally, it returns the `df_scat_vec` DataFrame.

        Parameters:
        - df_preds (pandas.DataFrame): The DataFrame containing predictions.

        Returns:
        - df_scat_vec (pandas.DataFrame): The DataFrame with columns 'scat_vec_first_order' and 'scat_vec_second_order'.
        """
        self.load_scat_coef_vectorized()
        file_list = glob(
            f'{self.data_savepath}scatterings/{self.data_network}_{self.data_station}_{self.data_location}_'
            f'{self.network_name}_scatterings_*.npz')
        scat_file = np.load(file_list[0])
        print(f"First order: {scat_file['scat_coef_0'].shape[1:]}")
        print(f"Second order: {scat_file['scat_coef_1'].shape[1:]}")

        num_channels = scat_file['scat_coef_0'].shape[1:][0]
        first_order = scat_file['scat_coef_0'].shape[1:][1]
        second_order = scat_file['scat_coef_1'].shape[1:][1:]

        scat_vec_list = [
            self.retreive_scat_vector(self.scat_coef_vectorized, i, num_channels, first_order, second_order)
            for i in df_preds.index
        ]

        df_scat_vec = pd.DataFrame({
            'scat_vec_first_order': [sv[0] for sv in scat_vec_list],
            'scat_vec_second_order': [sv[1] for sv in scat_vec_list]
        })
        return df_scat_vec

    def waveforms_envelopes_scat_coefficients_df_merge(
        self,
        df_preds,
        df_scat_vec,
    ):
        """
        Merge the DataFrames `df_preds` and `df_scat_vec` along the columns axis.

        Parameters:
        - df_preds (pandas.DataFrame): The DataFrame containing predictions.
        - df_scat_vec (pandas.DataFrame): The DataFrame containing scattering coefficients.

        Returns:
        - merged_df (pandas.DataFrame): The merged DataFrame with columns from `df_preds` and `df_scat_vec`.
        """
        return pd.concat([df_preds, df_scat_vec], axis=1)

    def plot_waveforms_envelopes_scat_coefficients(self,
                                                   df_pred_scat_vec: pd.DataFrame,
                                                   channel: str = 'HHZ',
                                                   num_waveforms: int = 5,
                                                   num_scat_coeff_stacking: int = 10,
                                                   GPU: bool = is_gpu_available()):
        """
        Plot waveforms, envelopes, and scattering coefficients for different clusters.

        Parameters:
        - df_pred_scat_vec (pandas.DataFrame): DataFrame with predictions and scattering coefficients.
        - channel (str): The channel to plot waveforms for (default is 'HHZ').
        - num_waveforms (int): Number of waveforms to plot (default is 5).
        - num_scat_coeff_stacking (int): Number of scattering coefficients to stack (default is 10).
        - GPU (bool): Flag indicating if GPU is used for processing (default is determined by `is_gpu_available()`).

        Returns:
        None
        """
        if GPU:
            self.net.banks[0].centers = self.net.banks[0].centers.get()
            self.net.banks[1].centers = self.net.banks[2].centers.get()

        _, ax = plt.subplots(len(set(df_pred_scat_vec.predictions)), 4, figsize=(20, 10), sharex='col', sharey='col')

        sv1_mean = np.mean(np.array([sv1[2, :] for sv1 in df_pred_scat_vec.scat_vec_first_order]), axis=0)
        sv2_mean = np.mean(np.array([sv2[2, :, :] for sv2 in df_pred_scat_vec.scat_vec_second_order]), axis=0)

        ax[0, 0].set_title('Waveforms')
        ax[0, 0].margins(x=0)
        ax[len(set(df_pred_scat_vec.predictions)) - 1, 0].set_xlabel(f'Time samples ({self.network_segment}s)')

        ax[0, 1].set_title('Envelopes')
        ax[0, 1].margins(x=0)
        ax[len(set(df_pred_scat_vec.predictions)) - 1, 1].set_xlabel(f'Time samples ({self.network_segment}s)')

        ax[0, 2].set_title('First Order Scat. Coeff.')
        # ax[0,2].set_xscale('log')
        # ax[0,2].set_yscale('log')
        ax[len(set(df_pred_scat_vec.predictions)) - 1, 2].set_xlabel('First-order frequency (Hz)')
        ax[len(set(df_pred_scat_vec.predictions)) - 1, 2].set_xticks(range(0, sv1_mean.shape[0]))
        first_order_scat = [f'{x:.1f}' for x in reversed(self.net.banks[0].centers)]
        ax[len(set(df_pred_scat_vec.predictions)) - 1, 2].set_xticklabels(labels=first_order_scat, rotation='vertical')

        ax[0, 3].set_title('Second Order Scat. Coeff.')
        # ax[0,3].set_xscale('log')
        # ax[0,3].set_yscale('log')
        ax[len(set(df_pred_scat_vec.predictions)) - 1, 3].set_xlabel('First-order frequency (Hz)')
        ax[len(set(df_pred_scat_vec.predictions)) - 1, 3].set_xticks(range(0, sv1_mean.shape[0]))
        ax[len(set(df_pred_scat_vec.predictions)) - 1, 3].set_xticklabels(labels=first_order_scat, rotation='vertical')
        ax[len(set(df_pred_scat_vec.predictions)) - 1, 3].set_yticks(range(0, sv2_mean.shape[1]))
        second_order_scat = [f'{x:.1f}' for x in self.net.banks[1].centers]
        ax[len(set(df_pred_scat_vec.predictions)) - 1, 3].set_yticklabels(labels=second_order_scat)

        for row in range(len(set(df_pred_scat_vec.predictions))):
            ax[row, 2].set_ylabel('First-order scat. coef.')
            ax[row, 3].set_ylabel('Second-order freq. (Hz)')

        num_clusters = list(set(df_pred_scat_vec.predictions))
        for cluster_enum, cluster in enumerate(num_clusters):

            ax[cluster_enum, 0].set_ylabel(f'Cluster {cluster}')

            wvf0_time = str(df_pred_scat_vec.loc[(df_pred_scat_vec.predictions == cluster) &
                                                 (df_pred_scat_vec.cluster_rank == 0), 'times_YYYYMMDD'].values[0])
            wvf0 = self.get_waveform(start_time=str(wvf0_time),
                                     time_second=self.network_segment,
                                     channel=channel,
                                     envelope=False)
            if len(wvf0) < 1:
                print(f'  The waveform in the centre of Cluster {cluster} contains no traces. This \n' +
                      '  is most likely a cluster of damaged/missing data.')
            else:
                df_scat_vec = df_pred_scat_vec.loc[
                    (df_pred_scat_vec.predictions == cluster),
                ].sort_values(by='cluster_rank').reset_index()

                # WAVEFORMS

                ax[cluster_enum, 0].plot(self.min_max_vector(wvf0[0].data) - 0.5, 'k', alpha=0.5)
                wvfs = [
                    self.get_waveform(start_time=str(st).replace(' ', 'T'),
                                      time_second=self.network_segment,
                                      channel=channel,
                                      envelope=False)[0].data for st in df_scat_vec['times_YYYYMMDD'][1:num_waveforms]
                ]
                for wvf_enum, wvf in enumerate(wvfs):
                    ax[cluster_enum, 0].plot(self.min_max_vector(wvf) + wvf_enum + 1 - 0.5, 'b', alpha=0.2)

                # ENVELOPES
                env0 = self.get_waveform(start_time=str(wvf0_time),
                                         time_second=self.network_segment,
                                         channel=channel,
                                         envelope=True)
                ax[cluster_enum, 1].plot(self.min_max_vector(env0[0].data), 'k', alpha=0.5)
                envs = [
                    self.get_waveform(start_time=str(st).replace(' ', 'T'),
                                      time_second=self.network_segment,
                                      channel=channel,
                                      envelope=True)[0].data for st in df_scat_vec['times_YYYYMMDD'][1:num_waveforms]
                ]
                for env_enum, env in enumerate(envs):
                    ax[cluster_enum, 1].plot(self.min_max_vector(env) + env_enum + 1, 'b', alpha=0.2)

                # First Order Scat Coeffs
                sv1_array = np.array([sv1[2, :] for sv1 in df_scat_vec.scat_vec_first_order[:num_scat_coeff_stacking]])
                sv1_array = sv1_array - sv1_mean
                for sv1_row in range(sv1_array.shape[0]):
                    ax[cluster_enum, 2].plot(sv1_array[sv1_row, :], 'b', alpha=0.02)
                ax[cluster_enum, 2].plot(np.mean(sv1_array, axis=0), 'k', alpha=0.5)

                # Second Order Scat Coeffs
                sv2_array = np.array(
                    [sv2[2, :, :] for sv2 in df_scat_vec.scat_vec_second_order[:num_scat_coeff_stacking]])
                sv2_array = sv2_array - sv2_mean
                sv2_array = np.mean(sv2_array, axis=0).T
                sv2_array = np.flip(sv2_array, 0)
                print(f'MIN {sv2_array.min()} - MAX {sv2_array.max()}')
                im = ax[cluster_enum, 3].imshow(sv2_array, aspect='auto', cmap='RdYlBu')
                plt.colorbar(im, ax=ax[cluster_enum, 3])

        filename = (f'{self.data_network}_{self.data_station}_{self.data_location}_{self.network_name}_ICA_'
                    f'{self.ica.n_components}_Clustering_{len(num_clusters)}_Xcorr_ScatCoeff')
        plt.suptitle(filename)
        plt.savefig(f'{self.data_savepath}figures/{filename}.png', bbox_inches='tight')
        plt.show()
