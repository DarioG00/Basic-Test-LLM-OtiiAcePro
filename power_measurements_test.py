#!/usr/bin/env python3

import time
from otii_tcp_client import otii_client

MEASUREMENT_DURATION = 5.0
NUM_RECORDINGS = 5

class AppException(Exception):
    pass


def run_measurement(otii, device, project, index):

    print(f'\n=== Recording {index + 1} ===')

    # Avvia recording
    project.start_recording()

    # Accende DUT
    device.set_main(True)

    # Attende
    time.sleep(MEASUREMENT_DURATION)

    # Spegne DUT
    device.set_main(False)

    # Stop recording
    project.stop_recording()

    # Recupera ultima registrazione
    recording = project.get_last_recording()

    if recording is None:
        raise AppException('Recording non trovata')

    # Statistiche canale corrente main
    info = recording.get_channel_info(device.id, 'mc')

    stats = recording.get_channel_statistics(
        device.id,
        'mc',
        info['from'],
        info['to']
    )

    print(f'Nome:     {recording.name}')
    print(f'Average:  {stats["average"]:.6f} A')
    print(f'Min:      {stats["min"]:.6f} A')
    print(f'Max:      {stats["max"]:.6f} A')
    print(f'Energy:   {stats["energy"] / 3600:.6f} Wh')
    print(f'Charge:   {stats["charge"] / 3600:.6f} Ah')


def main():

    client = otii_client.OtiiClient()

    with client.connect() as otii:

        devices = otii.get_devices()

        if not devices:
            raise AppException('Nessun device trovato')

        device = devices[0]

        # Configurazione device
        device.set_main_voltage(3.7)
        device.set_exp_voltage(3.3)
        device.set_max_current(0.5)

        # Enable main current
        device.enable_channel('mc', True)

        project = otii.get_active_project()

        # Esegue 5 recording
        for i in range(NUM_RECORDINGS):

            run_measurement(
                otii,
                device,
                project,
                i
            )

            # pausa opzionale tra recording
            time.sleep(1)


if __name__ == '__main__':
    main()