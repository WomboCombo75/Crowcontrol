#!/usr/bin/env python3

from miflora.miflora_poller import MiFloraPoller, MI_CONDUCTIVITY, MI_MOISTURE, MI_LIGHT, MI_TEMPERATURE, MI_BATTERY
from btlewrap.bluepy import BluepyBackend
from datetime import datetime

def fetch_sensor_data(mac_address):
    try:
        poller = MiFloraPoller(mac_address, BluepyBackend)
        firmware_version = poller.firmware_version()
        sensor_name = poller.name()
        temperature = poller.parameter_value(MI_TEMPERATURE)
        moisture = poller.parameter_value(MI_MOISTURE)
        light = poller.parameter_value(MI_LIGHT)
        conductivity = poller.parameter_value(MI_CONDUCTIVITY)
        battery = poller.parameter_value(MI_BATTERY)

        return firmware_version, sensor_name, temperature, moisture, light, conductivity, battery
    except Exception as e:
        return None, None, None, None, None, None, None

def write_sensor_data_to_file(data, filename):
    current_time = datetime.now().strftime("%d.%m %H:%M")
    new_data_block = [
        'Date/Time: {}\n'.format(current_time),
        'Firmware Version: {}\n'.format(data[0]),
        'Sensor Name: {}\n'.format(data[1]),
        'Temperature: {}\n'.format(data[2]),
        'Moisture: {}\n'.format(data[3]),
        'Light: {}\n'.format(data[4]),
        'Conductivity: {}\n'.format(data[5]),
        'Battery: {}\n'.format(data[6]),
        '\n'  # Add a newline to separate data blocks
    ]

    try:
        with open(filename, 'r') as file:
            existing_data = file.readlines()
    except FileNotFoundError:
        existing_data = []

    # Find the indices of the start and end of each data block
    data_block_indices = []
    start_index = 0
    for i, line in enumerate(existing_data):
        if line.startswith("Date/Time:"):
            if start_index != i:  # Ignore empty data blocks
                data_block_indices.append((start_index, i))
            start_index = i
    data_block_indices.append((start_index, len(existing_data)))

    # Remove the oldest data block if there are already 5 blocks
    if len(data_block_indices) >= 10:
        start_index, end_index = data_block_indices[0]
        existing_data = existing_data[end_index:]  

    # Add the new data block
    data_blocks = existing_data + new_data_block

    # Write data blocks to file
    with open(filename, 'w') as file:
        file.writelines(data_blocks)

if __name__ == "__main__":
    mac_address = "1c:1c:1c:1c:1c"  # Replace with your MAC address
    sensor_data = fetch_sensor_data(mac_address)

    if sensor_data:
        write_sensor_data_to_file(sensor_data, '/path/to/where/you/want/to/store/')
