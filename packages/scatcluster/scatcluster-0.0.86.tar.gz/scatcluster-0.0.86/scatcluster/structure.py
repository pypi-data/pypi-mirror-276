# scatcluster/structure.py
import json
import os
from glob import glob
from typing import List, Optional


class Structure:

    def prepare_directory_structure(self, directories: Optional[List[str]] = None) -> None:
        """Build directory structure required for workflow processing

        Args:
            directories (List[str], optional): Directories created as part of the workflow.
            Defaults to ['scatterings', 'figures', 'networks', 'ICA','clustering','data', 'config'].
        """
        if directories is None:
            directories = ['scatterings', 'figures', 'networks', 'ICA', 'clustering', 'data', 'config']

        if self.data_savepath == '':
            raise ValueError('"data_savepath" has not been set up correctly. Kindly update the parametrization.')

        if os.path.exists(self.data_savepath):
            print(f'Main directory {self.data_savepath} already exists. \n')
        else:
            os.mkdir(self.data_savepath)
            print(f'Main directory {self.data_savepath} created. \n')

        for path in directories:
            isExist = os.path.exists(f'{self.data_savepath}{path}')
            if not isExist:
                os.makedirs(f'{self.data_savepath}{path}')
                print(f'Directory {self.data_savepath}{path} created.')
            else:
                print(f'Directory {self.data_savepath}{path} already exists.')

    def delete_scatterings(self) -> None:
        """
        Deletes scatterings files based on specific naming conventions.
        """
        file_list_scatterings = glob(
            f'{self.data_savepath}scatterings/{self.data_network}_{self.data_station}_{self.data_location}_'
            f'{self.network_name}_scatterings_*.npz')
        for file in file_list_scatterings:
            os.remove(file)
        print(f'{len(file_list_scatterings)} scatterings have been deleted from "{self.data_savepath}scatterings/"\n')

    def config_store(self):
        """
        Stores the configuration of the current object as a JSON file.

        This function creates a dictionary `sc_config` containing the configuration parameters of the current object.
        The dictionary includes the following keys:
        - 'data_savepath': The path to the main directory where data is saved.
        - 'data_client_path': The path to the client data.
        - 'data_network': The network name.
        - 'data_station': The station name.
        - 'data_location': The location name.
        - 'data_channel': The channel name.
        - 'data_sample_starttime': The start time of the data sample.
        - 'data_sample_endtime': The end time of the data sample.
        - 'data_starttime': The start time of the data.
        - 'data_endtime': The end time of the data.
        - 'data_exclude_days': The excluded days for the data.
        - 'network_segment': The network segment.
        - 'network_step': The network step.
        - 'network_sampling_rate': The network sampling rate.
        - 'network_banks': The network banks.
        - 'network_pooling': The network pooling.
        - 'ica_ev_limit': The ICA event limit.
        - 'ica_min_ICAs': The minimum number of ICAs.
        - 'ica_max_ICAs': The maximum number of ICAs.
        - 'ica_overwrite_previous_models': Whether to overwrite previous models.
        - 'dendrogram_method': The method for generating the dendrogram.
        - 'waveforms_n_samples': The number of samples for waveforms.

        The function then constructs the path to the JSON file by combining the values of 'data_savepath',
        'data_network', 'data_station', 'data_location', and 'network_name'. The JSON file is opened in write mode with
        UTF-8 encoding. The `sc_config` dictionary is dumped into the JSON file using the `json.dump()` function.
        Finally, a message is printed indicating the location where the JSON file was stored.

        Parameters:
        - self: The current object.

        Returns:
        - None
        """
        sc_config = {
            'data_savepath': self.data_savepath,
            'data_client_path': self.data_client_path,
            'data_network': self.data_network,
            'data_station': self.data_station,
            'data_location': self.data_location,
            'data_channel': self.data_channel,
            'data_sample_starttime': self.data_sample_starttime,
            'data_sample_endtime': self.data_sample_endtime,
            'data_starttime': self.data_starttime,
            'data_endtime': self.data_endtime,
            'data_exclude_days': self.data_exclude_days,
            'network_segment': self.network_segment,
            'network_step': self.network_step,
            'network_sampling_rate': self.network_sampling_rate,
            'network_banks': self.network_banks,
            'network_pooling': self.network_pooling,
            'ica_ev_limit': self.ica_ev_limit,
            'ica_min_ICAs': self.ica_min_ICAs,
            'ica_max_ICAs': self.ica_max_ICAs,
            'ica_overwrite_previous_models': self.ica_overwrite_previous_models,
            'dendrogram_method': self.dendrogram_method,
            'waveforms_n_samples': self.waveforms_n_samples
        }

        ssn_json_file = (f'{self.data_savepath}config/{self.data_network}_{self.data_station}_{self.data_location}_'
                         f'{self.network_name}.json')

        with open(ssn_json_file, 'w', encoding='utf8') as jsonfile:
            json.dump(sc_config, jsonfile)

        print(f'SSN config stored at "{ssn_json_file}"')

    def config_show(self):
        """
        Prints the attributes of the object as a dictionary.

        This function prints the attributes of the object as a dictionary using the `__dict__` attribute. The attributes
         are the instance variables of the object.

        Parameters:
            self (object): The object whose attributes are to be printed.

        """
        print(self.__dict__)

    def list_available_configurations(self):
        """
        Lists all the available configurations in the config directory.

        This function uses the `glob` function to find all the JSON files in the config directory.
        It prints the list of JSON files found.

        Parameters:
            self (object): The instance of the class.
        """
        print(glob(f'{self.data_savepath}config/*json'))
