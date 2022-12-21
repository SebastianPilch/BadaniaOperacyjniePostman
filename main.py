import random
from typing import List

import Graf
import Paczka_Paczkomat as PP
import Krzyzowanie as Krz
from matplotlib import pyplot as plt
import ABC_step_1 as ABC

def zysk_z_drogi(limit_czasu, path):
        """
        funkcja obliczająca zysk wygenerowny przez ścieżkę
        funkcja jakości
        """
        czas_drogi = 0
        poprzedni = path[0]
        kolejny = path[1]
        zysk_calkowity = poprzedni.bilans(0)
        zysk_calkowity += Kurier.Dostarczenie(poprzedni, 0)
        for i in range(len(path) - 1):
            for edge in Mapa.Dict_[poprzedni]:
                if edge.Paczkomat_in_ == kolejny and edge.Paczkomat_out_ == poprzedni:
                    zysk_calkowity+= Kurier.Dostarczenie(edge.Paczkomat_in_,czas_drogi)
                    czas_drogi += edge.time_
                    if i < len(path) - 2:
                        poprzedni = path[1 + i]
                        kolejny = path[2 + i]
                    if czas_drogi <= limit_czasu:
                        zysk_calkowity += edge.Paczkomat_in_.bilans(czas_drogi)
        return zysk_calkowity


if __name__ == '__main__':
    Kurier = PP.Kurier()
    names = [chr(ord('A')+ i) for i in range(24)]
    key_lst = [0]
    Paczkomat_lst = []
    for i in range(len(names)):
        Paczkomat_lst.append(PP.Paczkomat(f'{names[i]}'))

    Mapa = Graf.UtworzMape(Paczkomat_lst, 9, 60)
    print(Mapa)
    pop = Krz.populacja_start(len(names), Mapa)
    Krz.PrintPopulacja(pop)

    PP.random_paczka(Kurier, Paczkomat_lst, 100, Mapa)
    Krz.PrintAktualnyStan(Kurier, Paczkomat_lst)

    best_sol = ABC.Algorytm_ABC(pop, zysk_z_drogi, ABC.funkcja_fit, 600, 3, 100, Mapa)
    idx = [i for i in range(len(best_sol[0]))]
    plt.plot(idx, best_sol[0])
    plt.scatter(best_sol[1][2], best_sol[1][1])
    plt.show()
    print(best_sol[1][0])

