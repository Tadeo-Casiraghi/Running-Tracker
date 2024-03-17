import pandas as pd
import matplotlib.pyplot as plt
import os
import json
from plotter import showall

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

for valor in lista:
    if valor in processed:
        print(f'{valor} already processed')
    else:
        print(f'Processing {valor}')
        data = pd.read_csv(valor)
        date = data['Date (US)'].iloc[0][:10]
        print(date)
        time = data['Time Offset']
        speed_data = data['Speed (mps)'].loc[data['Speed (mps)'] != 0] * 3600/1000
        speed_time = time.loc[data['Speed (mps)'] != 0]
        distance_data = data['Distance in Meters'].loc[data['Distance in Meters'] != 0] /1000
        distance_time = time.loc[data['Distance in Meters'] != 0]
        heartrate = data['Heart Rate'].loc[data['Heart Rate'] != 0]

        walking_limit = 7.5
        ready = False
        while not ready:
            plt.figure()
            plt.plot(speed_time, speed_data)
            plt.plot([speed_time.iloc[0], speed_time.iloc[-1]],[walking_limit, walking_limit])
            plt.show(block=False)
            plt.pause(0.001)
            answer = input("Is it ok?   ")
            ready = True if answer == '' else False
            walking_limit = float(answer) if not ready else walking_limit
            plt.close('all')

        values = {'heartrate': [],
                'running':{'time':[], 'speed':[], 'periods':[], 'distance':[]},
                'walking':{'time':[], 'speed':[], 'periods':[], 'distance':[]}}

        rf = False
        wf = False

        prev_distance = 0

        for t, s1, s2, s3 in zip(speed_time.iloc[1:-1], speed_data.iloc[:-2], speed_data.iloc[1:-1], speed_data.iloc[2:]):
            if (s1 < walking_limit and s2 < walking_limit) or (s2 < walking_limit and s3 < walking_limit):
                typer = 'walking'
            else:
                typer = 'running'
            
            if not rf and not wf:
                values[typer]['periods'].append([t])
                rf = True if typer == 'running' else False
                wf = True if typer == 'walking' else False
            elif rf and typer == 'walking':
                rf = False
                wf = True
                values['running']['periods'][-1].append(t)
                values['walking']['periods'].append([t])
                values['running']['distance'].append([prev_distance, distance_data.loc[distance_time == t].values[0]])
                prev_distance = distance_data.loc[distance_time == t].values[0]
            elif wf and typer == 'running':
                rf = True
                wf = False
                values['running']['periods'].append([t])
                values['walking']['periods'][-1].append(t)
                values['walking']['distance'].append([prev_distance, distance_data.loc[distance_time == t].values[0]])
                prev_distance = distance_data.loc[distance_time == t].values[0]


            values[typer]['time'].append(t)
            values[typer]['speed'].append(s2)

        if typer == 'walking':
            values['walking']['periods'][-1].append(t)
            values['walking']['distance'].append([prev_distance, distance_data.loc[distance_time == t].values[0]])
            prev_distance = distance_data.loc[distance_time == t].values[0]
        else:
            values['running']['periods'][-1].append(t)
            values['running']['distance'].append([prev_distance, distance_data.loc[distance_time == t].values[0]])
            prev_distance = distance_data.loc[distance_time == t].values[0]

        heartrate_zones = [119, 139, 159, 179, 199]
        heartrate_values = [0]*len(heartrate_zones)
        for heart in heartrate.tolist():
            for index, limit in enumerate(heartrate_zones):
                if heart <= limit:
                    heartrate_values[index] += 1
                    break

        values['heartrate'] = heartrate_values
        values['max_distance'] = distance_data.iloc[-1]

        values['vo2max'] = float(input('Ingrese el VO2Max:          '))

        all_data[date] = values

        with open('processed.txt', 'a') as file:
            file.write(valor + '\n')
        
with open('data.json', 'w') as file:
    json.dump(all_data, file, indent = 4)


showall()
