# SPECYFIKACJA PROGRAMU

## OPIS PROGRAMU
Program służy do wyszukiwania najkrótszych lub najszybszych połączeń drogowych pomiędzy polskimi miastami, za pomocą algorytmu A* z funkcją heurystyczną haversine. Wyszukiwanie odbywa się w zakresie danych znajdujących się w folderze /data w pliku mapa_polski.json, ale jest możliwe także uruchomienie aplikacji, jeżeli plik jest w formacie JSON oraz posiada dokładnie taki sam układ.

Program realizuje obsługę interfejsową - prosty program napisany za pomocą modułu tkinter oraz modułu tkintermapview https://github.com/TomSchimansky/TkinterMapView.

A także realizuje obsługę bez interfejsu w terminalu.

## WYMAGANIA
Projekt wymaga Pythona w wersji 3.9 lub wyższej oraz mieć poprawnie skonfigurowany instalator paczek Pythona - pip oraz virtual venv, który jest domyślnie dołączany do Pythona. Jeśli jednak by go nie było należy go zainstalować : 
```bash
pip install virtualenv
```

## TWORZENIE ŚRODOWISKA WIRTUALNEGO
1.Aby uruchomić program należy stworzyć środowisko wirtualne Python venv https://docs.python.org/3/library/venv.html. Aby to zrobić należy być w folderze docelowym i wpisać w konsoli :

```bash
python -m venv .venv
```

Utworzy to w folderze docelowym wirtualne środowisko Pythona w folderze .venv.

2.Następnie należy aktywować środowisko w bashu :

```bash
source .venv/bin/activate
```

3.Teraz aby zainstalować potrzebne paczki projektowe należy uruchomić polecenie :

```bash
pip install -r requirements.txt
```

4.Środowisko jest gotowe; w celu jego opuszczenia należy wpisać w terminal :

```bash
deactivate
```

## URUCHOMIENIE PROGRAMU

W celu skorzystania z programu należy uruchomić skrypt main.py. Aby poprawnie wywołać skrypt z użyciem GUI, należy zastosować następującą składnię :

```bash
python3 main.py
```

Aby poprawnie wywołać skrypt z użyciem argumentów (bez GUI), należy zastosować następującą składnię :
```bash
python3 main.py town1 town2 [ (LENGTH|TIME) [maxclass [minclass]] ]
```

*town1 - identyfikator miasta 1 (np. name = Nowy Sącz -> id = NowySacz)

*town2 - identfikator miasta 2 ( wymagany przy podaniu town1 )

*(LENGTH|TIME) - wybór trybu algorytmu ;
LENGTH - algorytm optymalizuje długość drogi ; 
TIME - algorytm optymalizuje czas przejazdu drogi

*maxclass - maksymalna klasa drogi jaką algorytm bierze pod uwagę  (liczba nieujemna)

*minclass - minimalna klasa drogi jaką algorytm bierze pod uwagę (liczba nieujemna)


Oznaczenia klas dróg:

*5 - autostrada
*4 - droga szybkiego ruchu
*3 - droga krajowa
*2 - droga powiatowa
*1 - połączenie promowe
*0 - dowolna

W takim trybie w terminalu pojawi się wynik w postaci :

```
miasta_połączenia długość/czas ilość_odwiedzonych_węzłów 
```

Jeżeli połączenie nie zostanie znalezionie, albo miasta nie będzie w bazie to wtedy wterminalu pojawi się :

```
NOTFOUND ilość_odwiedzonych_węzłów 
```

Autor 
Jakub Gilewicz 275409

Województwa podkarpackie i lubelskie zostały stworzone przeze mnie.