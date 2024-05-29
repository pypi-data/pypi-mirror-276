import os
import pickle

import cupy as cp
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xarray as xr
from matplotlib import dates as mdates
from obspy.clients.filesystem.sds import Client
from obspy.core import UTCDateTime
from obspy.core.stream import Stream
from scatseisnet.network import ScatteringNetwork
from scatseisnet.operation import segmentize
from scipy import stats as sp_stats
from tqdm import tqdm


class Scattering:

    def reduce_type(self):
        """
        Pooling operation performed on the last axis.
        """
        pooling_options = {
            'avg': np.mean,
            'max': np.max,
            'median': np.median,
            'std': np.std,
            'gmean': sp_stats.gmean,
            'hmean': sp_stats.hmean,
            'pmean': sp_stats.hmean,
            'kurtosis': sp_stats.kurtosis,
            'skew': sp_stats.skew,
            'entropy': sp_stats.entropy,
            'sem': sp_stats.sem,
            'differential_entropy': sp_stats.differential_entropy,
            'median_abs_deviation': sp_stats.median_abs_deviation,
        }
        return pooling_options.get(self.network_pooling, None)

    def load_data_times(self):
        """
        Load the data times from a file and store them in the `data_times` attribute.

        This function reads the data times from a file located at
        `{self.data_savepath}data/{self.data_network}_{self.data_station}_{self.data_location}_`
        `{self.network_name}_times.npy` and stores them in the `data_times` attribute.

        """
        try:
            file_path = f'{self.data_savepath}data/{self.data_network}_{self.data_station}_{self.data_location}_' \
                        f'{self.network_name}_times.npy'
            self.data_times = np.load(file_path)
        except FileNotFoundError:
            print(f'File not found: {file_path}')
        except Exception as e:
            print(f'An error occurred while loading data times: {e}')

    def build_day_list(self) -> None:
        """Build data_day_list object
        """
        try:
            start_time = UTCDateTime(self.data_starttime)
            end_time = UTCDateTime(self.data_endtime)
            exclude_days = [UTCDateTime(day).strftime('%Y-%m-%d') for day in self.data_exclude_days]
            day_list = [
                day_start for day_start in pd.date_range(start_time.strftime('%Y%m%d'), end_time.strftime(
                    '%Y%m%d')).strftime('%Y-%m-%d').tolist() if day_start not in exclude_days
            ]
            self.data_day_list = day_list
        except Exception as e:
            print(f'An error occurred while building day list: {e}')

    def build_channel_list(self) -> None:
        if self.sample_stream is None:
            self.process_sample_data()
        self.channel_list = [trace.stats.channel for trace in self.sample_stream]

    def stream_process(self, stream: Stream) -> Stream:
        """PreProcessing of obspy stream before calculating scattering coefficients

        Args:
            stream (Stream): Obspy Stream

        Returns:
            Stream: processed obspy Stream
        """
        # Remove trend
        stream.detrend(type='demean')
        # High-pass filter
        stream.filter(type='highpass', freq=0.5)
        # Remove residual trend
        stream.detrend(type='constant')
        # Remove edge effects
        stream.taper(0.05)
        return stream

    def load_data(self, starttime: UTCDateTime, endtime: UTCDateTime, channel: str) -> Stream:
        """Load the seismic and trim according to data_starttime and data_endtime

        Args:
            starttime (UTCDateTime): Start datetime of the trim
            endtime (UTCDateTime): End datetime of the trim
            channel (str): Channel selected

        Returns:
            Stream: Processed obspy stream
        """
        try:
            client = Client(self.data_client_path)
            stream = client.get_waveforms(network=self.data_network,
                                          station=self.data_station,
                                          location=self.data_location,
                                          channel=channel,
                                          starttime=starttime,
                                          endtime=endtime)

            stream = self.stream_process(stream)
            stream.merge(method=1, fill_value=0)
            stream.trim(starttime, endtime, pad=True, fill_value=0)
            return stream
        except Exception as e:
            print(f'>> Skipping {starttime}-{endtime} as there was an error in loading data from SDS Client due to {e}')
            return Stream()

    def network_build_scatcluster(self) -> None:
        """Build scatcluster network, assign to self.net and store as pickle
        """
        self.network_samples_per_segment = int(self.network_segment * self.network_sampling_rate)
        self.network_samples_per_step = int(self.network_step * self.network_sampling_rate)
        self.net = ScatteringNetwork(*self.network_banks,
                                     bins=self.network_samples_per_segment,
                                     sampling_rate=self.network_sampling_rate)

        # SAVE NETWORK IN PICKLE FILE
        with open(
                f'{self.data_savepath}networks/{self.data_network}_{self.data_station}_{self.data_location}_'
                f'{self.network_name}.pickle', 'wb') as handle:
            pickle.dump(self.net, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def plot_network_filter_banks(self, savefig: bool = True) -> None:
        """
        Plot the filter banks
        """
        NROWS = len(self.net.banks)
        # Crete axes
        octaves = [bank.octaves for bank in self.net.banks]
        height_ratios = 2, (octaves[1] + 2) / (octaves[0] + 2)
        grid = {'height_ratios': height_ratios, 'wspace': 0.1, 'hspace': 0.1}
        _, axes = plt.subplots(NROWS, 2, figsize=(10, 10), gridspec_kw=grid, sharey='row')
        # Loop over network layers
        for ax_enum, (ax, bank) in enumerate(zip(axes, self.net.banks)):
            # Limit view to three times the temporal width of largest wavelet
            width_max = min(2 * bank.widths.max(), bank.times.max())
            if isinstance(bank.wavelets, cp.ndarray):
                bank.wavelets = bank.wavelets.get()
            if isinstance(bank.spectra, cp.ndarray):
                bank.spectra = bank.spectra.get()
            if isinstance(bank.widths, cp.ndarray):
                bank.widths = bank.widths.get()
            if isinstance(bank.centers, cp.ndarray):
                bank.centers = bank.centers.get()
            if isinstance(bank.frequencies, cp.ndarray):
                bank.centers = bank.frequencies.get()

            # Temporal
            for octave_enum, (wavelet, octave, width) in enumerate(zip(bank.wavelets, bank.ratios, bank.widths)):
                # Truncate time for small-duration wavelets
                inner = np.abs(bank.times) < width_max
                t = bank.times[inner]
                y = wavelet[inner] / np.abs(wavelet[inner].max()) / 3
                ax[0].plot(t, y.real + octave, color='C0', zorder=1)
                ax[0].plot(t, y.imag + octave, color='C0', zorder=0, alpha=0.4)
                ax[0].text(-1 * width_max * (1 if octave_enum % 2 == 0 else 1.1),
                           octave,
                           f'{width*4:.2f}',
                           fontsize='small')

            # Spectral
            frequencies = bank.frequencies
            for octave_enum, (spectrum, octave, center) in enumerate(zip(bank.spectra, bank.ratios, bank.centers)):
                inner = frequencies > frequencies[1]
                f = frequencies[inner]
                y = spectrum[inner]
                y /= np.abs(y.max())
                ax[1].plot(f, np.abs(y) + octave, color='C0')
                ax[1].text((10**-2) * (1 if octave_enum % 2 == 0 else 1.1), octave, f'{center:.2f}', fontsize='small')

            # Labels
            ax[0].grid(axis='x')
            ax[0].set_xlabel('Time (seconds)')
            axes[ax_enum, 0].set_ylabel(f'Order {ax_enum+1}\nOctaves (base 2 log)')
            ax[1].grid(axis='x')
            ax[1].set_xlabel('Frequency (Hz)')
            ax[1].set_xscale('log')
            axes[ax_enum, 0].text(-1 * width_max, 0.2, 'Temporal\nWidth (s)', fontsize='small')
            axes[ax_enum, 1].text(10**-2, 0.2, 'Centre\nFreq. (Hz)', fontsize='small')

            # Axes
            ax[1].set_ylim(-bank.octaves - 1, 1)
            ax[0].set_yticks(-np.arange(bank.octaves + 1))
            ax[0].set_yticklabels(np.arange(bank.octaves + 1))
            ax[0].set_yticks(-np.arange(bank.octaves + 1))
            ax[0].set_yticklabels(np.arange(bank.octaves + 1))
            ax[1].tick_params(axis='y', left=False, labelleft=False)

        # Legend
        axes[1][0].legend([r'Re $\varphi(t)$', r'Im $\varphi(t)$'], loc=1)
        axes[1][1].legend([r'$\hat\varphi(\omega)$'], loc=1)

        plt.suptitle('ScatCluster Parametrization'
                     f'\nSegment:{self.network_segment}s  Step: {self.network_step}\n Banks: {self.network_banks_name}')
        plt.subplots_adjust(top=0.9)
        if savefig:
            plt.savefig(f'{self.data_savepath}figures/{self.data_network}_{self.data_station}_{self.data_location}_'
                        f'{self.network_name}_filter_banks.png')

    def load_sample_data(self) -> Stream:
        """Load sample
        """
        return self.load_data(starttime=UTCDateTime(self.data_sample_starttime),
                              endtime=UTCDateTime(self.data_sample_endtime),
                              channel=self.data_channel)

    def plot_sample_spectra(self) -> None:
        """Plot the Network filter spectra"""
        frequencies = self.net.banks[0].centers
        timestamps = pd.to_datetime(self.sample_times, unit='D')
        timestamps_scats = pd.to_datetime(self.sample_times_scatterings, unit='D')

        _, ax = plt.subplots(2, len(self.channel_list), sharex=True, sharey='row', figsize=(20, 5))

        for channel_num, _ in enumerate(self.channel_list):
            first_order_scattering_coefficients = self.sample_scattering_coefficients[0][:, channel_num, :].squeeze().T
            first_order_scattering_coefficients = np.real(np.log10(first_order_scattering_coefficients))

            ax[0, channel_num].plot(timestamps, self.sample_data[channel_num], rasterized=True)
            ax[0, channel_num].set_title(self.channel_list[channel_num])

            ax[1, channel_num].pcolormesh(timestamps_scats,
                                          frequencies,
                                          first_order_scattering_coefficients,
                                          rasterized=True)
            ax[1, channel_num].set_yscale('log')
            ax[1, channel_num].tick_params('x', labelrotation=90)

        ax[0, 0].set_ylabel('Sample Trace')
        ax[1, 0].set_ylabel('First Order Scat. Coefficients\nFrequency (Hz)')
        plt.subplots_adjust(wspace=0, hspace=0)

        plt.suptitle('Sample Trace ScatCluster Transform')
        plt.savefig(f'{self.data_savepath}figures/{self.data_network}_{self.data_station}_{self.data_location}_'
                    f'{self.network_name}_sample_transform.png')
        plt.show()

    def process_sample_data(self) -> None:
        """Process the sample data range. This involes:
        (1) load the data and process,
        (2) define the sample_times and sample_data,
        (3) segmentize into sample_data_segments and respective sample_times_scatterings,
        (4) transform into sample_scattering_coefficients,
        (5) plot filter spectra
        """
        self.sample_stream = self.load_sample_data()
        self.sample_times = self.sample_stream[0].times('matplotlib')
        self.sample_data = np.array([trace.data for trace in self.sample_stream])
        self.channel_list = [trace.stats.channel for trace in self.sample_stream]

        self.sample_data_segments = segmentize(self.sample_data, self.network_samples_per_segment,
                                               self.network_samples_per_step)
        self.sample_times_scatterings = segmentize(self.sample_times, self.network_samples_per_segment,
                                                   self.network_samples_per_step)[:, 0]
        self.sample_scattering_coefficients = self.net.transform(self.sample_data_segments, self.reduce_type())
        self.plot_sample_spectra()

    def plot_seismic(self, sample: bool = False):
        """
        Plot the seismic data.

        Parameters:
            sample (bool): If True, plot the sample data. Otherwise, plot the regular data.

        """
        if sample:
            if self.sample_data is None:
                self.sample_stream = self.load_sample_data()
                self.sample_times = self.sample_stream[0].times('matplotlib')
                self.sample_data = np.array([trace.data for trace in self.sample_stream])
                self.channel_list = [trace.stats.channel for trace in self.sample_stream]

            times = self.sample_times
            data = self.sample_data
            channel_list = self.channel_list
        else:
            if self.data_all is None:  # pylint: disable=access-member-before-definition
                self.data_stream = self.load_data(starttime=UTCDateTime(self.data_starttime),
                                                  endtime=UTCDateTime(self.data_endtime),
                                                  channel=self.data_channel)
                self.data_times = self.data_stream[0].times('matplotlib')
                self.data_all = np.array([trace.data for trace in self.data_stream])
                self.channel_list = [trace.stats.channel for trace in self.data_stream]
            times = self.data_times
            data = self.data_all
            channel_list = self.channel_list

        # Plot
        _, axes = plt.subplots(3, 1, figsize=(20, 10), sharex=True, sharey=True)
        for channel_enum, channel in enumerate(channel_list):
            axes[channel_enum].plot(times, data[channel_enum, :])
            axes[channel_enum].set_ylabel(f'{channel}')

        dateticks = mdates.AutoDateLocator()
        datelabels = mdates.ConciseDateFormatter(dateticks)
        axes[0].xaxis.set_major_locator(dateticks)
        axes[0].xaxis.set_major_formatter(datelabels)
        axes[0].set_xlim(times.min(), times.max())

    def process_scatcluster_yyyy_mm_dd(self, day_start: str, day_end: str) -> None:
        """Process scatcluster for a single day.

        Args:
            day_start (str): Start day of format "YYYY-MM-DD"
            day_end (str): End day of format "YYYY-MM-DD"
        """
        print(f'Processing {day_start} - {day_end}')
        scatterings_path = (f'{self.data_savepath}scatterings/{self.data_network}_{self.data_station}_'
                            f'{self.data_location}_{self.network_name}_scatterings_{day_start}.npz')
        if os.path.exists(scatterings_path):
            print('> Scatterings already exist')
        else:
            # Check if day_start exits is valid in data_day_start
            if day_start not in self.data_day_list:
                print(f'> Processing of {day_start} has been excluded as it is part of `data_exclude_days` parameter.')
            else:
                stream = self.load_data(starttime=UTCDateTime(day_start),
                                        endtime=UTCDateTime(day_end),
                                        channel=self.data_channel)
                if len(stream.traces) == 0:
                    print(f'>> Skipping {day_start} as there is no traces')
                elif len(stream.traces) < 3:
                    print(f'>> Skipping {day_start} as there is not all 3 channels')
                else:
                    # Numpyification
                    times = stream[0].times('matplotlib')
                    data = np.array([trace.data for trace in stream])

                    # Segmentization
                    data_segments = segmentize(data, self.network_samples_per_segment, self.network_samples_per_step)
                    times_scat = segmentize(times, self.network_samples_per_segment, self.network_samples_per_step)[:,
                                                                                                                    0]

                    # Scattering transform
                    scattering_coefficients = self.net.transform(data_segments, self.reduce_type())

                    # SAVE SCATTERING COEFFICIENTS IN NPZ FILE
                    np.savez(scatterings_path,
                             scat_coef_0=scattering_coefficients[0],
                             scat_coef_1=scattering_coefficients[1],
                             times=times_scat)

                    # print stats
                    print(f'>>> min {data.min()} : max {data.max()} : mean {data.mean()}')

    def process_scatcluster_for_range(self) -> None:
        """Process scatcluster_yyyy_mm_dd for range of YYYY-MM-DDs
        """
        self.build_day_list()
        if len(self.data_day_list) > 0:
            print(f'The following days will be excluded from the analysis: {self.data_exclude_days}')

        for day_start, day_end in zip(
                pd.date_range(
                    UTCDateTime(self.data_starttime).strftime('%Y%m%d'),
                    (UTCDateTime(self.data_endtime) - (60 * 60 * 24)).strftime('%Y%m%d')).strftime('%Y-%m-%d').tolist(),
                pd.date_range((UTCDateTime(self.data_starttime) + (60 * 60 * 24)).strftime('%Y%m%d'),
                              UTCDateTime(self.data_endtime).strftime('%Y%m%d')).strftime('%Y-%m-%d').tolist()):
            self.process_scatcluster_yyyy_mm_dd(day_start, day_end)

    def filters_per_layer(self, model):
        """Get the number of filters per layer."""
        center_frequencies = [bank.centers for bank in model.banks]
        return [len(centers) for centers in center_frequencies]

    def layer_shape(self, model, order):
        return self.filters_per_layer(model)[:order + 1]

    def log(self, dataset, waterlevel=1e-10):
        """Get the log of the scattering coefficients.

        Parameters
        ----------
        dataset : xarray.Dataset
            The scattering coefficients in the xarray.Dataset format.
        waterlevel : float
            The waterlevel to apply to the scattering coefficients.

        Returns
        -------
        xarray.Dataset
            The scattering coefficients in the xarray.Dataset format.
        """
        # Select where order 1 is non-zero for all channels and frequencies
        select = (dataset.order_1 > waterlevel).all(dim=['channel', 'f1'])
        dataset = dataset.sel(time=select)

        # Get the log
        dataset.order_1.values = np.log10(dataset.order_1.values + waterlevel)
        dataset.order_2.values = np.log10(dataset.order_2.values + waterlevel)

        return dataset

    def nyquist_mask(self, dataset):
        """Mask the scattering coefficients with a Nyquist frequency.

        The scattering coefficients of order 2 are masked when the frequency
        f2 is greater than the frequency f1 to avoid aliasing.

        Parameters
        ----------
        dataset : xarray.Dataset
            The scattering coefficients in the xarray.Dataset format.

        Returns
        -------
        xarray.Dataset
            The scattering coefficients in the xarray.Dataset format.
        """
        # Mask order 2 when f2 > f1
        dataset.order_2.data = dataset.order_2.where(dataset.f1 >= dataset.f2, np.nan)

        # Drop NaN values
        dataset = dataset.dropna(dim='time', how='all')

        return dataset

    def normalize(self, dataset):
        """Normalize the scattering coefficients.

        Parameters
        ----------
        dataset : xarray.Dataset
            The scattering coefficients in the xarray.Dataset format.

        Returns
        -------
        xarray.Dataset
            The scattering coefficients in the xarray.Dataset format.
        """
        # Working dimensions for normalization
        order_1_dim = ['time', 'f1', 'channel']
        order_2_dim = ['time', 'f1', 'f2', 'channel']

        # Normalize
        dataset.order_1.data -= dataset.order_1.mean(dim=order_1_dim).data
        dataset.order_1.data /= dataset.order_1.std(dim=order_1_dim).data
        dataset.order_2.data -= dataset.order_2.mean(dim=order_2_dim).data
        dataset.order_2.data /= dataset.order_2.std(dim=order_2_dim).data

        return dataset
    
    def min_max_scaling(self, dataset):
        """Min-Max scaling the scattering coefficients.

        Parameters
        ----------
        dataset : xarray.Dataset
            The scattering coefficients in the xarray.Dataset format.

        Returns
        -------
        xarray.Dataset
            The scattering coefficients in the xarray.Dataset format.
        """
        # Working dimensions for normalization
        order_1_dim = ['time', 'f1', 'channel']
        order_2_dim = ['time', 'f1', 'f2', 'channel']

        # Normalize
        dataset.order_1.data -= dataset.order_1.min(dim=order_1_dim).data
        dataset.order_1.data /= (dataset.order_1.max(dim=order_1_dim).data - dataset.order_1.min(dim=order_1_dim).data)
        dataset.order_2.data -= dataset.order_2.min(dim=order_2_dim).data
        dataset.order_2.data /= (dataset.order_2.max(dim=order_2_dim).data - dataset.order_2.min(dim=order_2_dim).data)

        return dataset

    def process_vectorized_scattering_coefficients(self) -> None:
        """
        Process the vectorized scattering coefficients by loading data from files, reshaping the coefficients,
        standardizing in log space, and vectorizing them. Display statistics from the vectorization and store the
        processed data.

        Parameters:
            self: An instance of the class.
        """
        file_list = [(f'{self.data_savepath}scatterings/{self.data_network}_{self.data_station}_{self.data_location}_'
                      f'{self.network_name}_scatterings_{day_start}.npz') for day_start in self.data_day_list]

        # LOAD DATA
        TIMES = []
        SC0 = []
        SC1 = []
        for file in file_list:
            try:
                scat_file = np.load(file)
                TIMES.append(scat_file['times'])
                SC0.append(scat_file['scat_coef_0'])
                SC1.append(scat_file['scat_coef_1'])
            except FileNotFoundError:
                print(f'{file} is missing. This has been skipped.')
        times = np.hstack(TIMES)
        del TIMES
        scat_coef_0 = np.vstack(SC0)
        del SC0
        scat_coef_1 = np.vstack(SC1)
        del SC1

        n_samples = len(times)
        if self.channel_list is None:
            self.build_channel_list()
        n_channels = len(self.channel_list)

        attributes = {k: str(v) for k, v in self.__dict__.items()}

        # The coordinates of the xarray dataset are the center frequencies of the
        # scattering network, the starttime of the waveforms, and the channel names.
        center_frequencies = [bank.centers for bank in self.net.banks]
        coordinates = {
            'time': ('time', times),
            'channel': ('channel', self.channel_list),
            **{
                f'f{i + 1}': (f'f{i + 1}', centers)
                for i, centers in enumerate(center_frequencies)
            },
        }
        # We now fill the data variables of the xarray dataset. The data variables
        # are the scattering coefficients for each order.
        variables = {}
        for order in range(len(self.net)):
            # Variable dimensions
            dimension = (
                'time',
                'channel',
                *[f'f{j + 1}' for j in range(order + 1)],
            )

            # Initialize and fill scattering matrix with scattering coefficients
            variable = np.zeros((n_samples, n_channels, *self.layer_shape(self.net, order)))

            for time_stamp in tqdm(range(n_samples), desc=f'Xarray order {order + 1}'):
                if order == 0:
                    x = np.abs(scat_coef_0[time_stamp])
                elif order == 1:
                    x = np.abs(scat_coef_1[time_stamp])
                for channel in range(n_channels):
                    variable[time_stamp, channel] = x[order][channel]

            # Assign scattering matrix to data variable
            variables[f'order_{order + 1}'] = (dimension, variable)

        # Assign attributes and data variables to dataset
        coefficients = xr.Dataset(
            coords=coordinates,
            data_vars=variables,
            attrs=attributes,
        )

        # Drop empty channels (where transform_waveform returned None)
        coefficients = coefficients.where(
            coefficients.order_1.sum(dim=('f1', 'channel')) > 0,
            drop=True,
        )
        coefficients = self.log(coefficients, waterlevel=1e-15)
        coefficients = self.nyquist_mask(coefficients)
        coefficients = self.normalize(coefficients)
        coefficients = self.min_max_scaling(coefficients)
        print(coefficients)

        self.data_times = coefficients.time.values
        self.data_scat_coef_vectorized = self.vectorize_scattering_coefficients_xarray(coefficients)

        # Display statistics from the vectorization
        print(f'Number of valid time windows of size {self.network_segment}s: {int(self.data_times.shape[0])}')
        print(f'Number of days investigated: {int((self.network_segment * self.data_times.shape[0])/86400)}')
        print(f'Number of Scat Coefficients: {int(self.data_scat_coef_vectorized.shape[1])}')
        print(f'Vectorized Scat Coefficients: {self.data_scat_coef_vectorized.shape}')

        # Store Data
        np.save(
            f'{self.data_savepath}data/{self.data_network}_{self.data_station}_{self.data_location}_'
            f'{self.network_name}_times.npy', self.data_times)
        np.save(
            f'{self.data_savepath}data/{self.data_network}_{self.data_station}_{self.data_location}_'
            f'{self.network_name}_scat_coef_vectorized.npy', self.data_scat_coef_vectorized)
        coefficients.to_netcdf(f'{self.data_savepath}data/{self.data_network}_{self.data_station}_{self.data_location}_'
                               f'{self.network_name}_scat_coef_xarray.nc')

        return coefficients

    def vectorize_scattering_coefficients_xarray(self, coefficients):
        n_samples = coefficients.time.shape[0]
        x1 = coefficients.order_1.data.reshape(n_samples, -1)
        x2 = coefficients.order_2.data.reshape(n_samples, -1)
        x = np.hstack((x1, x2))

        x[np.isnan(x)] = 0

        return x

    def load_scattering_coefficients_xarray(self):
        """
        Load the scattering coefficients from an xarray dataset file and store them in the
        `scattering_coefficients_xarray` attribute.

        Returns:
            xr.Dataset: The loaded scattering coefficients dataset.
        """
        scat_coeff_xr = xr.open_dataset(
            f'{self.data_savepath}data/{self.data_network}_{self.data_station}_{self.data_location}_'
            f'{self.network_name}_scat_coef_xarray.nc')
        self.scattering_coefficients_xarray = scat_coeff_xr
        return scat_coeff_xr

    def preload_times(self):
        """
        Preloads the times data from a numpy file and assigns it to the `data_times` attribute of the class.

        """
        data_times = np.load(f'{self.data_savepath}data/{self.data_network}_{self.data_station}_{self.data_location}_'
                             f'{self.network_name}_times.npy')
        self.data_times = data_times

    def load_scat_coef_vectorized(self):
        if not hasattr(self, 'scat_coef_vectorized'):
            self.scat_coef_vectorized = np.load(
                f'{self.data_savepath}data/{self.data_network}_{self.data_station}_{self.data_location}_'
                f'{self.network_name}_scat_coef_vectorized.npy')
        else:
            print('self.scat_coef_vectorized already exist')

        return self.scat_coef_vectorized
