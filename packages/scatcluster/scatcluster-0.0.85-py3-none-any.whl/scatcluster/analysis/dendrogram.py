"""Dendrogram analysis module."""
import os
from string import ascii_lowercase as letters
from typing import Union

import numpy as np
import obspy
import pandas as pd
from dateutil import tz
from fastcluster import linkage_vector
from matplotlib import dates as mdates
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from scipy.cluster import hierarchy
from scipy.spatial.distance import euclidean

from scatcluster.helper import COLORS


def get_leaves(dendrogram_info, ax):
    """
    Get dendrogram list of leaves coordinates and colors.

    Parameters
    ----------
    dendrogram_info : dict
        Output of the scipy.hierarchy.dendrogram function.
    ax : plt.Axes
        The axes to draw the dendrogram into.

    Returns
    -------
    leaves_coordinates: array-like
        The x coordinates of each leave.
    leaves_population_size: array-like
        The population size of each leave.
    """
    # Extract coordinates of each leave (with a depth coordinate indexed 0)
    infos = (key for key in dendrogram_info)
    node_index, node_depth, *_ = (dendrogram_info[key] for key in infos)
    leaves_coordinates = []
    for index, depth in zip(node_index, node_depth):
        if depth[0] == 0:
            leaves_coordinates.append(index[0])
        if depth[-1] == 0:
            leaves_coordinates.append(index[-1])
    leaves_coordinates = sorted(set(leaves_coordinates))

    # Cardinality
    leaves_population_size = []
    for label in ax.get_yticklabels():
        label = label.get_text()
        if '(' in label:
            label = label.replace('(', '').replace(')', '')
            population_size = int(label)
        else:
            population_size = 1
        leaves_population_size.append(population_size)
    return leaves_coordinates, leaves_population_size


def get_prediction(linkage, population_size):
    """
    Get cluster predection for each sample.

    The dendrogram (or linkage) matrix sorts the samples per catergory.
    We revert that back to their correct time coordinate.
    Note: the clusters are labeled from 1 to n_clusters.

    Parameters
    ----------
    linkage : np.ndarray
        Output of the linkage function.
    population_size : list
        The size of every cluster
    """
    # This is getting all leaves = every samples
    sample_indexes = hierarchy.leaves_list(linkage)
    predictions = np.zeros_like(sample_indexes)

    # Loop over every cluster (population)
    start = 0
    for index, size in enumerate(population_size):
        predictions[sample_indexes[start:start + size]] = index + 1
        start += size

    return predictions


def show_dendrogram(linkage, ax=None, depth=30):
    """
    Generate a dendrogram plot and return the cluster predictions.

    Parameters:
        linkage (np.ndarray): The linkage matrix.
        ax (matplotlib.axes.Axes, optional): The axes to plot the dendrogram on. Defaults to None.
        depth (int, optional): The depth of the dendrogram. Defaults to 30.

    Returns:
        np.ndarray: The cluster predictions for each sample.
    """
    # Generate axes
    ax = ax or plt.gca()

    # Show and get dendrogram
    with plt.rc_context({'lines.linewidth': 0.7}):

        dendrogram_infos = hierarchy.dendrogram(
            linkage,
            p=depth,
            truncate_mode='lastp',
            color_threshold=0,
            ax=ax,
            orientation='left',
            above_threshold_color='0.3',
            count_sort=True,
            labels=None,
        )

    # Extract information
    coordinates, population_sizes = get_leaves(dendrogram_infos, ax)

    predictions = get_prediction(linkage, population_sizes)

    # Plot leave nodes
    node_style = {'ms': 5, 'mec': '0.3', 'mew': 0.7, 'clip_on': False}
    for coordinate, color, pop in zip(coordinates, COLORS, population_sizes):
        ax.plot(0, coordinate, 'o', mfc=color, **node_style)
        index = int((coordinate - 5) / 10) + 1
        label = f'{index:d}\n{pop}\n{int(round((pop / sum(population_sizes)) * 100, 0))}%'
        ax.text(0.1, coordinate, label, color=color, va='center')

    return predictions


