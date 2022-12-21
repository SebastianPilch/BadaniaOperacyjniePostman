import random
from typing import List

import Graf
import Paczka_Paczkomat as PP
import Krzyzowanie as Krz
from matplotlib import pyplot as plt
import ABC_step_1 as ABC

if __name__ == '__main__':

    Kurier = PP.Kurier()
    names = [chr(ord('A') + i) for i in range(12)]
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

    for i in range(10):
        best_sol = ABC.Algorytm_ABC(pop, 600, 3, 400, Mapa, Kurier)

        print('\n\n\n\n\nWynik ',f'{i}:\n')
        idx = [i for i in range(len(best_sol[0]))]
        plt.plot(idx, best_sol[0])
        plt.scatter(best_sol[1][2], best_sol[1][1])
        plt.show()
        Krz.PrintPath(best_sol[1][0])
        print(f'\nMaksymalny znaleziony zysk: ', best_sol[1][1])
