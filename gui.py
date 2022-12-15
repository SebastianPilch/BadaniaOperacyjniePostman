import random
import Graf
import Paczka_Paczkomat as PP
from matplotlib import pyplot as plt
import PySimpleGUI as sg
import io
import os
from PIL import Image,ImageTk

sg.theme('DarkBrown4')
im = Image.open("img/kurier.png")
size = (320, 400)
im = im.resize(size, resample=Image.BICUBIC)
im.save(r'img/kurier.png')

layout = [  [sg.Text("Podaj liczbę paczek UwU")],
            [sg.Text('(づ๑•ᴗ•๑)づ♡')],
            [sg.Input()],
            [sg.Text('Podaj listę paczomatów')],
            [sg.Input()],
            [sg.Image(size=size, key='-IMAGE-')],
            [sg.Button('Ok'),sg.Button('Exit')] ]

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
    # zysk_calkowity = poprzedni.bilans()

    for i in range(len(path) - 1):

        for edge in Mapa.Dict_[poprzedni]:
            if edge.Paczkomat_in_ == kolejny and edge.Paczkomat_out_ == poprzedni:
                print(edge)
                czas_drogi += edge.time_
                if i < len(path) - 2:
                    poprzedni = path[1 + i]
                    kolejny = path[2 + i]

                # if czas_drogi <= limit_czasu:
                # zysk_calkowity += edge.Paczkomat_in_.bilans()
    return czas_drogi


def UtworzMape(ListaAdresow):
    """ Utworzenie grafu """
    Mapa = Graf.MapaPolaczen()
    for i in ListaAdresow:
        Mapa.InsertPaczkomat(i)
    visited = []
    for i in ListaAdresow:
        visited.append(i)
        for j in ListaAdresow:
            if i != j and j not in visited:
                r = random.randint(9, 60)
                Mapa.InsertEdges(i, j, r)
                Mapa.InsertEdges(j, i, r)
    return Mapa

while True:
    if __name__ == '__main__':
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        l_paczek = int(values[0])
        Kurier = PP.Kurier()
        names = values[1].split(',')
        print(names)
        key_lst = [0]
        Paczkomat_lst = []
        for i in range(len(names)):
            Paczkomat_lst.append(PP.Paczkomat(f'{names[i]}'))

        Mapa = UtworzMape(Paczkomat_lst)
        print(Mapa)

        pop = populacja_start(len(names))
        for i in range(len(pop)):
            str_ = ''
            for j in range(len(pop[i])):
                if j < len(pop[i])-1:
                    str_ += " " + str(pop[i][j]) + " -> "
                else:
                    str_ += " " + str(pop[i][j])
            print(f"Osobnik {i + 1} : " + str_)


        print(zysk_z_drogi(30, pop[1]),'\n\n')

        PP.random_paczka(Kurier, Paczkomat_lst, l_paczek, Mapa)
        for i in Paczkomat_lst:
            i.Print_zawartosc()
        print(Kurier)

        t = [0 + i for i in range(0,600)]
        z1 = [PP.Funkcja_zysk_szybka(12,i) for i in t]
        z2 = [PP.Funkcja_zysk_priorytet(12,i) for i in t]
        z3 = [PP.Funkcja_zysk_Normalna(12,i) for i in t]
        z4 = [PP.Funkcja_zysk_Dlugi_czas(12,i) for i in t]
        plt.plot(t, z1)
        plt.plot(t, z2)
        plt.plot(t, z3)
        plt.plot(t, z4)

        plt.show()
window.close()
