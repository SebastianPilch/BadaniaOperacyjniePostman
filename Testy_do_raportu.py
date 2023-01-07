import Graf
import Krzyzowanie as Krz
import ABC as Abc
import Paczka_Paczkomat as PP
from matplotlib import pyplot as plt
import time


def MapaTestowa(wymiar: int):
    Mapa = Graf.MapaPolaczen()

    names = []
    for i in range(wymiar + 1):
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
MaxIteracje = 800

Graf_testowy10, ListaAdresow10 = MapaTestowa(10)
print(Graf_testowy10)
Kurier10 = PP.Kurier()
PP.random_paczka(Kurier10, ListaAdresow10, liczba_paczek, Graf_testowy10)

liczebnosc_populacji = 40

for iter in range(1, 5):
    Trial = 10 * iter
    counting_time = []
    error = []
    print('\n\n\n\n\n Test liczba triali w scoucie: ', f'{Trial}:\n')
    populacja_start = Krz.populacja_start(liczebnosc_populacji, Graf_testowy10)
    w = open(f'Testy_trial/Test_trial_{Trial}.txt', 'wt')
    opt_wynik = Abc.zysk_z_drogi(600, ListaAdresow10, Graf_testowy10, Kurier10)
    for i in range(5):
        start_time = time.time()
        best_sol = Abc.Algorytm_ABC(populacja_start, 600, Trial, MaxIteracje, Graf_testowy10, Kurier10,
                                    cros_type='swap')
        counting_time.append(time.time() - start_time)

        w.write(f'\nWynik {i + 1}:\n')
        idx = [i for i in range(len(best_sol[0]))]
        plt.plot(idx, best_sol[0])
        plt.scatter(best_sol[1][2], best_sol[1][1], label='wykres zbieżności')
        plt.axhline(opt_wynik, color='red', label='Najlepszy wynik')
        plt.title(f'Zbieżność test {i + 1} dla Trial = {Trial} ')
        plt.xlabel('Numer iteracji')
        plt.ylabel('Maksymalny zysk po iteracji')
        plt.grid()
        plt.legend()
        plt.savefig(f'Testy_trial/Wykres_{i + 1}_trial_{Trial}.png')
        plt.show()

        find_path = Krz.PrintPath(best_sol[1][0])
        w.write(f'Najlepsza znaleziona sciezka:\n {find_path}\n')
        w.write(f'Maksymalny znaleziony zysk: {best_sol[1][1]}\n')
        error.append( opt_wynik - best_sol[1][1] )
        path_str = Krz.PrintPath(ListaAdresow10)
        w.write(f'Optymalna sciezka:\n {path_str}\n')
        w.write(f'Optymalny zysk ze znanego rozwiazania: {opt_wynik}')
        w.write('\n\n\n')
    w.write(
        f'sredni czas wykonania obliczen dla Trial = {Trial}:\n{sum(counting_time) / len(counting_time):.6f} s\n')
    w.write(f'sredni blad wyszukanych rozowiazan wynosi:\n {sum(error)/len(error)/opt_wynik*100:.2f} %\n')
    w.close()

# Graf_testowy100, ListaAdresow100 = MapaTestowa(100)
#
# Graf_testowy1000, ListaAdresow1000 = MapaTestowa(1000)
# print(Graf_testowy10)
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
