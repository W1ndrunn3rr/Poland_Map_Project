from tkinter import *
from tkinter import ttk
import tkintermapview
from PIL import Image, ImageTk
from unidecode import unidecode



class GUI:
    """
    @brief Klasa GUI reprezentuje interfejs użytkownika.
    """

    def __init__(self, graph):
        """
        @brief Inicjalizuje obiekt GUI.

        @args:
        - graph (object): Obiekt reprezentujący graf.
        """
        self.city_list = graph.get_cities()
        self.root = Tk()
        self.graph = graph
        map_label = LabelFrame(self.root, width=15, height=5)
        self.map = tkintermapview.TkinterMapView(
            map_label, width=400, height=400, corner_radius=10
        )

        # Tworzenie etykiety i pól tekstowych
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
        self.road_var.set("LENGTH")
        self.LENGTH_button = Checkbutton(
            self.root,
            text="Najkrótsza trasa",
            variable=self.road_var,
            onvalue="LENGTH",
            offvalue="TIME",
        )
        self.LENGTH_button.place(x=475, y=200)

        self.TIME_button = Checkbutton(
            self.root,
            text="Najszybsza trasa",
            variable=self.road_var,
            onvalue="TIME",
            offvalue="LENGTH",
        )

        self.TIME_button.place(x=650, y=200)

        self.find_button.place(x=575, y=250)

        # Konfiguracja okna głównego
        self.root.title("Wyszukiwarka połączeń")
        self.root.geometry("800x480")
        self.root.resizable(False, False)

        # Ustawienie mapy
        map_label.place(x=40, y=40)
        self.map.set_position(51.9189046, 19.1343786)
        self.map.set_zoom(6)
        self.map.pack()

        self.path_var = StringVar()

    def main_loop(self):
        """
        @brief Uruchamia główną pętlę interfejsu użytkownika.
        """
        self.city_1_entry.bind('<Tab>', self.update_list_1)
        self.city_2_entry.bind('<Tab>', self.update_list_2)
        self.path_label = Label(
            self.root,
            textvar=self.path_var,
        )
        self.path_label.place(x=500, y=300)
        self.root.mainloop()
        

    def find_path(self):
        """
        @brief Wyszukuje trasę pomiędzy dwoma miastami i aktualizuje interfejs.
        """
        self.path_var.set("Brak miasta w bazie / trasa nie istnieje")
        self.map.delete_all_marker()
        path = self.map.set_path([(0, 0), (1, 1)])
        self.map.delete_all_path()
        try:
            time, distance, connections, cities = self.graph.a_star_algorithm(
                self.city_1_entry.get().strip(),
                self.city_2_entry.get().strip(),
                self.road_var.get(),
                self.h_var.get(),
            )
        except Exception:
            return

        self.path_var.set(
            f"Całkowity czas przejazdu : {time[0]}\nCałkowita droga: {distance} km"
        )
        self.map.set_position(
            (cities[0][0] + cities[-1][0]) / 2, (cities[0][1] + cities[-1][1]) / 2
        )
        cords = []
        for x, y, _ in cities:
            cords.append((x, y))

        self.map.set_path(cords, color="grey")

        for x, y, name in cities:
            self.map.set_marker(x, y, name, text_color="black")

        transparent_image = Image.new("RGBA", (1, 1), (255, 0, 0, 0))
        transparent_photo = ImageTk.PhotoImage(transparent_image)

        for i in range(len(cities) - 1):
            marker = self.map.set_marker(
                ((cities[i][0] + cities[i + 1][0]) / 2),
                ((cities[i][1] + cities[i + 1][1]) / 2),
                text=connections[i],
                icon=transparent_photo,
                text_color="dark magenta",
            )
            marker.hide_image(True)

    # Kod źródłowy, na którym się wzorowałem : https://www.geeksforgeeks.org/autocmplete-combobox-in-python-tkinter/
    def update_list_1(self,event):
        """
        @brief Aktualizuje listę miast w polu tekstowym 1.
        """
        current_text = unidecode(self.city_1_entry.get().lower())

        matching_cities = [city.name for city in self.city_list if unidecode(city.name.lower()).startswith(current_text)]


        if matching_cities:
            self.city_1_entry.delete(0, 'end')
            self.city_1_entry.insert(0, matching_cities[0])
            
    def update_list_2(self,event):
        """
        @brief Aktualizuje listę miast w polu tekstowym 2.
        """
        current_text = unidecode(self.city_2_entry.get().lower())
        
        matching_cities = [city.name for city in self.city_list if unidecode(city.name.lower()).startswith(current_text)]


        if matching_cities:
            self.city_2_entry.delete(0, 'end')
            self.city_2_entry.insert(0, matching_cities[0])


        return "break"