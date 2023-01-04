import Paczka_Paczkomat as PP
from typing import List
import Graf
from copy import deepcopy as dp
from random import randint

""" Funkcję wypisujące populację oraz pojedynczego osobnika"""
def PrintPath(path):
    ''' Wypisanie pojedyńczego osobnika na konsolę'''
    str_ = ''
    for i in range(len(path)):
        if i < len(path) - 1:
            str_ += " " + str(path[i]) + " -> "
        else:
            str_ += " " + str(path[i])
    print(str_)
    return str_


def PrintPopulacja(pop):
    ''' Wypisanie populacji na konsolę'''
    for path in pop:
        PrintPath(path)


def PrintAktualnyStan(kurier: PP.Kurier, Paczkomaty: List[PP.Paczkomat]):
    ''' Wypisanie zwartości wszystkich paczkomatów i paczek u kuriera na konsolę'''
    for i in Paczkomaty:
        i.Print_zawartosc()
    print(kurier)


def losowa_sciezka(Mapa:Graf.MapaPolaczen):
    """
    losowanie ścieżki generowane
    losowo odwiedzające każdy paczkomat
    w grafie
    """
    wymiar = Mapa.order()
    indexes = [i for i in range(wymiar)]
    path = []
    while len(indexes) > len(path):
        idx = randint(0, wymiar - 1)
        if idx not in path:
            path.append(idx)
    for i in range(len(path)):
        path[i] = Mapa.getPaczkomat(path[i])
    return path


def populacja_start(liczebnosc: int, Mapa: Graf.MapaPolaczen):
    """
    wykorzystanie losowych ścieżek w celu złożenia
    początkowej populacji o liczebności podanej z zewnątrz
    """
    populacja = []
    for i in range(liczebnosc):
        populacja.append(losowa_sciezka(Mapa))
    return populacja



def Krzyzowanie(przodek_1: List[PP.Paczkomat], przodek_2: List[PP.Paczkomat]):
    ''' Funkcja krzyżująca dwie podanie ścieżki'''
    potomek: List[PP.Paczkomat] = [None for j in przodek_1]
    for i in range(len(przodek_1)// 2):
        potomek[i] = przodek_1[i]
    for j in range((len(przodek_1)// 2)):
        found_new_index = j
        found_new: PP.Paczkomat = przodek_1[j]
        first_new: PP.Paczkomat = przodek_2[j]
        while first_new not in potomek:
            for k in range(len(przodek_2)):
                if found_new == przodek_2[k]:
                    found_new_index = k
                    if potomek[found_new_index] is None:
                        potomek[found_new_index] = first_new
                        break
                    else:
                        found_new = przodek_1[k]
    for i in range(len(przodek_2)):
        if potomek[i] is None:
            potomek[i] = przodek_2[i]


def Swap(przodek):
    potomek = dp(przodek)
    swap_idx1, swap_idx2 = randint(0, len(przodek)-1), randint(0, len(przodek)-1)
    potomek[swap_idx1], potomek[swap_idx2] = potomek[swap_idx2], potomek[swap_idx1]
    return potomek