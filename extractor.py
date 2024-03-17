import pandas as pd
import matplotlib.pyplot as plt
import os
import json
from plotter import showall

class Extractor():
    
    def __init__(self, path_to_directory):
        self.speed_limits = [(0,7), (7,9), (9,10), (10,11), (11,12),
                             (12,13), (13,14), (14,15), (15,16), (16,17)]
        
        self.heartrate_zones = [119, 139, 159, 179, 199]
        
        self.path = path_to_directory
        self.datasets_path = os.path.join(self.path, "datasets")
        self.data_path = os.path.join(self.path, 'data.json')
        self.processed_path = os.path.join(self.path, 'processed.txt')
        if 'processed.txt' not in os.listdir(self.path):
            with open(self.processed_path, 'w') as _: pass
            self.processed = []
        else:
            self.processed = []
            with open(self.processed_path, 'r') as process:
                if process.read(1) != '':
                    process.seek(0)
                    self.processed.extend([name[:-1] for name in process.readlines()])
        
        if 'data.json' not in os.listdir(self.path):
            with open(self.data_path, 'w') as _: pass
            self.track = []
            self.data = {'information': {}}
        else:
            with open(os.path.join(self.path, 'data.json'), 'r') as json_file:
                if json_file.read(1) != '':
                    json_file.seek(0)
                    self.data = json.load(json_file)
                    self.track = self.data['tracking']
                else:
                    self.data = {'information': {}}
                    self.track = []
    
    def plot(self,):
        if len(self.processed) == 0:
            print('It appears you dont have any data processed yet')
        else:
            showall(self.data, self.path, False)
    
    def plot_and_save(self,):
        if len(self.processed) == 0:
            print('It appears you dont have any data processed yet')
        else:
            showall(self.data, self.path)
    
    def add_VO2(self,):
        if 'VO2' in self.data:
            print('The available data is:')
            for saved, value in self.data['VO2'].itemize():
                print(f'\t{saved}: {value}')
        
        again = True
        while again:
            date = input('Please input the date in US format (mm/dd/yyyy):   ')
            vo2 = float(input('Please input the corresponding VO2 value:   '))
            self.data['VO2'][date] = vo2
            again = True if 'y' == input('again [y/n]?') else False
        
    def define_tracking(self,):
        print('Please input what tracking categories you would prefer (separated by spaces):')
        print('For example: "Distance in Meters", "Heart Rate", "Speed (mps)" or default for those three')
        user = input()
        if user == 'default':
            self.track = ["Distance in Meters", "Heart Rate", "Speed (mps)"]
        else:
            self.track = user.strip().split()
        self.data['tracking'] = self.track

    def add_tracking(self,):
        print('Please input what tracking categories you would like to add (separated by spaces):')
        user = input()
        self.track.extend(user.strip().split())
        self.data['tracking'] = self.track
        
    def process(self,):
        files = [name for name in os.listdir(self.datasets_path)]
        files.sort()
        
        for name in files:
            if name in self.processed:
                print(f'{name} already processed')
            else:
                print(f'Processing {name}')
                self.processed.append(name)
                data = pd.read_csv(os.path.join(self.datasets_path, name))
                mask = (data['Speed (mps)'] != 0) & ((data['Distance in Meters'] != 0) | (data['Time Offset'] < 100))
                date = data['Date (US)'].iloc[0][:10]
                time = data['Time Offset'].loc[mask]

                values = {}

                if 'Speed (mps)' in self.track:
                    speed_data = data['Speed (mps)'].loc[mask] * 3600/1000
                    plt.figure()
                    plt.plot(time, speed_data)

                    for group in self.speed_limits:
                        plt.plot([time.iloc[0], time.iloc[-1]],[group[1]]*2)
                    
                    plt.show()
                if 'Distance in Meters' in self.track:
                    distance_data = data['Distance in Meters'].loc[mask] /1000
                if 'Heart Rate' in self.track:   
                    heartrate = data['Heart Rate'].loc[data['Heart Rate'] != 0]
                    values['heartrate'] = []

                
                
                for slice in self.speed_limits:
                    values[slice[-1]] = {'time':[], 'speed':[], 'periods':[], 'distance':[]}

                prev_distance = 0
                last_limi = 0

                for t, s, d in zip(time, speed_data, distance_data):
                    limi = self.find_limits(self.speed_limits, s)
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
                for zone in self.heartrate_zones:
                    heartrate_values[zone] = 0

                for heart in heartrate.tolist():
                    for limit in self.heartrate_zones:
                        if heart <= limit:
                            heartrate_values[limit] += 1
                            break
                    if heart > self.heartrate_zones[-1]:
                        print('Over max heartrate')

                values['heartrate'] = heartrate_values
                values['max_distance'] = distance_data.iloc[-1]

                self.data['information'][date] = values

                with open(self.processed_path, 'a') as file:
                    file.write(name + '\n')
                
    def save_data(self,):
        with open(self.data_path, 'w') as file:
            json.dump(self.data, file, indent = 4)
    

    def find_limits(self, limit, speed):
        for sides in limit:
            if sides[0] <= speed < sides[1]:
                return sides
            
        print('Excedes limits')
        return sides
