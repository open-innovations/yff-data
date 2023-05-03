import re
import numpy as np
import math


def slugify(s):
    # TODO try replace '\W+'
    return re.sub(r'[\*\-\=\(\)\s\,\"\:\(/)]+', '_', s.lower())


def round_up(x):
    '''round up to nearest 5'''
    return math.ceil(x/5)*5

def tick_gen(data, step=5, dtype=None):
    '''
    A function to generate tick labels in json format,
    to work with OI lume charts

    Inputs
    -------
        data: pandas dataframe
        step: 
        dtype: 'percentage' or 'level'

    Returns
    -------
        tick_min: minimum value of dataset (=0 for levels)
        tick_max: max value rounded up to sensible number
        ticks_labels: list of tick values and labels
    '''
    max_val = max(data.max(axis=1, numeric_only=True))
    min_val = min(data.min(axis=1, numeric_only=True))
    labels = []

    if dtype == 'percentage':

        tick_max = round_up(max_val)
        if min_val > 0:
            tick_min = 0
        else:
            tick_min = -1*round_up(-1*min_val)

        ticks = np.arange(tick_min, tick_max+5, 5)

        for i in ticks:
            labels.append("{}{}".format(i, "%"))

    elif dtype == 'level':
        tick_min = 0
        base = 5 * 10**(int(np.log10(max_val))-1)
        tick_max = math.ceil(max_val/base)*base
        vals = []

        for i in [2, 5, 10]:
            for k in range(7, -7, -1):
                num = i*(10**k)
                check = tick_max % num
                if check == 0:
                    vals.append(num)

        if max_val - min_val > 5:
            val_to_use = max(vals)
        else:
            val_to_use = min(vals)
            # print(vals)

        fact = int((tick_max / val_to_use) + 1)
        ticks = np.linspace(0, tick_max, fact)

        for i in ticks:
            labels.append("{}".format(i))

    tick_labels = [{'value': tick, 'label': label}
                   for tick, label in zip(ticks, labels)]

    if len(tick_labels) > 6:
        del tick_labels[1:-1: 2]

    return tick_min, tick_max, tick_labels
