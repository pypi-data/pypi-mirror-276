"""Processing analysis module."""
import os

import matplotlib.pyplot as plt
import numpy as np
import obspy
import obspy.signal.filter
from matplotlib import dates as mdates
from obspy import Stream
from tqdm import tqdm


class AnalysisProcessing:

    def process_stream_envelope(self, stream: Stream) -> Stream:
        st_env = stream.copy()
        for trace_enum, tr in enumerate(st_env):
            # pylint: disable-next=unnecessary-list-index-lookup
            st_env[trace_enum].data = obspy.signal.filter.envelope(tr.data)

        return st_env

    def process_stream_rms(self, stream: Stream) -> list:
        return [np.sqrt(np.mean(tr.data**2)) for tr in stream]

    def build_waveforms_data(self, include_envelopes=False, include_RMS=False, custom_title=''):
        """
        This function builds waveforms data based on specified parameters.

        Parameters:
            include_envelopes (bool): Flag to include envelopes in the data.
            include_RMS (bool): Flag to include RMS values in the data.
            custom_title (str): Custom title to append to the waveforms file.

        Returns:
            numpy.ndarray: Array containing the waveforms' data.
        """
        waveforms_file = (f'{self.data_savepath}data/{self.data_network}_{self.data_station}_{self.data_location}_'
                          f'{self.network_segment}_waveforms{custom_title}.npy')
        if os.path.exists(waveforms_file):
            print('Waveforms already calculated. Loading into self.waveforms')
            waveforms = self.load_waveforms(custom_title)
        else:
            self.load_data_times()
            start_times = [obspy.UTCDateTime(s_time) for s_time in mdates.num2date(self.data_times)]
            end_times = [e_time + self.network_segment for e_time in start_times]

            data_stream = []
            data_envelope = []
            data_rms = []

            for start, end in tqdm(zip(start_times, end_times)):
                ds = self.load_data(starttime=start, endtime=end, channel=self.data_channel)
                data_stream.append(ds)
                if include_envelopes:
                    data_envelope.append(self.process_stream_envelope(ds))
                if include_RMS:
                    data_rms.append(self.process_stream_rms(ds))
            waveforms = np.array(data_stream)
            np.save(waveforms_file, waveforms)

            if include_envelopes:
                np.save(
                    f'{self.data_savepath}data/{self.data_network}_{self.data_station}_{self.data_location}_'
                    f'{self.network_segment}_envelopes{custom_title}.npy', np.array(data_envelope))

            if include_RMS:
                np.save(
                    f'{self.data_savepath}data/{self.data_network}_{self.data_station}_{self.data_location}_'
                    f'{self.network_segment}_RMS{custom_title}.npy', np.array(data_rms))

        self.waveforms = waveforms
        return waveforms

    def load_waveforms(self, waveform_extra_title: str = ''):
        waveforms = np.load(
            f'{self.data_savepath}data/{self.data_network}_{self.data_station}_{self.data_location}_'
            f'{self.network_segment}_waveforms{waveform_extra_title}.npy',
            allow_pickle=True)
        self.waveforms = waveforms
        return waveforms

    def get_spectrogram_data(self, Zwaveform, samp_rate):
        if len(Zwaveform.traces) > 0:
            spec = Zwaveform.spectrogram(samp_rate=samp_rate, show=False)
            orig_data = spec[0].axes[0].images[0].get_array().data
            plt.close()
            return orig_data
        else:
            return ''

    def spectrogram_build(self, waveforms, samp_rate, extra_title=''):
        """
        Builds spectrograms based on the provided waveforms and sample rate.
        Saves the spectrograms to a file if they don't already exist.
        Updates the class attribute 'spectrograms' with the generated spectrograms.

        Parameters:
            waveforms (list): List of waveforms for spectrogram generation.
            samp_rate (int): Sampling rate for spectrogram generation.
            extra_title (str): Additional title for the spectrogram file (default '').

        Returns:
            numpy.ndarray: Array containing the generated spectrograms.
        """
        spectrum_file = (f'{self.data_savepath}data/{self.data_network}_{self.data_station}_{self.data_location}_'
                         f'{self.network_segment}_spectrograms{extra_title}.npy')
        if os.path.exists(spectrum_file):
            print(f'>> Spectrum already exists for {spectrum_file}')
            spectrograms = self.load_spectrograms(extra_title)
        else:
            specgrams = []
            for _, waveform in tqdm(enumerate(waveforms)):
                specgrams.append(self.get_spectrogram_data(waveform.select(component='Z'), samp_rate))
            spectrograms = np.array(specgrams)
            np.save(spectrum_file, spectrograms)

        self.spectrograms = spectrograms

        return spectrograms

    def build_spectrum_data(
        self,
        waveform_extra_title: str = '',
        spectrum_extra_title: str = '',
        spectrum_samp_rate: int = 50,
    ):
        if self.waveforms is None:
            self.waveforms = self.load_waveforms(waveform_extra_title)
        self.spectrogram_build(waveforms=self.waveforms, samp_rate=spectrum_samp_rate, extra_title=spectrum_extra_title)

    def load_spectrograms(self, extra_title=''):
        spectrograms = np.load(
            f'{self.data_savepath}data/{self.data_network}_{self.data_station}_{self.data_location}_'
            f'{self.network_segment}_spectrograms{extra_title}.npy',
            allow_pickle=True)
        self.spectrograms = spectrograms

        return spectrograms
