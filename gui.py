import random
import Graf
import Paczka_Paczkomat as PP
from matplotlib import pyplot as plt
import PySimpleGUI as sg
import Krzyzowanie as Krz
import io
import os
from PIL import Image,ImageTk

sg.theme('DarkBrown4')
im = Image.open("img/kurier.png")
size = (320, 400)
im = im.resize(size, resample=Image.BICUBIC)
im.save(r'img/kurier.png')

layout = [[sg.Text("Podaj liczbę paczek UwU")],
          [sg.Text('(づ๑•ᴗ•๑)づ♡')],
          [sg.Input()],
          [sg.Text('Podaj listę paczomatów')],
          [sg.Input()],
          [sg.Text('Liczba iteracji')],
          [sg.Input()],
          [sg.Text('Limit w fazie scout')],
          [sg.Input()],
          [sg.Image(size=size, key='-IMAGE-')],
          [sg.Button('Ok'),sg.Button('Exit')]]

window = sg.Window('Window Title', layout,margins=(0, 0), finalize=True)
image = ImageTk.PhotoImage(image=im)
window['-IMAGE-'].update(data=image)
def losowa_sciezka(wymiar: int):
    """
    losowanie ścieżki generowane
    losowo odwiedzające każdy paczkomat
    w grafie

    """
    indexes = [i for i in range(wymiar)]
    wybrane = 0
    path = []
    while len(indexes) > len(path):
        idx = random.randint(0, wymiar - 1)
        if idx not in path:
            path.append(idx)
    for i in range(len(path)):
        path[i] = Mapa.getPaczkomat(path[i])
    return path


def populacja_start(liczebnosc: int):
    """
    wykorzystanie losowych ścieżek w celu złożenia
    początkowej populacji o liczebności podanej z zewnątrz
    """
    populacja = []
    for i in range(liczebnosc):
        populacja.append(losowa_sciezka(Mapa.order()))
    return populacja


def zysk_z_drogi(limit_czasu, path):
    """
    funkcja obliczająca zysk wygenerowny przez ścieżkę
    funkcja jakości
    """
    czas_drogi = 0
    poprzedni = path[0]
    kolejny = path[1]
    Kurier.Dostarczenie(poprzedni)
    zysk_calkowity = poprzedni.bilans(0)
    for i in range(len(path) - 1):
        for edge in Mapa.Dict_[poprzedni]:
            if edge.Paczkomat_in_ == kolejny and edge.Paczkomat_out_ == poprzedni:
                Kurier.Dostarczenie(edge.Paczkomat_in_)
                czas_drogi += edge.time_
                if i < len(path) - 2:
                    poprzedni = path[1 + i]
                    kolejny = path[2 + i]
                if czas_drogi <= limit_czasu:
                    zysk_calkowity += edge.Paczkomat_in_.bilans(czas_drogi)
    return zysk_calkowity




while True:
    if __name__ == '__main__':
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        l_paczek = int(values[0])
        Kurier = PP.Kurier()
        names = values[1].split(',')
        key_lst = [0]
        Paczkomat_lst = [PP.Paczkomat(f'{names[i]}') for i in range(len(names))]
        Mapa = Graf.UtworzMape(Paczkomat_lst)
        print(Mapa)
        pop = populacja_start(len(names))
        Krz.PrintPopulacja(pop)
        PP.random_paczka(Kurier, Paczkomat_lst, l_paczek, Mapa)
        for i in Paczkomat_lst:
            i.Print_zawartosc()
        print(Kurier)


window.close()
