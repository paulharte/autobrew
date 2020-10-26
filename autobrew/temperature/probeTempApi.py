import os
import glob
import time


def initialise_probes():
    os.system("modprobe w1-gpio")
    os.system("modprobe w1-therm")


def get_temp_sources() -> []:
    initialise_probes()
    base_dir = "/sys/bus/w1/devices/"
    device_folders = glob.glob(base_dir + "28*")
    device_files = []
    for device_folder in device_folders:
        device_files.append(device_folder + "/w1_slave")
    return device_files


def read_temp_raw(file: str):
    f = open(file, "r")
    lines = f.readlines()
    f.close()
    return lines


def read_temp(file: str) -> float:
    lines = _extract_valid_file_lines(file)
    equals_pos = lines[1].find("t=")
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2 :]
        temp_c = float(temp_string) / 1000.0
        return temp_c


def _extract_valid_file_lines(file: str):
    for i in range(0, 100):
        lines = read_temp_raw(file)
        if lines[0].strip()[-3:] == "YES":
            return lines
        time.sleep(0.2)
    raise InvalidTemperatureFileError(file)


class InvalidTemperatureFileError(RuntimeError):
    pass
