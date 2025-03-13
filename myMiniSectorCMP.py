import fastf1 as ff1
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np


race = {
    'Year': 2024,
    'Venue': 'Canada',
    'Mode': ['Q','R']
}

driver1 = {
    'Name': 'Max Verstappen',
    'Number': 1,
    'Colour': 'orange',
    'Code': 'VER'
}

driver2 = {
    'Name': 'George Russell',
    'Number': 63,
    'Colour': 'blue',
    'Code': 'RUS'    
}


quali = ff1.get_session(race['Year'], race['Venue'], race['Mode'][0])
quali.load()
laps = quali.laps


fastd1   = laps.pick_drivers(driver1['Number']).pick_fastest().get_telemetry().add_distance()
fastd2   = laps.pick_drivers(driver2['Number']).pick_fastest().get_telemetry().add_distance()

distance  = fastd1['Distance']
cornerlines = quali.get_circuit_info().corners['Distance']
headers = ['Date','SessionTime', 'DriverAhead', 'DistanceToDriverAhead',
            'Time', 'RPM', 'Speed', 'nGear', 'Throttle', 'Brake', 'DRS',
              'Source', 'RelativeDistance', 'Status', 'X', 'Y', 'Z',
                'Distance']

# interpolating all telemetry data to make sure comparisons are accurate.
# removes the bias of unequal data points in telemetry.

headers = ['Speed', 'X', 'Y']

common_distances = np.linspace(0, 4360, 748)

driver1df = pd.DataFrame()
driver2df = pd.DataFrame()



for header in headers:

    # now, I have made interpolated values for speed and their X and Y positions on their hot lap
    driver1df[header] = np.interp(common_distances, fastd1['Distance'], fastd1[header])
    driver2df[header] = np.interp(common_distances, fastd2['Distance'], fastd2[header])


driver1df['DriverNo'] = driver1['Number']
driver2df['DriverNo'] = driver2['Number']
fastest_ms = pd.DataFrame()


# minisector comparison by speed
for msnumber in range(20):
    start_index = msnumber * 37
    end_index = start_index + 37

    d1_chunk = driver1df.iloc[start_index:end_index]
    d2_chunk = driver2df.iloc[start_index:end_index]

    # Compare the average speeds and append the faster driver's rows
    if d1_chunk['Speed'].mean() > d2_chunk['Speed'].mean():
        fastest_ms = pd.concat([fastest_ms, d1_chunk], ignore_index=True)
    else:
        fastest_ms = pd.concat([fastest_ms, d2_chunk], ignore_index=True)



# mapping DriverNo to colours
color_map = {driver1df['DriverNo'].iloc[0]: driver1['Colour'], driver2df['DriverNo'].iloc[0]: 'blue'}
fastest_ms['Color'] = fastest_ms['DriverNo'].map(color_map)

# creatning  line segments
points = fastest_ms[['X', 'Y']].to_numpy()
segments = np.array([[points[i], points[i + 1]] for i in range(len(points) - 1)])

# assigning colours to segments
colors = fastest_ms['Color'].to_numpy()


# create a LineCollection
lc = LineCollection(segments, colors=colors, linewidths=2)

# plot the track
plt.figure(figsize=(2, 6))
ax = plt.gca()
ax.add_collection(lc)
ax.autoscale()
plt.title('Driver Performance Across Minisectors', fontsize=16)

# Save the figure before displaying it
plt.savefig('figure.png', dpi=300, bbox_inches='tight')
plt.show()