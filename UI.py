import tkinter as tk
from tkinter import ttk
from Model import TrainData

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns


class TrainUI(tk.Tk):

    def __init__(self, data: TrainData):
        super().__init__()
        self.data = data
        self.all_line = ['Airport Rail Link', 'Sukhumvit Line', 'Silom Line',
                         'Blue Line', 'Purple Line']
        self.colors = ['red', 'yellowgreen', 'darkgreen', 'blue', 'purple']
        self.init_components()

    def init_components(self):
        self.font = {'font': ('Monospace', 20)}
        self.title("Metro Path finder")
        self.header = self.create_header()
        self.header.pack(side=tk.TOP, anchor=tk.CENTER, pady=20, padx=10)

        self.selected_unit1 = tk.StringVar()
        self.selected_unit2 = tk.StringVar()

        self.box_frame = tk.Frame(self)
        self.box_frame.pack(side=tk.TOP, anchor=tk.CENTER, pady=20)
        self.start_box, self.final_box = self.create_cbb(self.box_frame)
        self.load_units(station_list=self.data.station_list)
        label = tk.Label(self.box_frame, text="To", **self.font)
        self.start_box.pack(side=tk.LEFT, padx=10)
        label.pack(side=tk.LEFT, padx=10)
        self.final_box.pack(side=tk.LEFT, padx=10)

        self.start_box.bind('<<ComboboxSelected>>', self.select_handler)
        self.final_box.bind('<<ComboboxSelected>>', self.select_handler)

        self.map_frame = tk.Frame(self)
        self.map_frame.pack(side=tk.TOP, pady=20)
        self.map = self.create_map(self.map_frame)
        self.map.get_tk_widget().pack(side=tk.TOP)

    def create_header(self):
        header = tk.Label(self,
                          text="Choose your start and final station below")
        header.configure(**self.font)
        return header

    def create_cbb(self, frame):
        start_box = ttk.Combobox(frame,
                                 textvariable=self.selected_unit1,
                                 width=20,
                                 state='readonly',
                                 **self.font)
        final_box = ttk.Combobox(frame,
                                 textvariable=self.selected_unit2,
                                 width=20,
                                 state='readonly',
                                 **self.font)

        return start_box, final_box

    def create_map(self, frame):
        # Let's do one line at a time
        fig, ax = plt.subplots(figsize=(10, 10))
        df = self.data.df.copy()

        df['lineNameEng']['CEN'] = "Sukhumvit Line"

        for count, line in enumerate(self.all_line):
            new_df = df[df['lineNameEng'] == line]
            sns.scatterplot(new_df, x='geoLng', y='geoLat',
                            color=self.colors[count])

        # Find a way to assign name to the nodes
        # And find a way to change it's color
        # then we can try to use algorithm to make a list and change color depends on the list

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()

        return canvas

    def create_path(self, frame):
        pass

    def load_units(self, station_list):
        """Load metro station into the comboboxes."""
        units = station_list
        self.start_box['values'] = units
        self.final_box['values'] = units
        self.start_box.current(newindex=0)
        self.final_box.current(newindex=0)

    def select_handler(self, event):
        start = self.start_box.get()
        start_id = self.data.name_to_id[start]
        final = self.final_box.get()
        final_id = self.data.name_to_id[final]

        if start == final:
            return
        self.data.bfs(start_id)
        path = self.data.get_shortest_path(start_id, final_id)

        df = self.data.df.copy()
        print("from", start_id, "to", final_id)
        # path_df = df[df['stationId'].isin(path)]
        print('stationID')
        print(list(df['stationId']))
        print('PATH')
        print(path)

        fig, ax = plt.subplots(figsize=(10, 10))

        grey_station = list(df['stationId'])
        grey_station = [x for x in grey_station if x not in path]
        grey_station_df = df[df['stationId'].isin(grey_station)]

        sns.scatterplot(grey_station_df, x='geoLng', y='geoLat',
                        color='whitesmoke')

        df['lineNameEng']['CEN'] = "Sukhumvit Line"

        for count, line in enumerate(self.all_line):
            new_df = df[
                (df['lineNameEng'] == line) & (df['stationId'].isin(path))]
            sns.scatterplot(new_df, x='geoLng', y='geoLat',
                            color=self.colors[count])

            for index, row in new_df.iterrows():
                plt.annotate(row['nameEng'], (row['geoLng'], row['geoLat']),
                             rotation=15)  # Adjust rotation as needed

        self.map.get_tk_widget().destroy()
        self.map = FigureCanvasTkAgg(fig, master=self.map_frame)
        self.map.draw()
        self.map.get_tk_widget().pack(side=tk.TOP)

    def run(self):
        self.mainloop()
