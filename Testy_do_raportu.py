import Graf
import Krzyzowanie as Krz
import ABC_step_1 as Abc
import Paczka_Paczkomat as PP
from matplotlib import pyplot as plt


def MapaTestowa(wymiar:int):
    Mapa = Graf.MapaPolaczen()

    names = []
    for i in range(wymiar+1):
        aa = chr(97 + int(i / 26)) + chr(97 + i % 26)
        names.append(aa)
    ListaAdresow = []
    for i in range(len(names)):
        ListaAdresow.append(PP.Paczkomat(f'{names[i]}'))

    for i in ListaAdresow:
        Mapa.InsertPaczkomat(i)
    visited = []
    for i_idx, i in enumerate(ListaAdresow):
        visited.append(i)
        for j_idx, j in enumerate(ListaAdresow):
            if j not in visited:
                r = 1000
                if i_idx + 1 == j_idx:
                    r = 0
                Mapa.InsertEdges(i, j, r)
                Mapa.InsertEdges(j, i, r)

    return Mapa, ListaAdresow


liczba_paczek = 15

trial = 10
MaxIteracje = 1000

Graf_testowy10, ListaAdresow10 = MapaTestowa(10)
print(Graf_testowy10)
Kurier10 = PP.Kurier()
PP.random_paczka(Kurier10, ListaAdresow10, liczba_paczek, Graf_testowy10)

liczebnosc_populacji = 10


for licz in range(4):
    liczebnosc_populacji = 10**(licz+1)
    print('\n\n\n\n\n Test liczebności populacji dla wartości ', f'{liczebnosc_populacji}:\n')
    populacja_start = Krz.populacja_start(liczebnosc_populacji, Graf_testowy10)
    for i in range(10):
        best_sol = Abc.Algorytm_ABC(populacja_start, 600, trial, MaxIteracje, Graf_testowy10, Kurier10)
        print('Wynik ', f'{i}:')
        idx = [i for i in range(len(best_sol[0]))]
        plt.plot(idx, best_sol[0])
        plt.scatter(best_sol[1][2], best_sol[1][1])
        plt.title(f'Zbieżność test {i} dla liczebności populacji równej {liczebnosc_populacji} ')
        plt.show()
        Krz.PrintPath(best_sol[1][0])
        print(f'Maksymalny znaleziony zysk: ', best_sol[1][1])
        print(f'Optymalna ścieżka:')
        Krz.PrintPath(ListaAdresow10)
        print(f'Optymalny zysk ze znanego rozwiązania: ',Abc.zysk_z_drogi(600,ListaAdresow10,Graf_testowy10,Kurier10))






Graf_testowy100, ListaAdresow100 = MapaTestowa(100)

Graf_testowy1000, ListaAdresow1000 = MapaTestowa(1000)
print(Graf_testowy10)
'''
Wpływ na kod:
    -ilość paczek
    - rozmiar populacji
    - liczba iteracji
    - typ krzyżowania
    - liczba traili
    
Sprawdzane właściwości:
    - poprawność wyniku
    - zbieżność w której iteracji
    - czas trwania kodu
    -
'''
