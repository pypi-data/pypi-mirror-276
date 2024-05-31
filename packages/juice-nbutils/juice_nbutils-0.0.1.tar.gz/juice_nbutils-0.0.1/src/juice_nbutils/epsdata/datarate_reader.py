import datetime
import os
from pathlib import Path

import pandas as pd

from .abstract_reader import CURRENT_TIME, DATETIME_KEY, AbstractReader
from .epsoutput import EpsOutput


class DataRateAverage(AbstractReader):
    """
    This class allows to handle (read, write) date_rate_avg produce as eps_output by MAPPS/EPS Tools
    """

    def __init__(self, input_file_path, read_start=None, experiment_to_ignore=None):

        experiment_to_ignore = [] if experiment_to_ignore is None else experiment_to_ignore

        self.data_frame = self.get_data_frame(input_file_path, read_start, experiment_to_ignore)

        if self.data_frame is not None:
            self.__get_eps_output_report_time_step__()

            self.start = pd.to_datetime(self.data_frame[DATETIME_KEY].iloc[0])
            self.end = pd.to_datetime(self.data_frame[DATETIME_KEY].iloc[-1])

    def __read(self, input_file_path):
        """
        Read and parse date_rate_avg file

        :param input_file_path: path of the input data_rate_avg.out file
        :return data_out: EpsOutput Object
        """

        input_file_path = Path(os.path.expandvars(input_file_path))
        if not Path.exists(input_file_path):
            mssg = f"Data rate average file {input_file_path} does not exist"
            raise RuntimeError(mssg)

        data_out = EpsOutput(input_file_path.name)

        with Path.open(input_file_path) as f:
            for line in f.read().splitlines():  # readlines():
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
            list_of_float = [float(x) for x in line.split(",")[1:]]
            list_of_values.extend(list_of_float)
            data_out.data_value.append(list_of_values)


    def get_data_frame(self, input_file_path, read_start=None, experiment_to_ignore=None):
        """
        Return eps data_rate_avg as pandas frames

        :param input_file_path:
        :param read_start: Allow to specify the first time to read
        :param experiment_to_ignore: list of experiment to ignore
        :return: df: panda data frame
        """

        experiment_to_ignore = [] if experiment_to_ignore is None else experiment_to_ignore

        datetime_format = "%d-%b-%Y_%H:%M:%S"

        data_out = self.__read(input_file_path)

        # Create data frame keys
        df_keys = [data_out.data_title[0][j] + ":" + data_out.data_title[1][j]
                   for j in range(len(data_out.data_title[0]))]

        # Fill data frame dictionary
        df_dictionary = {}
        for i in range(len(df_keys)):
            df_dictionary[df_keys[i]] = []
            for line in data_out.data_value:
                df_dictionary[df_keys[i]].append(line[i])

        if ":Current time" in df_dictionary:

            df_dictionary[CURRENT_TIME] = df_dictionary.pop(":Current time")

            df_dictionary[DATETIME_KEY] = []
            for t in df_dictionary[CURRENT_TIME]:
                date_time = datetime.datetime.strptime(t, datetime_format)
                df_dictionary[DATETIME_KEY].append(date_time)
            data_out.start_utc = datetime.datetime.strptime(df_dictionary[CURRENT_TIME][0], datetime_format)

        else:
            messg = f"Error in EPS file format: {input_file_path}"
            raise RuntimeError(messg)

        df_dictionary = {k: v for k, v in df_dictionary.items() if not k.startswith("JUICE:")}
        for experiment in experiment_to_ignore:
            df_dictionary = {k: v for k, v in df_dictionary.items() if not k.startswith(f"{experiment}:")}

        data_frame = pd.DataFrame(df_dictionary)

        if read_start:
            data_frame = data_frame[data_frame[DATETIME_KEY] >= read_start]
            data_frame.reset_index(drop=True, inplace=True)

        return data_frame


    def __get_eps_output_report_time_step__(self):
        """
        Calculates the eps output report time step in seconds.
        """

        self.report_time_step = (self.data_frame[DATETIME_KEY][1]
                                 - self.data_frame[DATETIME_KEY][0]).total_seconds()

        self.Kbits_sec_to_Gbits_dt = self.report_time_step / 1000 / 1000

    def get_generated_data_volume(self):
        """
        Return the total volume generated in Gbits
        This is the sum of uploaded data per instrument
        Note that is equivalent to Accum
        :return:
        """
        dic_summary = self.get_uploaded_data_volume()
        sum_of_uploaded_data = 0

        for k in sorted(dic_summary.keys()):
            sum_of_uploaded_data += dic_summary[k]

        return sum_of_uploaded_data

    def get_uploaded_data_volume(self, inst_filter=None):
        """
        Returns a dictionary including the data volume uploaded for each instrument

        :param inst_filter: this list allow to filter a subset of instrument; by default all instrument.
        Note that is equivalent to Accum
        :return:
        """
        inst_filter = [] if inst_filter is None else inst_filter

        if len(inst_filter) == 0:
            inst_filter = [k for k in self.data_frame if "Upload" in k]

        dic_summary = {}
        for param in inst_filter:
            instrument = param.split(":")[0]
            dic_summary[instrument] = (self.data_frame[param].sum() - self.data_frame[param].iloc[0])\
                                      / 1000 / 1000 * self.report_time_step

        return dic_summary

    def get_total_accum_data_volume(self, inst_filter=None, label_to_ignore=None):
        """
        Returns a dictionary including the data volume accumulated (downlink) for each instrument

        Note that assuming initial value could be no null we have to subtract it

        :param inst_filter: this list allow to filter a subset of instrument; by default all instrument.
        :param label_to_ignore: label use to remove Accum not related to experiments
        :return: dic_summary
        """

        inst_filter = [] if inst_filter is None else inst_filter
        label_to_ignore = ["KAB_LINK", "XB_LINK"] if label_to_ignore is None else label_to_ignore

        if len(inst_filter) == 0:
            inst_filter = [k for k in self.data_frame if "Accum" in k and "SSMM" not in k]
            for of in label_to_ignore:
                inst_filter = [k for k in inst_filter if of not in k]

        dic_summary = {}
        for param in inst_filter:
            instrument = param.split(":")[0]
            dic_summary[instrument] = self.data_frame[param].iloc[-1] - self.data_frame[param].iloc[0]

        return dic_summary

    def get_total_downlink(self, antenna_label=None):
        """
        Return the total downlink in Gbits including RF X-band + RF Ka-band
        Note: due to round errors could nul if report_time_step to big (i.e. 1day=86400)

        :param antenna_label: label use to filter antenna values
        return: df: dataframe including downlink per experiment
        """

        if antenna_label:

            total_downlink = self.data_frame[f"{antenna_label}:Downlink"].sum() / 1000 / 1000 * self.report_time_step

        else:

            total_downlink = \
                self.data_frame["KAB_LINK:Downlink"].sum() / 1000 / 1000 * self.report_time_step \
                + self.data_frame["XB_LINK:Downlink"].sum() / 1000 / 1000 * self.report_time_step

        return total_downlink

    def get_total_ssmm_accum(self, experiment="SSMM"):
        """
        Return the values in Gbit of SSMM accumulated at the end of scenario
        This means the total (X + KA bands) data downlink to ground

        :param experiment: experiment; to use in case SSMM Platform and science are included
        :return: get_total_ssmm_accum
        """

        col_label = f"{experiment}:Accum"
        return self.data_frame[col_label].iloc[-1] - self.data_frame[col_label].iloc[0]

    def get_x_band_accum(self):
        """
        Return the values in Gbit accumulated at the end of scenario
        This means the data downlink to ground in Gbit for RF X-band

        :return: X band Total downlink
        """
        col_label = "XB_LINK:Accum"
        return self.data_frame[col_label].iloc[-1] - self.data_frame[col_label].iloc[0]

    def get_ka_band_accum(self):
        """
        Return the values in Gbit of accumulated data at the end of scenario
        This means the data downlink to ground in Gbit for RF Ka-band

        :return: K band Total downkink
        """

        col_label = "KAB_LINK:Accum"
        return self.data_frame[col_label].iloc[-1] - self.data_frame[col_label].iloc[0]

    def get_ssmm_initial_value(self, ssmm_type="SSMM"):
        """
        Provide the SSMM value at the end of scenario
        :param ssmm_type: SSMM type; to use in case SSMM Platform and science are included
        :return: ssmm_last_value: SSMM last value in Gbit
        """

        return self.data_frame[f"{ssmm_type}:Memory"].iloc[0]

    def get_ssmm_last_value(self, ssmm_type="SSMM"):
        """
        Provide the SSMM value at the end of scenario
        :param ssmm_type: SSMM type; to use in case SSMM Platform and science are included
        :return: ssmm_last_value: SSMM last value in Gbit
        """

        return self.data_frame[f"{ssmm_type}:Memory"].iloc[-1]
