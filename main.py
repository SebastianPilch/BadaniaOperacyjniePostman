import random
from typing import List

import Graf
import Paczka_Paczkomat as PP
import Krzyzowanie as Krz
from matplotlib import pyplot as plt


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


def funkcja_fit(wartosc_f_celu):
    if wartosc_f_celu >= 0:
        return 1/(1+wartosc_f_celu)
    else:
        return 1 + abs(wartosc_f_celu)


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


def PrintPath(path):
        str_ = ''
        for i in range(len(path)):
            if i < len(path) - 1:
                str_ += " " + str(path[i]) + " -> "
            else:
                str_ += " " + str(path[i])
        print(str_)


def PrintPopulacja(pop):
    for path in pop:
        PrintPath(path)


def PrintAktualnyStan(kurir:PP.Kurier,Paczkomaty: List[PP.Paczkomat]):
    for i in Paczkomat_lst:
        i.Print_zawartosc()
    print(Kurier)



if __name__ == '__main__':
    Kurier = PP.Kurier()
    names = ['A', 'B', 'C', 'D', 'E']
    key_lst = [0]
    Paczkomat_lst = []
    for i in range(len(names)):
        Paczkomat_lst.append(PP.Paczkomat(f'{names[i]}'))

    Mapa = UtworzMape(Paczkomat_lst)
    print(Mapa)
    pop = populacja_start(len(names))
    PrintPopulacja(pop)

    PP.random_paczka(Kurier, Paczkomat_lst, 10, Mapa)
    print('\n\n', zysk_z_drogi(100, pop[1]), '\n\n')
    PrintAktualnyStan(Kurier, Paczkomat_lst)





