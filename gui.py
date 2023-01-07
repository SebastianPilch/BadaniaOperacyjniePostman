import PySimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import Graf
import Paczka_Paczkomat as PP
import ABC as ABC
import Krzyzowanie as Krz
import time

_VARS = {'window': False,
         'fig_agg': False,
         'pltFig': False}

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

layout_lst = [[sg.Text("Podaj liczbę paczek UwU")],
              [sg.Text('(づ๑•ᴗ•๑)づ♡')],
              [sg.Input(key='-INPUT_PACZKI-',do_not_clear=True)],
              [sg.Text('Liczba iteracji')],
              [sg.Input(key='-INPUT_ITERACJE-',do_not_clear=True)],
              [sg.Text('Wielkość początkowej populcji')],
              [sg.Input(key="-INPUT_POPULATION-")],
              [sg.Text('Limit w fazie scout')],
              [sg.Input(key='-INPUT_LIMIT_SCOUT-',do_not_clear=True)],
              [sg.Text('Czas pracy kuriera')],
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


layout_plot = [[sg.Canvas(key='figCanvas')],
               [sg.Text("", key='-PATH-')],
               [sg.Text("", key='-GAIN-')],
               [sg.Text('',key='-TIME-')]
               ]

layout=[
    [
        sg.Column(layout_lst),
        sg.VSeparator(),
        sg.Column(layout_plot),
    ]
]
_VARS['window'] = sg.Window('Kurier APP 0.9',
                            layout,
                            finalize=True,
                            resizable=True,
                            location=(100, 100),
                            element_justification="center")

def drawChart():
    _VARS['pltFig'] = plt.figure()
    plt.plot(0,0)
    plt.grid('on')
    _VARS['fig_agg'] = draw_figure(_VARS['window']['figCanvas'].TKCanvas, _VARS['pltFig'])

def updateChart(x,y):
    _VARS['fig_agg'].get_tk_widget().forget()
    plt.clf()
    plt.plot(x, y)
    plt.grid('on')
    plt.xlabel('Iteracje')
    plt.ylabel('Zysk')
    plt.title('Funkcja zysku w kolejnych iteracjach')
    _VARS['fig_agg'] = draw_figure(_VARS['window']['figCanvas'].TKCanvas, _VARS['pltFig'])

def paczk_lst(lista,bol:bool):
    names = []
    if bol is True:
        names = lista.split(',')
    else:
        for i in range(int(values['-INPUT_Paczkomat-'])):
            aa = chr(97 + int(i / 26)) + chr(97 + i % 26)
            names.append(aa)
    return names


drawChart()

while True:
    event, values = _VARS['window'].read(timeout=200)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Ok':
        cros_type = 'Cross'
        if values['-RADIO4-'] is True:
            type = 'swap'
        Kurier = PP.Kurier()
        names = paczk_lst(values['-INPUT_Paczkomat-'], values['-RADIO1-'])
        key_lst = [0]
        Paczkomat_lst = []
        for i in range(len(names)):
            Paczkomat_lst.append(PP.Paczkomat(f'{names[i]}'))
        Mapa = Graf.UtworzMape(Paczkomat_lst, 9, 60)
        pop = Krz.populacja_start(int(values["-INPUT_POPULATION-"]), Mapa)
        Krz.PrintPopulacja(pop)
        PP.random_paczka(Kurier, Paczkomat_lst, int(values["-INPUT_PACZKI-"]), Mapa)
        Krz.PrintAktualnyStan(Kurier, Paczkomat_lst)
        start_time = time.time()
        best_sol = ABC.Algorytm_ABC(pop, int(values['-INPUT_TIME-']), int(values['-INPUT_LIMIT_SCOUT-']),
                                    int(values['-INPUT_ITERACJE-']), Mapa, Kurier, cros_type)
        time_test = (time.time() - start_time)
        idx = [i for i in range(len(best_sol[0]))]
        aa = Krz.PrintPath(best_sol[1][0])
        _VARS['window']['-PATH-'].update("Najlepsza ścieżka: " + aa)
        _VARS['window']['-GAIN-'].update("Największy zysk: " + str(best_sol[1][1]))
        _VARS['window']['-TIME-'].update("Czas pracy alogorytmu: " + str(time_test))
        updateChart(idx,best_sol[0])
_VARS['window'].close()