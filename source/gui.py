from os import stat
from sys import displayhook
from tkinter import *
from tkinter import ttk
from tkinter.font import BOLD
import tkintermapview
import math


class GUI:
    def __init__(self, graph):
        self.root = Tk()
        self.graph = graph
        map_label = LabelFrame(self.root, width=15, height=5)
        self.map = tkintermapview.TkinterMapView(
            map_label, width=400, height=400, corner_radius=10
        )

        label = Label(self.root, text="Wyszukaj trasę pomiędzy dwoma miastami")
        label.place(x=490, y=20)

        self.city_1_entry = Entry(self.root, width=30)
        self.city_1_entry.place(x=500, y=50)
        self.city_1_entry.insert(0, "Miasto początkowe")

        self.city_2_entry = Entry(self.root, width=30)
        self.city_2_entry.place(x=500, y=100)
        self.city_2_entry.insert(0, "Miasto docelowe")

        self.find_button = Button(
            self.root, text="Znajdź trasę", command=self.find_path
        )

        self.h_var = BooleanVar()
        self.highways_button = Checkbutton(
            self.root,
            text="Unikaj autostrad",
            variable=self.h_var,
            onvalue=True,
            offvalue=False,
        )
        self.highways_button.place(x=550, y=150)

        self.road_var = StringVar()
        self.shortest_button = Checkbutton(
            self.root,
            text="Najkrótsza trasa",
            variable=self.road_var,
            onvalue="shortest",
            offvalue="",
        )
        self.shortest_button.place(x=475, y=200)

        self.fastest_button = Checkbutton(
            self.root,
            text="Najszybsza trasa",
            variable=self.road_var,
            onvalue="fastest",
            offvalue="",
        )

        self.fastest_button.place(x=650, y=200)

        self.find_button.place(x=575, y=250)

        self.root.title("MAPA")
        self.root.geometry("800x480")
        self.root.resizable(False, False)

        map_label.place(x=40, y=40)
        self.map.set_position(51.9189046, 19.1343786)
        self.map.set_zoom(6)
        self.map.pack()

    def main_loop(self):
        self.root.mainloop()

    def find_path(self):
        self.map.delete_all_marker()
        marker = self.map.set_marker(0, 0, "a")
        path = self.map.set_path([(0, 0), (1, 1)])
        self.map.delete_all_path()
        time, distance, connections, cities = self.graph.a_star_algorithm(
            self.city_1_entry.get(),
            self.city_2_entry.get(),
            self.h_var.get(),
            self.road_var.get(),
        )

        if time is None:
            return  # raise error

        path_label = Label(
            self.root,
            text=f"Całkowity czas przejazdu : {time}\nCałkowita droga: {distance} km",
        )
        path_label.place(x=510, y=300)
        self.map.set_position(
            (cities[0][0] + cities[-1][0]) / 2, (cities[0][1] + cities[-1][1]) / 2
        )
        cords = []
        for x, y, _ in cities:
            cords.append((x, y))

        self.map.set_path(cords)

        for x, y, name in cities:
            self.map.set_marker(x, y, name)
