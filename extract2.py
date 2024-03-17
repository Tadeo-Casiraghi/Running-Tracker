import pandas as pd
import matplotlib.pyplot as plt
import os
import json
from plotter2 import showall

def find_limits(limit, speed):
    for sides in limit:
        if sides[0] <= speed < sides[1]:
            return sides
    
    print('Excedes limits')
    return sides

with open('data.json', 'r') as json_file:
    if json_file.read(1) != '':
        json_file.seek(0)
        all_data = json.load(json_file)
    else:
        all_data = {}

with open('processed.txt', 'r') as file:
    processed = file.readlines()
processed = [ proc[:-1] for proc in processed]

lista = [ valor for valor in os.listdir() if '.csv' in valor ]
lista.sort()

limits = [(0,7),
          (7,9),
          (9,10),
          (10,11),
          (11,12),
          (12,13),
          (13,14),
          (14,15),
          (15,16),
          (16,17)]

heartrate_zones = [119, 139, 159, 179, 199]

for valor in lista:
    if valor in processed:
        print(f'{valor} already processed')
    else:
        print(f'Processing {valor}')
        data = pd.read_csv(valor)
        mask = (data['Speed (mps)'] != 0) & ((data['Distance in Meters'] != 0) | (data['Time Offset'] < 100))
        date = data['Date (US)'].iloc[0][:10]
        time = data['Time Offset'].loc[mask]
        speed_data = data['Speed (mps)'].loc[mask] * 3600/1000
        distance_data = data['Distance in Meters'].loc[mask] /1000
        heartrate = data['Heart Rate'].loc[data['Heart Rate'] != 0]
        vo2 = data['Vo2'].iloc[0]

        
        plt.figure()
        plt.plot(time, speed_data)
        for group in limits:
            plt.plot([time.iloc[0], time.iloc[-1]],[group[1]]*2)
        plt.show()

        values = {'heartrate': []}
        for slice in limits:
            values[slice[-1]] = {'time':[], 'speed':[], 'periods':[], 'distance':[]}

        prev_distance = 0
        last_limi = 0

        for t, s, d in zip(time, speed_data, distance_data):
            limi = find_limits(limits, s)
            limi = limi[-1]
            if last_limi != limi:
                values[limi]['periods'].append([t])
                if last_limi != 0:
                    values[last_limi]['periods'][-1].append(t)
                    values[last_limi]['distance'].append([prev_distance, d])
                last_limi = limi
                prev_distance = d

            values[limi]['time'].append(t)
            values[limi]['speed'].append(s)

        values[limi]['periods'][-1].append(t)
        values[limi]['distance'].append([prev_distance, d])
        prev_distance = d

        heartrate_values = {}
        for zone in heartrate_zones:
            heartrate_values[zone] = 0

        for heart in heartrate.tolist():
            for limit in heartrate_zones:
                if heart <= limit:
                    heartrate_values[limit] += 1
                    break
            if heart > heartrate_zones[-1]:
                print('Over max heartrate')

        values['heartrate'] = heartrate_values
        values['max_distance'] = distance_data.iloc[-1]

        values['vo2max'] = vo2

        all_data[date] = values

        with open('processed.txt', 'a') as file:
            file.write(valor + '\n')
        
with open('data.json', 'w') as file:
    json.dump(all_data, file, indent = 4)


showall()
