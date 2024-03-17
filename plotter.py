import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import datetime

def bar_with_shade(dates, values, name, ylab, bar_colors, line_colors, labe):
    plt.figure()
    plt.rc('axes', axisbelow=True)
    plt.grid()

    for n in range(len(labe)):
        if n == 0:
            bot = [0]*len(values)
        else:
            bot = []
            for disa in values:
                bot.append(sum(disa[:n]))
        
        plt.bar(dates, [disa[n] for disa in values],
                bottom = bot, color=bar_colors[n])

    ax = plt.gca()
    plt.xticks(dates)
    ax_width = ax.patches[0].get_width()
    xticks = ax.get_xticks()

    x = []
    yn = {}

    for tick, disa in zip(xticks, values):

        x.extend([tick - ax_width/2, tick + ax_width/2])

        for index in range(len(disa)):

            if f'y{index}' not in yn:
                yn[f'y{index}'] = []

            yn[f'y{index}'].extend([sum(disa[:index+1])]*2)

    for index in range(len(disa)):
        plt.plot(x, yn[f'y{index}'], ':', color = line_colors[index])
        if index == 0:
            y1 = [0]*len(yn[f'y{index}'])
            y2 = yn[f'y{index}']
        else:
            y1 = yn[f'y{index-1}']
            y2 = yn[f'y{index}']
        plt.fill_between(x, y1, y2, color=bar_colors[index], alpha=0.15)
    
    plt.title(name)
    for n in range(len(labe)):
        if n == 0:
            bot = [0]*len(values)
        else:
            bot = []
            for disa in values:
                bot.append(sum(disa[:n]))
        
        plt.bar(dates, [disa[n] for disa in values],
                bottom = bot, color=bar_colors[n], label=labe[n])
    
    plt.legend()
    
    plt.ylabel(ylab)

    plt.savefig(name)

def showall():
    with open('data.json', 'r') as json_file:
        all_data = json.load(json_file)

    distancia = []
    timer = []
    avg_speed = []
    heartrate = []
    runwalkd = []
    runwalkt = []
    dates = []
    vo2 = []

    for date, data in all_data.items():
        vo2.append(data['vo2max'])
        time_walking = 0
        time_running = 0

        total_time = 0

        for period in data['running']['periods']:
            time_running += period[1] - period[0]
            if period[1] > total_time:
                total_time = period[1]

        for period in data['walking']['periods']:
            time_walking += period[1] - period[0]
            if period[1] > total_time:
                total_time = period[1]

        total_disr = 0
        total_disw = 0

        for distant in data['running']['distance']:
            total_disr += distant[1] - distant[0]
        
        for distant in data['walking']['distance']:
            total_disw += distant[1] - distant[0]

        distancia.append([total_disr, total_disw])
        timer.append([time_running/60, time_walking/60])
        avg_speed.append(data['max_distance']/(total_time/3600))
        heartrate.append(data['heartrate'])

        runwalkd.append({'run':data['running']['distance'], 'walk':data['walking']['distance']})
        runwalkt.append({'run':data['running']['periods'], 'walk':data['walking']['periods']})

        dates.append(datetime.strptime(date, '%m/%d/%Y'))

    bar_with_shade(dates, distancia, 'Distancia recorrida', 'Distancia [km]',
                   ['seagreen', 'tomato'], ['darkgreen', 'orangered'],
                   ['corriendo', 'caminando'])
    
    bar_with_shade(dates, timer, 'Tiempo', 'Tiempo [min]',
                   ['seagreen', 'tomato'], ['darkgreen', 'orangered'],
                   ['corriendo', 'caminando'])

    bar_with_shade(dates, heartrate, 'Heartrate Zones', 'Cuantity',
                   ['seagreen', 'y', 'gold', 'tomato', 'indianred'],
                   ['darkgreen', 'olive', 'orange', 'orangered', 'brown'],
                   ['Zone 1', 'Zone 2', 'Zone 3', 'Zone 4', 'Zone 5'])
    
    ########################

    plt.figure()
    plt.rc('axes', axisbelow=True)
    plt.grid()
    plt.bar(dates, avg_speed, color = 'seagreen')
    plt.title('Average Speed')
    plt.ylabel('km/h')
    ax = plt.gca()
    plt.xticks(dates)
    ax_width = ax.patches[0].get_width()
    xticks = ax.get_xticks()

    x = []
    y = []

    for tick, disa in zip(xticks, avg_speed):
        x.extend([tick - ax_width/2, tick + ax_width/2])
        y.extend([disa]*2)

    plt.plot(x, y, ':', color = 'darkgreen')
    plt.fill_between(x, [0]*len(y) , y, color='seagreen', alpha=0.15)

    plt.bar(dates, avg_speed, color = 'seagreen')

    plt.savefig('Average Speed')


    #########################

    plt.figure()
    plt.title('VO2Max')
    plt.plot(dates, vo2, linestyle='-', marker='o', color = 'seagreen')
    ax = plt.gca()
    plt.xticks(dates)

    plt.savefig('VO2max')

    #########################

    plt.figure()
    plt.rc('axes', axisbelow=True)
    plt.grid()
    for date, values in zip(dates, runwalkt):
        for bot, hei in values['run']:
            plt.bar(date, hei - bot, bottom = bot, color = 'seagreen')
        
        for bot, hei in values['walk']:
            plt.bar(date, hei - bot, bottom = bot, color = 'tomato')

    ax = plt.gca()
    plt.xticks(dates)

    plt.title('Time distribution')
    plt.ylabel('Time [s]')

    plt.savefig('Time distribution')
    
    plt.show()

if __name__ == '__main__':
    showall()