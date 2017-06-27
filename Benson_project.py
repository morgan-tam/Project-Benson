import os
import pandas as pd
from datetime import datetime
from collections import defaultdict
import numpy as np

def read_data(path):
    '''opens all txt files in the given directory and creates a df'''
    all_data = pd.DataFrame()
    for filename in os.listdir(path):
        with open(path+str(filename)) as f:
            df = pd.read_csv(f)
            all_data = all_data.append(df)
    all_data.columns = ['C/A', 'UNIT', 'SCP', 'STATION', 'LINENAME', 'DIVISION', 'DATE', 'TIME','DESC', 'ENTRIES', 'EXITS']
    return all_data

def save_as_csv(df, path):
    '''saves df in given directory'''
    df.to_csv(path+'all_data.csv')

def transit_per_station(all_data):
    '''Get number of people going through a station for the whole period of time considered. Returns dict with
    station: transit'''
    station_transit = {}
    for station in all_data.STATION.unique():
        df = all_data.loc[all_data['STATION'] == station]
        entries = df.ENTRIES
        exits = df['EXITS']
        saldo_entries = entries.max() - entries.min()
        saldo_exits = exits.max() - exits.min()
        transit = saldo_entries + saldo_exits
        station_transit[station] = transit
    return station_transit

def transit_per_station(all_data):
    '''Get number of people going through a station for the whole period of time considered. Returns dict with
    station: transit'''
    # tries to take into account single turnstiles
    db = all_data.set_index(['C/A', 'UNIT', 'SCP','STATION'])
    list_of_turnstiles = np.unique(db.index.values).tolist()
    station_transit = defaultdict(int)
    for turnstile in list_of_turnstiles:
        turndf = db.loc[turnstile]
        entries = turndf.ENTRIES
        exits = turndf.EXITS
        saldo_entries = entries.max() - entries.min()
        saldo_exits = exits.max() - exits.min()
        transit = saldo_entries + saldo_exits
        station_transit[turnstile[3]] += transit
    return station_transit

# actually, this gets correct results. So based on this, correct the code:

from collections import defaultdict
import csv
from datetime import datetime

DATE_FORMAT = '%m/%d/%Y'
with open('turnstile_160702.txt') as f:
    reader = csv.reader(f)
    data = list(reader)
    date_and_entries = defaultdict(list)
    for i in range(1, len(data)):
        row = data[i]
        dts = str(row[6])
        date = datetime.strptime(dts, DATE_FORMAT)
        t = (row[0], row[1], row[2], row[3], date)
        date_and_entries[t].append(int(row[9]))
        i = 0
    entries_per_day = {}
    for k, v in date_and_entries.items():
        key = k[:-1]
        maxim = sorted(v)[-1]
        minim = sorted(v)[0]
        value = [k[-1], maxim - minim]
        entries_per_day[key] = value

data = read_data('/Users/aleksandra/ds/metis/metisgh/metis_projects/mta_project/data_mta/')
transit = transit_per_station(data)