def dendrogram(linkage, times, n_clusters, n_cal_bins=150):
    """
    Generates a dendrogram plot and visualizes cluster properties for a given linkage matrix and times.

    Parameters:
        linkage (numpy.ndarray): The linkage matrix representing the hierarchical clustering.
        times (numpy.ndarray): The array of times associated with each data point.
        n_clusters (int): The number of clusters to show in the dendrogram.
        n_cal_bins (int, optional): The number of calendar bins to use for calendar occurrences. Defaults to 150.

    Returns:
        tuple: A tuple containing the figure object and the predictions made by the dendrogram.
    """

    # Deactivate axes basic properties
    spines_off = {
        'axes.spines.right': False,
        'axes.spines.left': False,
        'axes.spines.top': False,
        'axes.facecolor': 'none',
        'xtick.top': False,
        'ytick.left': False,
    }

    # Generate axes
    gs = {'width_ratios': [2, 4, 1, 2]}
    figsize = 6, n_clusters * 0.35
    with plt.rc_context(spines_off):
        figure_kwargs = {'sharey': True, 'figsize': figsize, 'gridspec_kw': gs}
        figure, axes = plt.subplots(1, 4, **figure_kwargs)

    # Calendar bins
    cal = pd.date_range(times[0], times[-1], n_cal_bins)

    # Show dendrogram
    predictions = show_dendrogram(linkage, ax=axes[0], depth=n_clusters)
    classes = sorted(set(predictions))

    # Show other cluster properties
    for cluster, color in zip(classes, COLORS):

        # Cluster coordinates
        y0 = (cluster - 1) * 10 + 5
        indexes = predictions == cluster

        # Population size
        size = np.sum(predictions == cluster)
        ratio = 100 * size / len(times)

        # Calendar occurrences
        rate, _ = np.histogram(times[indexes], cal)
        rate = 5 * rate / rate.max()
        rate += y0
        axes[1].step(cal[:-1], rate, 'k', lw=0.5, where='post')
        axes[1].fill_between(cal[:-1], y0, rate, step='post', lw=0, color=color)

        # Hourly occurrences
        hours = times[indexes].hour
        hours_counts, _ = np.histogram(hours, np.arange(25))
        hours_counts = 5 * hours_counts / hours_counts.max()
        hours_counts += y0
        axes[2].step(np.arange(24), hours_counts, 'k', lw=0.5, where='post')
        axes[2].fill_between(np.arange(24), y0, hours_counts, lw=0, step='post', color=color)

        # Population graph
        bar_style = {'height': 3, 'color': color, 'ec': 'k', 'lw': 0.5, 'align': 'edge'}
        text_style = {'va': 'center', 'color': color, 'size': 'small'}
        text_label = f' {size}'
        axes[-1].barh(y0, ratio, **bar_style)
        axes[-1].text(ratio, y0 + 1.8, text_label, **text_style)

    # Labels dendrogram
    axes[0].set_xlabel('Distance', loc='left')
    axes[0].set_yticklabels([])
    axes[0].yaxis.set_label_position('right')

    # Labels population
    axes[-1].set_yticks(10 * np.arange(len(classes)) + 5)
    axes[-1].set_xlabel('Relative\npopulation size (%)', loc='left')

    # # Labels calendar
    axes[1].set_yticks(10 * np.arange(len(classes)) + 5)
    axes[1].set_xlabel('Calendar date', loc='left')
    dateticks = mdates.AutoDateLocator()
    datelabels = mdates.ConciseDateFormatter(dateticks, show_offset=False)
    axes[1].xaxis.set_major_locator(dateticks)
    axes[1].xaxis.set_major_formatter(datelabels)
    plt.setp(axes[1].get_xticklabels(), rotation='vertical')

    # Labels hourly
    hours_ticks = range(0, 25, 12)
    hours_labels = [f'{h:0d}' for h in hours_ticks]
    axes[2].set_xlim(0, 24)
    axes[2].set_xlabel('Local\ntime (hours)', loc='left')
    axes[2].set_xticks(hours_ticks)
    axes[2].set_xticklabels(hours_labels)

    # All-axes cosmetics
    for ax, letter in zip(axes, letters):
        ax.grid(clip_on=False)
        ax.set_title(letter, loc='left', weight='bold')

    return figure, predictions


