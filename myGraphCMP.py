import fastf1 as ff1
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np


quali = ff1.get_session(2024, 'Canada', 'Q')
quali.load()
laps = quali.laps

cornerlines = quali.get_circuit_info().corners['Distance']


cornerlines = quali.get_circuit_info().corners['Distance']

fastVER   = laps.pick_drivers(1).pick_fastest().get_telemetry().add_distance()
distance  = fastVER['Distance']
VERcolour = 'orange'
ver = 'Verstappen'

fastRUS   = laps.pick_drivers(63).pick_fastest().get_telemetry().add_distance()
RUScolour = 'blue'
rus  = 'Russell'


headers = ['Date','SessionTime', 'DriverAhead', 'DistanceToDriverAhead',
            'Time', 'RPM', 'Speed', 'nGear', 'Throttle', 'Brake', 'DRS',
              'Source', 'RelativeDistance', 'Status', 'X', 'Y', 'Z',
                'Distance']



# graphing speed, near, throttle and brake cmp using interpolated data points to 
# remove bias of more/less data points recorded

common_distances = np.linspace(0, 5800, 700)
fig, axes = plt.subplots(3, figsize=(30, 10))

for row, header, ymax in zip(range(3), headers[5:8], [12500, 300, 10]):
    IPfastVERvals = np.interp(common_distances, fastVER['Distance'], fastVER[header])
    IPfastRUSvals = np.interp(common_distances, fastRUS['Distance'], fastRUS[header])

    axes[row].plot(common_distances, IPfastVERvals, label=ver, color=VERcolour)
    axes[row].plot(common_distances, IPfastRUSvals, label=rus, color=RUScolour)
    axes[row].set_title(f"{header} comparison relative to track distance (interpolated)")
    axes[row].set_xlabel("Distance (m)")
    axes[row].set_ylabel(f"{header}")

    axes[row].legend()
    axes[row].grid(True, linestyle="--", alpha=0.6)
    axes[row].vlines(cornerlines, linestyles='dotted', colors='grey', ymin=0, ymax=ymax)

plt.tight_layout()
plt.show()
