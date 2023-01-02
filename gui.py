import random
import Graf
import Paczka_Paczkomat as PP
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import Krzyzowanie as Krz
import io
import os
from PIL import Image,ImageTk
import ABC_step_1 as ABC

sg.theme('DarkBrown4')
im = Image.open("img/kurier.png")
size = (320, 400)
im = im.resize(size, resample=Image.BICUBIC)
im.save(r'img/kurier.png')

layout_lst = [[sg.Text("Podaj liczbę paczek UwU")],
              [sg.Text('(づ๑•ᴗ•๑)づ♡')],
              [sg.Input(key='-INPUT_PACZKI-',do_not_clear=True)],
              [sg.Text('Liczba iteracji')],
              [sg.Input(key='-INPUT_ITERACJE-',do_not_clear=True)],
              [sg.Text('Limit w fazie scout')],
              [sg.Input(key='-INPUT_LIMIT_SCOUT-',do_not_clear=True)],
              [sg.Text('Limit czasowy')],
              [sg.Input(key='-INPUT_TIME-',do_not_clear=True)],
              [sg.Text('Podaj liste/liczbe paczkomatów',key='-TEXT_Paczkomat-')],
              [
                sg.Radio("Lista",'group 1',key='-RADIO1-',default=True),
                sg.Radio("Liczba","group 1",key='-RADIO2-')
              ],
              [sg.Input(key='-INPUT_Paczkomat-')],
              [sg.Text('Podaj sposób krzyżowania',key='-TEXT_Paczkomat-')],
              [
                sg.Radio("cross", 'group 2', key='-RADIO3-', default=True),
                sg.Radio("swap", "group 2", key='-RADIO4-')
              ],
              [sg.Text('',key='-ERROR-')],
              [sg.Button('Ok'),sg.Button('Exit')]]
layout_img= [
            [sg.Image(size=size, key='-IMAGE-')]]


layout_plot = [
    [sg.Canvas(key="-CANVAS-",size=(500,500))]
]
layout=[
    [
        sg.Column(layout_img),
        sg.VSeparator(),
        sg.Column(layout_lst),
        sg.VSeparator(),
        sg.Column(layout_plot),
    ]
]
window = sg.Window('Window Title', layout,margins=(0, 0), finalize=True)
image = ImageTk.PhotoImage(image=im)
window['-IMAGE-'].update(data=image)

def creat_plot(x,y):
    plt.plot(x,y)
    plt.grid('on')
    return plt.gcf()

def draw_figure(canvas,figure):
    figure_can = FigureCanvasTkAgg(figure,canvas)
    figure_can.draw()
    figure_can.get_tk_widget().pack(side='top',fill='both',expand=1)
    return figure_can

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
    Kurier.Dostarczenie(poprzedni,czas_drogi)
    zysk_calkowity = poprzedni.bilans(0)
    for i in range(len(path) - 1):
        for edge in Mapa.Dict_[poprzedni]:
            if edge.Paczkomat_in_ == kolejny and edge.Paczkomat_out_ == poprzedni:
                Kurier.Dostarczenie(edge.Paczkomat_in_,czas_drogi)
                czas_drogi += edge.time_
                if i < len(path) - 2:
                    poprzedni = path[1 + i]
                    kolejny = path[2 + i]
                if czas_drogi <= limit_czasu:
                    zysk_calkowity += edge.Paczkomat_in_.bilans(czas_drogi)
    return zysk_calkowity



2
while True:

        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        cros_type = 'Cross'
        if values['-RADIO4-'] is True:
            type = 'swap'
        Kurier = PP.Kurier()
        names = []
        if values['-RADIO1-'] == True:
            paczkomat = values['-INPUT_Paczkomat-']
            names = values['-INPUT_Paczkomat-'].split(',')
        elif values['-RADIO2-'] == True:
            paczkomat = values['-INPUT_Paczkomat-']
            names = []
            for i in range(int(values['-INPUT_Paczkomat-'])):
                aa = chr(97 + int(i / 26)) + chr(97 + i % 26)
                names.append(aa)
        key_lst = [0]
        Paczkomat_lst = []
        for i in range(len(names)):
            Paczkomat_lst.append(PP.Paczkomat(f'{names[i]}'))

        Mapa = Graf.UtworzMape(Paczkomat_lst, 9, 60)
        print(Mapa)
        pop = Krz.populacja_start(len(names), Mapa)
        Krz.PrintPopulacja(pop)

        PP.random_paczka(Kurier, Paczkomat_lst, 170, Mapa)
        Krz.PrintAktualnyStan(Kurier, Paczkomat_lst)

        for i in range(1):
            best_sol = ABC.Algorytm_ABC(pop, int(values['-INPUT_TIME-']), int(values['-INPUT_LIMIT_SCOUT-']), int(values['-INPUT_ITERACJE-']), Mapa, Kurier,cros_type)

            print('\n\n\n\n\nWynik ', f'{i}:\n')
            idx = [i for i in range(len(best_sol[0]))]
            # plt.plot(idx, best_sol[0])
            # plt.scatter(best_sol[1][2], best_sol[1][1])
            # plt.show()
            # Krz.PrintPath(best_sol[1][0])
            draw_figure(window["-CANVAS-"].TKCanvas,creat_plot(idx,best_sol[0]))
            print(f'\nMaksymalny znaleziony zysk: ', best_sol[1][1])

window.close()
