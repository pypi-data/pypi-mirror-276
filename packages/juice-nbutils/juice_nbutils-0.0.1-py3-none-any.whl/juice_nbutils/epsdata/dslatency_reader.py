import datetime
from pathlib import Path

import numpy as np
import pandas as pd

from .abstract_reader import CURRENT_TIME, CURRENT_TIME_EPS_HEADER, DATETIME_KEY, EPS_DATE_FORMAT, AbstractReader
from .epsoutput import EpsOutput


class DsLatency(AbstractReader):
    """
    This class allows to handle (read, write) DS_latency file
    """

    def __init__(self, input_file_path, read_start=None, experiment_to_ignore=None, read_stop=None):

        experiment_to_ignore = [] if experiment_to_ignore is None else experiment_to_ignore

        self.data_frame = self.get_data_frame(input_file_path,
                                      read_start=read_start,
                                      experiment_to_ignore=experiment_to_ignore,
                                      read_stop=read_stop)

        if self.data_frame is not None:
            self.start = pd.to_datetime(self.data_frame[DATETIME_KEY][0])
            self.end = pd.to_datetime(self.data_frame[DATETIME_KEY].iloc[-1])

    def read(self, input_file_str):
        """
        Read event file

        :param input_file_path: path of the input data_rate_avg.out file
        :return EpsOutput Object
        """
        input_file_path = Path(input_file_str)
        if not Path.exists(input_file_path):
            message = f"Juice SOA data latency file {input_file_path} does not exist"
            raise RuntimeError(message)

        data_out = EpsOutput(input_file_path.name)

        with Path.open(input_file_path) as f:
            for line in f.read().splitlines():
                if line.startswith("#"):  # reading file header
                    self._read_header(line, data_out)
                elif line != "":  # Reading values
                    self.__read_value(line, data_out)

        return data_out

    def __read_value(self, line, data_out):
        if not line[0].isdigit():
            data_out.data_title.append(line.split(","))
        else:
            list_of_values = [line.split(",")[0]]
            for ele in line.split(",")[1:]:
                clean_ele = ele.rstrip()
                if clean_ele.isdigit():
                    list_of_values.append(float(clean_ele))
                else:
                    list_of_values.append(clean_ele)
            data_out.data_value.append(list_of_values)

    def get_data_frame(self, input_file_path, read_start=None, read_stop=None, experiment_to_ignore=None):
        """
        Return eps data_latency as pandas frames

        :param input_file_path:
        :param read_start: Allow to specify the first time to read
        :param experiment_to_ignore: list of experiment to ignore
        :param read_stop: Allow to specify the final time to read
        :return: df: panda data frame
        """

        experiment_to_ignore = [] if experiment_to_ignore is None else experiment_to_ignore
        data_out = self.read(input_file_path)

        # Create data frame keys
        df_keys = [data_out.data_title[0][j] + ":" + data_out.data_title[1][j]
                   for j in range(len(data_out.data_title[0]))]


        # Fill data frame dictionary
        df_dictionary = {}
        for i in range(len(df_keys)):
            df_dictionary[df_keys[i]] = []

            for line in data_out.data_value:

                # Remove undefined values +, - are set to "NaN
                if line[i] == "+" or line[i] == "-":
                    line[i] = np.nan
                df_dictionary[df_keys[i]].append(line[i])

        if not df_dictionary:
            # No latency information
            return None

        if CURRENT_TIME_EPS_HEADER in df_dictionary:
            self.__process_current_time(df_dictionary, data_out)
        else:
            message = f"Please check eps file files format: {input_file_path}"
            raise RuntimeError(message)

        df_dictionary = {k: v for k, v in df_dictionary.items() if not k.startswith("JUICE:")}
        for experiment in experiment_to_ignore:
            df_dictionary = {k: v for k, v in df_dictionary.items() if not k.startswith(f"{experiment}:")}

        data_frame = pd.DataFrame(df_dictionary)

        if read_start:
            data_frame = data_frame[data_frame[DATETIME_KEY] >= read_start]
            data_frame.reset_index(drop=True, inplace=True)
        if read_stop:
            data_frame = data_frame[data_frame[DATETIME_KEY] <= read_stop]
            data_frame.reset_index(drop=True, inplace=True)

        return data_frame


    def __process_current_time(self, df_dictionary, data_out):

        if len(df_dictionary[CURRENT_TIME_EPS_HEADER]) == 0:
            # No latency information
            message = "No latency information"
            raise RuntimeError(message)

        df_dictionary[CURRENT_TIME] = df_dictionary.pop(CURRENT_TIME_EPS_HEADER)

        # Check if relative first start time for latency is not 000_00:00:00
        # and in affirmative case insert this corresponding values

        df_dictionary[DATETIME_KEY] = []

        for t in df_dictionary[CURRENT_TIME]:
            date_time = datetime.datetime.strptime(t, EPS_DATE_FORMAT)

            df_dictionary[DATETIME_KEY].append(date_time)

        data_out.start_utc = datetime.datetime.strptime(df_dictionary[CURRENT_TIME][0], EPS_DATE_FORMAT)