class Dendrogram:

    def process_dendrogram_linkage(self, **kwargs) -> None:
        """Process the full linkage for the Dendrogram. This is managed via dendrogram_method.
        Any additional parameters apart from 'method' can be supplied via kwargs
        """
        linkage = linkage_vector(self.ica_features, self.dendrogram_method, **kwargs)
        np.save(
            f'{self.data_savepath}clustering/{self.data_network}_{self.data_station}_{self.data_location}_'
            f'{self.network_name}_ICA_{self.ica_number_components}_linkage.npy', linkage)

        self.dendrogram_linkage = linkage

    def preload_linkage(self) -> None:
        """
        Load the linkage for the Dendrogram.

        This function loads the linkage for the Dendrogram from a file. The file path is constructed using the
        attributes `data_network`, `data_station`, `data_location`, `network_name`, and `ica_number_components` of
        the instance. The file path is constructed using the `data_savepath` attribute of the instance.

        """
        print(f'Loading linkage for {self.data_network}_{self.data_station}_{self.data_location}_'
              f'{self.network_name}_ICA_{self.ica_number_components}_linkage.npy')
        linkage = np.load(
            f'{self.data_savepath}clustering/{self.data_network}_{self.data_station}_{self.data_location}_'
            f'{self.network_name}_ICA_{self.ica_number_components}_linkage.npy')
        self.dendrogram_linkage = linkage

    def single_dendrogram(self, n_clusters: int, print_predictions: bool = True) -> Union[np.ndarray, None]:
        """
        Visualise a single Dendrogram based on n_cluster

        Args:
            n_clusters (int): The number of clusters to be identifed
            print_predictions (bool, optional): Whether to print the predictions. Defaults to True.

        Returns:
            np.ndarray: An array with cluster defintion of all the data
        """

        # Plot hierarchical waveforms
        plt.close('all')

        # Temporal vectors for histogram in time (calendar and hourly)
        timestamps = self.data_times.copy()  # mdates.date2num(times)
        if self.dendrogram_time_zone is not None:
            timestamps = np.array([
                mdates.date2num(mdates.num2date(d).astimezone(tz.gettz(self.dendrogram_time_zone)))
                for d in self.data_times
            ])
        calendar_bins = 150
        calendar_margin = 0.1 * (timestamps[-1] - timestamps[0])
        calendar_start, calendar_end = timestamps[0] - calendar_margin, timestamps[-1] + calendar_margin
        calendar_times = np.linspace(calendar_start, calendar_end, calendar_bins)

        calendar_time_step = calendar_times[1] - calendar_times[0]
        hourly = np.arange(24)

        # Figure generation settings
        spines_off = {
            'axes.spines.right': False,
            'axes.spines.left': False,
            'axes.spines.top': False,
            'axes.facecolor': 'none',
            'xtick.top': False,
            'ytick.left': False,
        }
        gs = {'width_ratios': [2, 4, 1, 2]}
        figsize = 10, n_clusters * 0.7
        with plt.rc_context(spines_off):
            figure_kwargs = {'sharey': True, 'figsize': figsize, 'gridspec_kw': gs}
            _, axes = plt.subplots(1, 4, **figure_kwargs)

        # Axes unpack
        ax_dendrogram, ax_cal, ax_hourly, ax_population = axes

        # Show dendrogram
        predictions = show_dendrogram(self.dendrogram_linkage, ax=ax_dendrogram, depth=n_clusters)
        classes = sorted(set(predictions))
        # _, counts = np.unique(predictions, return_counts=True)

        # Show other cluster properties
        for cluster, color in zip(classes, COLORS):

            # Cluster coordinates (scipy-enforced)
            yshift = (cluster - 1) * 10 + 5

            # Population size
            size = np.sum(predictions == cluster)
            ratio = 100 * size / len(self.data_times)

            # Get samples for which the class is the current one in the loop
            within_cluster = predictions == cluster
            cluster_times = self.data_times[within_cluster]
            cluster_timestamps = timestamps[within_cluster]
            cluster_hours = np.round((cluster_times - np.fix(cluster_times)) * 24)

            # Calendar occurences
            cal_counts, _ = np.histogram(cluster_timestamps, calendar_times)
            cal_counts = cal_counts / cal_counts.max()

            # Hourly occurrences
            hourly_counts = np.sum(cluster_hours == hourly[:, None], axis=1)
            hourly_counts = hourly_counts / hourly_counts.max()

            # Population graph
            bar_style = {'height': 3, 'color': color, 'ec': '0.3', 'lw': 0.5, 'align': 'edge'}
            text_style = {'size': 6, 'va': 'center', 'color': color}
            text_label = f' {size}'
            ax_population.barh(yshift, ratio, **bar_style)
            ax_population.text(ratio, yshift + 1.5, text_label, **text_style)

            # Calendar graph
            bar_style = {'bottom': yshift, 'width': calendar_time_step, 'fc': color, 'align': 'edge'}
            step_style = {'c': '0.3', 'lw': 0.5, 'where': 'post'}
            ax_cal.bar(calendar_times[:-1], cal_counts * 5, **bar_style)
            ax_cal.step(calendar_times[:-1], cal_counts * 5 + yshift, **step_style)

            # Hourly graph
            bar_style = {'bottom': yshift, 'width': 1, 'fc': color, 'align': 'edge'}
            step_style = {'c': '0.3', 'lw': 0.5, 'where': 'post'}
            ax_hourly.bar(hourly, hourly_counts * 5, **bar_style)
            ax_hourly.step(hourly, hourly_counts * 5 + yshift, **step_style)

        # Labels dendrogram
        ax_dendrogram.set_xlabel('Rescaled distance')
        ax_dendrogram.set_yticklabels([])
        ax_dendrogram.yaxis.set_label_position('right')

        # Labels population
        ax_population.set_yticks(10 * np.arange(len(classes)) + 5)
        ax_population.set_xlabel('Relative\npopulation size (%)')

        # Labels calendar
        ax_cal.set_yticks(10 * np.arange(len(classes)) + 5)
        ax_cal.set_xlabel('Calendar date')
        dateticks = mdates.AutoDateLocator()
        datelabels = mdates.ConciseDateFormatter(dateticks, show_offset=False)
        ax_cal.xaxis.set_major_locator(dateticks)
        ax_cal.xaxis.set_major_formatter(datelabels)
        ax_cal.set_xlim(calendar_start, calendar_end)
        plt.setp(ax_cal.get_xticklabels(), rotation='vertical')

        # Labels hourly
        hours_ticks = range(0, 25, 12)
        hours_labels = [f'{h:02d}' for h in hours_ticks]
        ax_hourly.set_xlim(0, 24)
        if self.dendrogram_time_zone is None:
            ax_hourly.set_xlabel('UTC time\n(hours)')
        else:
            ax_hourly.set_xlabel(f'{self.dendrogram_time_zone} time\n(hours)')
        ax_hourly.set_xticks(hours_ticks)
        ax_hourly.set_xticklabels(hours_labels)

        # All-axes cosmetics
        for ax, _ in zip(axes, letters):
            ax.grid(clip_on=False)
            # ax.set_title(letter)

        plt.suptitle(f'{self.data_network}_{self.data_station}_{self.data_location}_{self.network_name}_ICA_'
                     f'{self.ica.n_components}_dendrogram_clusters_{n_clusters}')

        plt.savefig(f'{self.data_savepath}figures/{self.data_network}_{self.data_station}_{self.data_location}_'
                    f'{self.network_name}_ICA_{self.ica.n_components}_dendrogram_clusters_{n_clusters}.png')

        plt.show()

        # Save predictions
        np.savez(
            f'{self.data_savepath}clustering/{self.data_network}_{self.data_station}_{self.data_location}_'
            f'{self.network_name}_ICA_{self.ica.n_components}_clusters_{n_clusters}.npz',
            predictions=predictions,
            times=timestamps)
        if print_predictions:
            return predictions

    def range_dendrograms(self, dendrogram_start: int = 4, dendrogram_end: int = 20) -> None:
        """Visualise a range of Dendrograms based on dendrogram_start and dendrogram_end

        Args:
            dendrogram_start (int, optional): Defaults to 4.
            dendrogram_end (int, optional): Defaults to 20.
        """
        for n_cluster in range(dendrogram_start, dendrogram_end + 1):
            _ = self.single_dendrogram(n_cluster)

    def preload_dendrogram_linkage(self, n_clusters: int) -> None:
        """Preload Dendrogram linkage based on n_clusters.

        Args:
            n_clusters (int): Number of clusters
        """
        clusters_path = (f'{self.data_savepath}clustering/{self.data_network}_{self.data_station}_{self.data_location}_'
                         f'{self.network_name}_ICA_{self.ica.n_components}_clusters_{n_clusters}.npz')
        if not os.path.exists(clusters_path):
            raise ValueError(
                f'Clusters of size {n_clusters} does not exist. Kindly choose another n_clusters or compute using '
                f'"single_dendrogram"')

        dendrogram_linkage_path = (f'{self.data_savepath}clustering/{self.data_network}_{self.data_station}_'
                                   f'{self.data_location}_{self.network_name}_ICA_{self.ica_number_components}_'
                                   f'linkage.npy')
        if not os.path.exists(dendrogram_linkage_path):
            raise ValueError('Dendrogram linkage does not exist. Kindly compute using "process_dendrogram_linkage"')

        p = np.load(clusters_path)
        self.dendrogram_predictions = p['predictions']
        self.dendrogram_timestamps = p['times']
        self.dendrogram_linkage = np.load(dendrogram_linkage_path)

    def _set_share_axes(self, axs, target=None, sharex=False, sharey=False) -> None:
        """
        Sets the axes sharing properties for a given set of axes.

        Parameters:
            axs (numpy.ndarray): The array of axes to set the sharing properties for.
            target (matplotlib.axes.Axes, optional): The target axes to share with. If not provided, the first axes
                in the array will be used.
            sharex (bool, optional): Whether to share the x-axis between the axes. Defaults to False.
            sharey (bool, optional): Whether to share the y-axis between the axes. Defaults to False.

        """
        if target is None:
            target = axs.flat[0]
        # Manage share using grouper objects
        for ax in axs.flat:
            if sharex:
                # pylint: disable-next=protected-access
                target._shared_axes['x'].join(target, ax)
            if sharey:
                # pylint: disable-next=protected-access
                target._shared_axes['y'].join(target, ax)
        # Turn off x tick labels and offset text for all but the bottom row
        if sharex and axs.ndim > 1:
            for ax in axs[:-1, :].flat:
                ax.xaxis.set_tick_params(which='both', labelbottom=False, labeltop=False)
                ax.xaxis.offsetText.set_visible(False)
        # Turn off y tick labels and offset text for all but the left most column
        if sharey and axs.ndim > 1:
            for ax in axs[:, 1:].flat:
                ax.yaxis.set_tick_params(which='both', labelleft=False, labelright=False)
                ax.yaxis.offsetText.set_visible(False)

    def show_dendrogram_waveforms(self, linkage: np.array, ax: Axes, depth: int = 30):
        """
        Generate a dendrogram plot of waveforms and return the leaf node coordinates and population labels.

        Parameters:
            linkage (np.array): The linkage matrix.
            ax (matplotlib.axes.Axes): The axes to plot the dendrogram on.
            depth (int, optional): The depth of the dendrogram. Defaults to 30.

        """
        # Show and get dendrogram
        with plt.rc_context({'lines.linewidth': 0.7}):
            dendrogram_infos = hierarchy.dendrogram(linkage,
                                                    p=depth,
                                                    truncate_mode='lastp',
                                                    color_threshold=0,
                                                    ax=ax,
                                                    orientation='left',
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
                orientation='left',
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
            ax.plot(0, coordinate, 'o', mfc=color, **node_style)
            index = int((coordinate - 5) / 10) + 1
            label = f'{index:d} {pop}'
            ax.text(-0.1, coordinate, label, color=color, va='center')

    def show_dendrogram_with_waveforms(self, n_clusters: int, experiment_name: str = ''):
        """
        Generates a dendrogram with waveforms for clustering analysis.

        Parameters:
            n_clusters (int): The number of clusters to generate.
            experiment_name (str, optional): The name of the experiment. Defaults to an empty string.

        """
        # Temporal vectors for histogram in time (calendar and hourly)
        timestamps = self.data_times.copy()  # mdates.date2num(times)
        if self.dendrogram_time_zone is not None:
            timestamps = np.array([
                mdates.date2num(mdates.num2date(d).astimezone(tz.gettz(self.dendrogram_time_zone)))
                for d in self.data_times
            ])
        calendar_bins = 150
        calendar_margin = 0.1 * (timestamps[-1] - timestamps[0])
        calendar_start, calendar_end = timestamps[0] - calendar_margin, timestamps[-1] + calendar_margin
        calendar_times = np.linspace(calendar_start, calendar_end, calendar_bins)

        calendar_time_step = calendar_times[1] - calendar_times[0]
        hourly = np.arange(24)

        # Figure generation settings
        spines_off = {
            'axes.spines.right': False,
            'axes.spines.left': False,
            'axes.spines.top': False,
            'axes.facecolor': 'none',
            'xtick.top': False,
            'ytick.left': False,
        }
        gs = {'width_ratios': [1, 4, 1, 5]}
        figsize = 15, n_clusters * 0.9
        with plt.rc_context(spines_off):
            figure_kwargs = {'sharey': True, 'figsize': figsize, 'gridspec_kw': gs}
            _, axes = plt.subplots(1, 4, **figure_kwargs)

        # Axes unpack
        ax_dendrogram, ax_cal, ax_hourly, ax_waveforms = axes

        # Show dendrogram
        predictions = show_dendrogram(self.dendrogram_linkage, ax=ax_dendrogram, depth=n_clusters)
        classes = sorted(set(predictions))
        # _, counts = np.unique(predictions, return_counts=True)

        self.preload_dendrogram_linkage(n_clusters)

        # Show other cluster properties
        for cluster, color in zip(classes, COLORS):

            # Cluster coordinates (scipy-enforced)
            yshift = (cluster - 1) * 10 + 5

            # Population
            # size = np.sum(predictions == cluster)

            # Get samples for which the class is the current one in the loop
            within_cluster = predictions == cluster
            cluster_times = self.data_times[within_cluster]
            cluster_timestamps = timestamps[within_cluster]
            cluster_hours = np.round((cluster_times - np.fix(cluster_times)) * 24)

            # Calendar occurences
            cal_counts, _ = np.histogram(cluster_timestamps, calendar_times)
            cal_counts = cal_counts / cal_counts.max()

            # Hourly occurrences
            hourly_counts = np.sum(cluster_hours == hourly[:, None], axis=1)
            hourly_counts = hourly_counts / hourly_counts.max()

            # Calendar graph
            bar_style = {'bottom': yshift, 'width': calendar_time_step, 'fc': color, 'align': 'edge'}
            step_style = {'c': '0.3', 'lw': 0.5, 'where': 'post'}
            ax_cal.bar(calendar_times[:-1], cal_counts * 5, **bar_style)
            ax_cal.step(calendar_times[:-1], cal_counts * 5 + yshift, **step_style)

            # Hourly graph
            bar_style = {'bottom': yshift, 'width': 1, 'fc': color, 'align': 'edge'}
            step_style = {'c': '0.3', 'lw': 0.5, 'where': 'post'}
            ax_hourly.bar(hourly, hourly_counts * 5, **bar_style)
            ax_hourly.step(hourly, hourly_counts * 5 + yshift, **step_style)

            # WAVEFORMS
            cluster_samples = self.ica_features[within_cluster]

            # Centroid
            centroid = np.median(cluster_samples, axis=0)
            distances = []
            for sample in cluster_samples:
                distances.append(euclidean(sample, centroid))
            distances = np.array(distances)

            # Extract the best waveforms timestamps
            _waveforms_n_samples = 5
            distances_argsort = np.argsort(distances)
            sorted_times = cluster_times[distances_argsort][:_waveforms_n_samples]
            sorted_times = mdates.num2date(sorted_times)
            for index, t in enumerate(sorted_times):
                start = obspy.UTCDateTime(t)
                end = start + self.network_segment
                stream = self.load_data(starttime=start, endtime=end, channel=self.data_channel)
                if len(stream) > 0:
                    trace = stream.select(component='Z')[0]
                    data = trace.data
                    data /= np.abs(data).max()
                    ax_waveforms.plot(trace.times(), data + index + yshift, color=color, linewidth=0.25)

        # Labels dendrogram
        ax_dendrogram.set_xlabel('Scaled\ndendrogram')
        ax_dendrogram.set_yticklabels([])
        ax_dendrogram.yaxis.set_label_position('right')

        # Labels Waveforms
        ax_waveforms.set_xlabel('Time (s)')

        # Labels calendar
        ax_cal.set_yticks(10 * np.arange(len(classes)) + 5)
        ax_cal.set_xlabel('Calendar date')
        dateticks = mdates.AutoDateLocator()
        datelabels = mdates.ConciseDateFormatter(dateticks, show_offset=False)
        ax_cal.xaxis.set_major_locator(dateticks)
        ax_cal.xaxis.set_major_formatter(datelabels)
        ax_cal.set_xlim(calendar_start, calendar_end)
        plt.setp(ax_cal.get_xticklabels(), rotation='vertical')

        # Labels hourly
        hours_ticks = range(0, 25, 12)
        hours_labels = [f'{h:02d}' for h in hours_ticks]
        ax_hourly.set_xlim(0, 24)
        if self.dendrogram_time_zone is None:
            ax_hourly.set_xlabel('UTC time\n(hours)')
        else:
            ax_hourly.set_xlabel(f'{self.dendrogram_time_zone} time\n(hours)')
        ax_hourly.set_xticks(hours_ticks)
        ax_hourly.set_xticklabels(hours_labels)

        # All-axes cosmetics
        for ax, letter in zip(axes, letters):
            ax.grid(clip_on=False)
            ax.set_title(letter)

        plt.suptitle(experiment_name)

        plt.savefig(
            f'{self.data_savepath}figures/02_dendrogram_{self.data_network}_{self.data_station}_{self.data_location}_'
            f'{self.network_name}_clusters_{n_clusters}_v2.png')

        plt.show()
