import time
from otii_tcp_client import otii_client

BOOT_DURATION = 30.0

RASPBERRY_VOLTAGE = 5.1
CURRENT_LIMIT = 4.5

class AppException(Exception):
    '''Application Exception'''

def basic_measurement(otii: otii_client.Connect) -> None:
    '''
    This example shows you how to configure and
    start a recording of the main current channel.
    '''

    # -------------------------------------------------
    # Configure the device and prepare for recording
    # -------------------------------------------------

    # Get a reference to a Arc device
    devices = otii.get_devices()
    if len(devices) == 0:
        raise AppException('No Arc are connected!')
    device = devices[0]

    # Get the active project
    project = otii.get_active_project()

    # Configure the device
    device.set_main_voltage(RASPBERRY_VOLTAGE)
    device.set_max_current(CURRENT_LIMIT)

    # Enable the main current channel
    device.enable_channel('mc', True)



    # -------------------------------------------------
    # Perform the recording and get statistics
    # -------------------------------------------------

    # Turn on the main output of the selected device
    device.set_main(True)

    # Wait for boot and stabilization
    time.sleep(BOOT_DURATION)

    # launching the model and wait for it to finish
    # ...

    # Start a recording
    project.start_recording()

    # Performing LLM inferences
    # ...

    # Stop the recording
    project.stop_recording()

    # Turn off the main output of the selected device
    device.set_main(False)


    # Get statistics for the recording
    recording = project.get_last_recording()
    assert recording is not None

    print('Recording info')
    print('==============')
    print(f'Name:        {recording.name}')
    print(f'Start time:  {recording.start_time}')
    print('Measurements:')
    if recording.measurements is not None:
        for measurement in recording.measurements:
            print('    ', end='')
            print(f'Device: {measurement["device_id"]}', end='')
            print(f', {measurement["channel"]}', end='')
            if 'sample_rate' in measurement:
                print(f', sample rate: {measurement["sample_rate"]}', end='')
            print('')
    print('')

    info = recording.get_channel_info(device.id, 'mc')
    statistics = recording.get_channel_statistics(device.id, 'mc', info['from'], info['to'])

    # Print the statistics
    print('Statistics')
    print('==========')
    print(f'From:        {info["from"]} s')
    print(f'To:          {info["to"]} s')
    print(f'Offset:      {info["offset"]} s')
    print(f'Sample rate: {info["sample_rate"]}')
    print('')

    print(f'Min:         {statistics["min"]:.5} A')
    print(f'Max:         {statistics["max"]:.5} A')
    print(f'Average:     {statistics["average"]:.5} A')
    print(f'Energy:      {statistics["energy"] / 3600:.5} Wh')
    print(f'Charge:      {statistics["charge"] / 3600:.5} Ah')

def main() -> None:
    '''Connect to the Otii 3 application and run the measurement'''
    client = otii_client.OtiiClient()
    with client.connect() as otii:
        basic_measurement(otii)

if __name__ == '__main__':
    main()