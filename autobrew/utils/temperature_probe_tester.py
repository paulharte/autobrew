import os
import glob
import time

""" This is a useful script for testing the DS18B20 temperature probes attached to your raspberry pi.
Will work for x number of attached probes (you can attach them to the same pins)
A good tutorial on how to hook up a single on and install is here: pimylifeup.com/raspberry-pi-temperature-sensor/
"""


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


def read_temp_raw(file):
    f = open(file, "r")
    lines = f.readlines()
    f.close()
    return lines


def read_temp(file):
    lines = read_temp_raw(file)
    while lines[0].strip()[-3:] != "YES":
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find("t=")
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2 :]
        temp_c = float(temp_string) / 1000.0
        return temp_c


def main():
    device_files = get_temp_sources()
    while True:
        for file in device_files:
            print("File: " + str(file))
            print(read_temp(file))
        time.sleep(2)


main()
