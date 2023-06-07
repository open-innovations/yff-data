import re
import numpy as np
import math


def slugify(s):
    # TODO try replace '\W+'
    return re.sub(r'[\*\-\=\(\)\s\,\"\:\(/)]+', '_', s.lower())

def tick_gen(data, dtype, cut_labels=True):
    '''
    Takes a dataframe and the type of number "percentage" or "num"
    and returns the values and labels of the ticks and the max and min values.
   
    Parameters
    ------
    Data: dataframe, data in a pandas dataframe
    dtype: str, "num" or "percent"
    cut_labels:  boolean, removes some labels if there are too many, default True.

    Returns
    -------
    tick_min: float, smallest tick
    tick_max: float, argest tick
    tick_labels: list, values and labels of all ticks
    '''
    #1 calc. abs. max of absolute values
    #2 work out tick_size for tick_range
    #3 calc. chart_min and chart_max by rounding down/up to tick_size.
    #4 generate range from chartmin/max and tick_szie using linspace. reject every other if too many labels
    #6 cut labels if required
    #7 add 0 label in if not there.
    
    #get the max and min values, and find which is biggest. 
    # Abs taken as may be negative
    data = data.drop(index='Prefix')
    data_max = max(data.max(axis=1, numeric_only=True))
    data_min = min(data.min(axis=1, numeric_only=True))
    chart_max = max(abs(data_max), abs(data_min))
    
    #the base is for rounding, e.g if max is 127 we round to 150 (nearest 50)
    #if max is 1270 we round to 1300 (nearest 100)
    base = 5 * 10**(int(np.log10(chart_max))-1)
    
    #check the 3 cases of max and min values
    # round to whatever the base is set to
    if data_min and data_max >= 0:
        tick_min = 0
        tick_max = math.ceil(chart_max / base) * base
    
    if data_min <= 0 and data_max >= 0:
        tick_min = -1 * math.ceil(-1*data_min / base) * base
        tick_max = math.ceil(chart_max / base) * base
        
    if data_min <= 0 and data_max <= 0:
        tick_max = 0
        tick_min = -1 * math.ceil(-1*data_min / base) * base
    
    tick_range = tick_max-tick_min
    tick_options = []
    labels = []
    tick_array = []
    
    #check for range divisible by 2, 5, 10 for tick spacing
    for i in [2, 5, 10]: 
        for k in range(7, -7, -1):
            tick_space = i*(10**k)
            check = tick_range % tick_space
            if check == 0:
                tick_options.append(tick_space)
    
    #if the range > 5, pick largest tick spacing, 
    # otherwise pick smallest        
    if tick_range > 5:
        tick_size = max(tick_options)
    else: 
        tick_size = min(tick_options)
    
    #make the ticks
    fact = int((tick_range / tick_size) + 1)
    ticks = np.linspace(tick_min, tick_max, fact)
    
    #add these to a list as a string for use with yaml
    for i in ticks:
        if dtype == 'num':
            labels.append("{}".format(i))
            tick_array.append("{}".format(i))
        if dtype == 'percent':
            labels.append("{}{}".format(i, '%'))
            tick_array.append("{}".format(i))
    
    #set up the dictionary
    tick_labels = [{'value': tick, 'label': label} \
                   for tick, label in zip(tick_array, labels)]
    
    #if there are too many labels, cut every other apart from 1st and last.
    #@TODO Note this can cause the last tick to have a different
    #interval from the others. This is something to improve.
    if cut_labels == True:
        if len(tick_labels) > 6:
            del tick_labels[1:-1: 2]
    
    #add a 0 label if not already there        
    p = []
    for i in tick_labels:
        p.append(i.get('value'))
    if '0.0' not in p:
        tick_labels.append({'value': '0.0', 'label': '0'})
    
    return tick_min, tick_max, tick_labels

