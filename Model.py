import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import sys
import os

directory = "Data/TrainDataReal.xlsx"


class TrainData:

    bag = []
    mark = {}
    parent = {}
    dist = {}
    adj = {}

    name_to_id = {}

    df = pd.read_excel(directory)
    df = df.copy()
    df = df.drop("Column1", axis=1)
    df = df.drop("name", axis=1)

    station_list = list(df['nameEng'])

    station_id = list(df['stationId'])

    for i, name in enumerate(station_list):
        name_to_id[name] = station_id[i]

    station_list.sort()
    sorting_list = []

    for id in station_id:
        string_part = ''.join(filter(str.isalpha, id))
        int_part = ''.join(filter(str.isdigit, id))

        sorting_list.append(string_part)

    sorting_list = set(sorting_list)  # get unique strings
    sorting_list.remove('CEN')  # deal with special case manually
    station_id.remove('CEN')

    id_dict = {}

    for string_id in sorting_list:
        unique_str_int_list = []
        for id in station_id:
            string_part = ''.join(filter(str.isalpha, id))
            int_part = int(''.join(filter(str.isdigit, id)))
            if string_id == string_part:
                unique_str_int_list.append(int_part)

        max_int = max(unique_str_int_list)
        id_dict[string_id] = max_int

    for id in station_id:
        string_part = ''.join(filter(str.isalpha, id))
        string_part_check = string_part
        int_part = ''.join(filter(str.isdigit, id))
        optional_zero = ''

        if int_part.startswith('0'):
            string_part += '0'
        int_part = int(int_part)

        if int_part < 2:
            adj_id = string_part + str(int_part + 1)
            adj[id] = [adj_id]
        elif int_part >= id_dict[string_part_check]:  # if int at
            adj_id = string_part + str(int_part - 1)
            adj[id] = [adj_id]
        else:
            adj_id1 = string_part + str(int_part - 1)
            adj_id2 = string_part + str(int_part + 1)
            if str(int_part + 1) == '10':
                adj_id2 = string_part.replace('0', '') + str(int_part + 1)
            adj[id] = [adj_id1, adj_id2]

    # deal with special cases

    adj['CEN'] = ["W1", "N1", "E1", "S1"]
    adj['W1'] = ["CEN"]
    adj['N1'].append('CEN')
    adj['E1'].append('CEN')
    adj['S1'].append('CEN')
    adj['BL10'] = ['BL09', 'BL11']
    adj['PP10'] = ['PP09', 'PP11']
    adj['N5'] = ['N4', 'N7']
    adj['N7'] = ['N5', 'N8']

    # add intersection

    adj['PP16'].append('BL10')
    adj['BL10'].append('PP16')

    adj['BL13'].append('N8')
    adj['N8'].append('BL13')

    adj['A8'].append('N2')
    adj['N2'].append('A8')

    adj['S12'].append('BL34')
    adj['BL34'].append('S12')

    adj['G1'].append('S7')
    adj['S7'].append('G1')

    # print(adj)

    # now the adj list is ready

    @classmethod
    def bfs(cls, s):
        stationId = TrainData.station_id
        stationId.append('CEN')
        for id in stationId:
            cls.mark[id] = False
            cls.dist[id] = 9999
            cls.parent[id] = -1

        cls.dist[s] = 0

        cls.bag = []
        cls.bag.append((-1, s))
        while cls.bag:
            bag_item = cls.bag.pop(0)
            p = bag_item[0]
            v = bag_item[1]
            if not cls.mark[v]:
                cls.mark[v] = True

                if p != -1:
                    cls.dist[v] = cls.dist[p] + 1
                    cls.parent[v] = p

                for w in cls.adj[v]:
                    cls.bag.append((v, w))

    @classmethod
    def get_shortest_path(cls, start, destination):
        current = destination
        path = []
        while current != start:
            # print(current)
            path.insert(0, current)
            current = cls.parent[current]

        path.insert(0, start)
        return path

# YESSSSSS I FINALLY GOT A LIST OF ID OF THE SHORTEST PATH YEEEEEEEEEEEAHH
