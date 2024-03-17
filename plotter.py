import os
import matplotlib.pyplot as plt
import json
from datetime import datetime
from matplotlib import colors as rc
import colorsys
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)

color_map = 'Set3'

def get_color(n):
    colors = ['seagreen','darkgreen','y','olive','gold','orange','tomato','orangered', 'indianred','brown']
    return rc.to_rgba(colors[n])

def light_dark(color, conv):
    rgb = color[:3]
    a = color[3]

    h, l, s = colorsys.rgb_to_hls(rgb[0], rgb[1], rgb[2])
    r, g, b = colorsys.hls_to_rgb(h, l*(1 + conv), s)

    return [r, g, b, a]

def desaturate(color, conv):
    rgb = color[:3]
    a = color[3]

    h, l, s = colorsys.rgb_to_hls(rgb[0], rgb[1], rgb[2])
    r, g, b = colorsys.hls_to_rgb(h, l, s*(1 + conv))

    return [r, g, b, a]

def bar_with_shade1(dates, values, name, ylab, bar_colors, line_colors, labe, path, saving):
    values_temp = values.copy()
    values = []
    for sett in values_temp:
        values.append(list(sett.values()))
    plt.figure(figsize=(14,7))
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
    
    plt.legend(bbox_to_anchor=(1.02, 0.5), loc="center left")
    
    plt.ylabel(ylab)
    plt.tight_layout()

    if saving:
        plt.savefig(os.path.join(path, 'images', name))


def bar_with_shade2(dates, values, name, ylab, labe, lines = False, path=None, saving=False):
    plt.figure(figsize=(14,7))

    # cmap = matplotlib.cm.get_cmap(color_map)
    ax = plt.gca()
    max_max_dist = 0
    if lines:
        ax.yaxis.set_major_locator(MultipleLocator(1))
        ax.yaxis.grid() # horizontal lines
        

    for n in range(len(labe)):
        # rgba = cmap(n/(len(labe)-1))
        rgba = get_color(n)
        if n == 0:
            bot = [0]*len(values)
        else:
            bot = []
            for disa in values:
                bot.append(sum(disa[:n]))
        
        plt.bar(dates, [disa[n] for disa in values],
                bottom = bot, color=rgba)

    
    plt.xticks(dates, rotation=90)
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

    max_max_dist = max(yn[f'y{len(disa)-1}'])

    for index in range(len(disa)):
        # rgba = cmap(index/(len(labe)-1))
        rgba = get_color(index)
        plt.plot(x, yn[f'y{index}'], ':', color = light_dark(rgba, -0.3))
        if index == 0:
            y1 = [0]*len(yn[f'y{index}'])
            y2 = yn[f'y{index}']
        else:
            y1 = yn[f'y{index-1}']
            y2 = yn[f'y{index}']
        plt.fill_between(x, y1, y2, color=rgba, alpha=0.15)
    
    plt.title(name)
    for n in range(len(labe)):
        # rgba = cmap(n/(len(labe)-1))
        rgba = get_color(n)
        if n == 0:
            bot = [0]*len(values)
        else:
            bot = []
            for disa in values:
                bot.append(sum(disa[:n]))
        
        plt.bar(dates, [disa[n] for disa in values],
                bottom = bot, color=rgba, label = f'({labe[n-1] if n != 0 else 0}, {labe[n]})')
    
    plt.legend(bbox_to_anchor=(1.02, 0.5), loc="center left")
    
    plt.ylabel(ylab)

    plt.ylim([0, max_max_dist*1.1])

    plt.tight_layout()
    
    if saving:
        plt.savefig(os.path.join(path, 'images', name))

def showall(datum, path, saving = True):
    if saving and not os.path.exists(os.path.join(path, "images")):
        os.makedirs(os.path.join(path, "images"))

    all_data = datum['information']

    distancia = []
    timer = []
    avg_speed = []
    heartrate = []
    dates = []
    vo2 = []
    if 'VO2' in datum:
        vo2 = (datum['VO2'])

    for date, data in all_data.items():
        

        total_time = 0

        intervals = [value for value in data.keys() if type(value) == int]
        total_distance = {inter:0 for inter in intervals}
        total_times = {inter:0 for inter in intervals}

        for interval in intervals:
            for period in data[interval]['periods']:
                total_times[interval] += period[1] - period[0]
                if period[1] > total_time:
                    total_time = period[1]

            for distant in data[interval]['distance']:
                total_distance[interval] += distant[1] - distant[0]

        distancia.append(list(total_distance.values()))
        timer.append([value/60 for value in total_times.values()])
        avg_speed.append(data['max_distance']/(total_time/3600))
        heartrate.append(data['heartrate'])

        dates.append(datetime.strptime(date, '%m/%d/%Y'))

    bar_with_shade2(dates, distancia, 'Distancia recorrida', 'Distancia [km]',
                   intervals, True, path, saving)
    
    bar_with_shade2(dates, timer, 'Tiempo', 'Tiempo [min]',
                   intervals, False, path, saving)
    
    lab = []
    for index, lim in enumerate(data['heartrate'].keys()):
        if index == 0:
            lab.append(f'(0, {lim})')
        else:
            lab.append(f'({list(data["heartrate"].keys())[index-1]}, {lim})')

    bar_with_shade1(dates, heartrate, 'Heartrate Zones', 'Cuantity',
                   ['seagreen', 'y', 'gold', 'tomato', 'indianred'],
                   ['darkgreen', 'olive', 'orange', 'orangered', 'brown'],
                   lab, path, saving)
    
    ########################

    plt.figure()
    plt.rc('axes', axisbelow=True)
    plt.grid()
    plt.bar(dates, avg_speed, color = 'seagreen')
    plt.title('Average Speed')
    plt.ylabel('km/h')
    ax = plt.gca()
    plt.xticks(dates, rotation = 90)
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
    plt.tight_layout()

    if saving:
        plt.savefig(os.path.join(path, "images", 'Average Speed'))


    #########################

    if len(vo2) != 0:
        plt.figure()
        plt.title('VO2Max')
        plt.plot(dates, vo2, linestyle='-', marker='o', color = 'seagreen')
        ax = plt.gca()
        plt.xticks(dates, rotation = 90)
        plt.tight_layout()
        if saving:
            plt.savefig(os.path.join(path, "images", 'VO2max'))


    #########################
    plt.show()

if __name__ == '__main__':
    showall()