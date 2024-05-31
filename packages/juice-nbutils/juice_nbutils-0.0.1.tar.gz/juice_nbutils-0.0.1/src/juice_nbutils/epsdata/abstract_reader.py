import datetime

DATETIME_KEY = "datetime (UTC)"
CURRENT_TIME = "Current time"
ELAPSEDTIME_KEY = "Elapsed time"
CURRENT_TIME_EPS_HEADER = "Current time:dd-mmm-yyyy_hh:mm:ss"
EPS_DATE_FORMAT = "%d-%b-%Y_%H:%M:%S"

class AbstractReader:

    def _read_header(self, line, data_out):
        date_format = "%d-%B-%Y"
        line = line[1:].lstrip()
        metadata_header = line.split(":")[0]
        header_value = ""
        if ":" in line:
            header_value = line.split(":")[1]
            if "Ref_date:" in line:
                ref_date_str = line.split(":")[1].strip().split("\n")[0]
                data_out.start_utc = datetime.datetime.strptime(ref_date_str, d_format=date_format)
                if not data_out.start_utc:
                    raise RuntimeError

        data_out.header.append(["#", metadata_header, header_value.lstrip()])
