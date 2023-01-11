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


liczba_paczek = 25

Graf_testowy10, ListaAdresow10 = MapaTestowa(10)
print(Graf_testowy10)
Kurier10 = PP.Kurier()
PP.random_paczka(Kurier10, ListaAdresow10, liczba_paczek, Graf_testowy10)

liczebnosc_populacji = 40
popul_testy = [10, 20, 30, 40, 50]
cross_type = 'swap'
cross_type_testy = ['Cross', 'swap']
MaxIteracje = 1000
iter_testy = [100, 500, 1000, 1500, 2000]
# iter_testy = [5, 10, 15, 20, 25]
trial = 10
trial_limit = [10, 20, 30, 40, 50]
liczba_prob = 5
opt_wynik = Abc.zysk_z_drogi(600, ListaAdresow10, Graf_testowy10, Kurier10)
populacja_start = Krz.populacja_start(liczebnosc_populacji, Graf_testowy10)

'''Testy Iteracji'''


fig_iter, iter_axs = plt.subplots(len(iter_testy), liczba_prob, figsize=(50, 50))
fig_iter.suptitle('Testy Iteracji przy Trial = 10, Liczebność populacji 10 i metodzie krzyżowania swap')
w = open(f'Testy_iteracje/Test_podsumowanie.txt', 'wt')

avg_error_it = []
avg_time_it = []
for idx, iter in enumerate(iter_testy):
    counting_time = []
    error = []
    print('\n\n\n\n\n Test liczba Iteracji: ', f'{iter}:\n')

    for i in range(liczba_prob):
        start_time = time.time()

        best_sol = Abc.Algorytm_ABC(populacja_start, 600, trial, iter, Graf_testowy10, Kurier10,
                                    cross_type='swap')
        counting_time.append(time.time() - start_time)

        '''Dokument tekstowy z podsumowaniem'''
        w.write(f'\nWynik {i + 1} dal liczby iteracji {iter}:\n')
        find_path = Krz.PrintPath(best_sol[1][0])
        w.write(f'Najlepsza znaleziona sciezka:\n {find_path}\n')
        w.write(f'Maksymalny znaleziony zysk: {best_sol[1][1]}\n')
        error.append(opt_wynik - best_sol[1][1])
        path_str = Krz.PrintPath(ListaAdresow10)
        w.write(f'Optymalna sciezka:\n {path_str}\n')
        w.write(f'Optymalny zysk ze znanego rozwiazania: {opt_wynik}')
        w.write('\n\n\n')

        '''Subplot '''
        plot_idx = [i + 1 for i in range(len(best_sol[0]))]
        iter_axs[idx, i].plot(plot_idx, best_sol[0], label='wykres zbieżności')
        iter_axs[idx, i].set_title(f'Zbieżność test {i + 1} dla Iteracji = {iter} ')
        iter_axs[idx, i].set_xlabel(f'numer iteracji')
        iter_axs[idx, i].set_ylabel(f'Największy znaleziony zysk')
        iter_axs[idx, i].axhline(opt_wynik, color='red', label='Najlepszy wynik')
        iter_axs[idx, i].grid()
        iter_axs[idx, i].legend()

    avg_time_it.append(round((sum(counting_time) / len(counting_time)), 6))
    avg_error_it.append(round((sum(error) / len(error) / opt_wynik * 100), 2))

tab, time_st, err = "{:>18}".format('|Liczba iteracji |'), "{:>18}".format('|    sredni czas |'), "{:>18}".format(
    '|    sredni blad |')
for idx, iter in enumerate(iter_testy):
    tab += "{:^20}".format(str(iter)) + '|'
    time_st += "{:^20}".format(str(avg_time_it[idx])) + '|'
    err += "{:^20}".format(str(avg_error_it[idx])) + '|'
tab += '\n'
time_st += '\n'
err += '\n'
table_frame = '-' * (25 + 20 * liczba_prob) + '\n'
w.write(table_frame)
w.write(tab)
w.write(table_frame)
w.write(time_st)
w.write(table_frame)
w.write(err)
w.write(table_frame)
w.close()
fig_iter.savefig(f'Testy_iteracje/Wykres_podsumowanie.png')

'''Testy Populacji'''

fig_pop, pop_axs = plt.subplots(len(iter_testy), liczba_prob, figsize=(50, 50))
fig_pop.suptitle('Testy Populacji przy Trial = 10, liczba iteracji 1000 i metodzie krzyżowania swap')
w = open(f'Testy_populacji/Test_podsumowanie.txt', 'wt')
avg_error_pop = []
avg_time_pop = []
for idx, pop in enumerate(popul_testy):
    populacja_start_test = Krz.populacja_start(pop, Graf_testowy10)
    counting_time = []
    error = []
    print('\n\n\n\n\n Test liczba Iteracji: ', f'{pop}:\n')

    for i in range(liczba_prob):
        start_time = time.time()

        best_sol = Abc.Algorytm_ABC(populacja_start_test, 600, trial, 1000, Graf_testowy10, Kurier10,
                                    cross_type='swap')
        counting_time.append(time.time() - start_time)

        '''Dokument tekstowy z podsumowaniem'''
        w.write(f'\nWynik {i + 1} dla populacji wielkości {pop}:\n')
        find_path = Krz.PrintPath(best_sol[1][0])
        w.write(f'Najlepsza znaleziona sciezka:\n {find_path}\n')
        w.write(f'Maksymalny znaleziony zysk: {best_sol[1][1]}\n')
        error.append(opt_wynik - best_sol[1][1])
        path_str = Krz.PrintPath(ListaAdresow10)
        w.write(f'Optymalna sciezka:\n {path_str}\n')
        w.write(f'Optymalny zysk ze znanego rozwiazania: {opt_wynik}')
        w.write('\n\n\n')

        '''Subplot '''
        plot_idx = [i + 1 for i in range(len(best_sol[0]))]
        pop_axs[idx, i].plot(plot_idx, best_sol[0], label='wykres zbieżności')
        pop_axs[idx, i].set_title(f'Zbieżność test {i + 1} dla populacji wielkości {pop} ')
        pop_axs[idx, i].set_xlabel(f'numer iteracji')
        pop_axs[idx, i].set_ylabel(f'Największy znaleziony zysk')
        pop_axs[idx, i].axhline(opt_wynik, color='red', label='Najlepszy wynik')
        pop_axs[idx, i].grid()
        pop_axs[idx, i].legend()

    avg_time_pop.append(round((sum(counting_time) / len(counting_time)), 6))
    avg_error_pop.append(round((sum(error) / len(error) / opt_wynik * 100), 2))

tab, time_st, err = "{:>20}".format('|Wielkosc populacji|'), "{:>20}".format('|    sredni czas |'), "{:>20}".format(
    '|    sredni blad |')
for idx, iter in enumerate(popul_testy):
    tab += "{:^20}".format(str(iter)) + '|'
    time_st += "{:^20}".format(str(avg_time_pop[idx])) + '|'
    err += "{:^20}".format(str(avg_error_pop[idx])) + '|'
tab += '\n'
time_st += '\n'
err += '\n'
table_frame = '-' * (25 + 20 * liczba_prob) + '\n'
w.write(table_frame)
w.write(tab)
w.write(table_frame)
w.write(time_st)
w.write(table_frame)
w.write(err)
w.write(table_frame)
w.close()
fig_pop.savefig(f'Testy_populacji/Wykres_podsumowanie.png')



'''Testy Crossa'''

fig_crs, crs_axs = plt.subplots(len(cross_type_testy)*2, liczba_prob, figsize=(50, 50))
fig_crs.suptitle('Testy Krzyżowania przy Trial = 10, liczba iteracji 1000 i populacji wielkości 40')
w = open(f'Testy_crossowanie/Test_podsumowanie.txt', 'wt')
avg_error_crs = []
avg_time_crs = []
for idx, crs in enumerate(cross_type_testy):
    counting_time = []
    error = []
    print('\n\n\n\n\n Test krzyżowanie: ', f'{crs}:\n')

    for i in range(liczba_prob * 2):
        j = 0 + idx
        if i >= 5:
            j = 1 + idx
        start_time = time.time()

        best_sol = Abc.Algorytm_ABC(populacja_start, 600, trial, 1000, Graf_testowy10, Kurier10,
                                    cross_type= crs)
        counting_time.append(time.time() - start_time)

        '''Dokument tekstowy z podsumowaniem'''
        w.write(f'\nWynik {i + 1} dla krzyżowania typu {crs}:\n')
        find_path = Krz.PrintPath(best_sol[1][0])
        w.write(f'Najlepsza znaleziona sciezka:\n {find_path}\n')
        w.write(f'Maksymalny znaleziony zysk: {best_sol[1][1]}\n')
        error.append(opt_wynik - best_sol[1][1])
        path_str = Krz.PrintPath(ListaAdresow10)
        w.write(f'Optymalna sciezka:\n {path_str}\n')
        w.write(f'Optymalny zysk ze znanego rozwiazania: {opt_wynik}')
        w.write('\n\n\n')

        '''Subplot '''
        plot_idx = [i + 1 for i in range(len(best_sol[0]))]
        crs_axs[idx + j, i % 5].plot(plot_idx, best_sol[0], label='wykres zbieżności')
        crs_axs[idx + j, i % 5].set_title(f'Zbieżność test {i + 1} dla Krzyżowania {crs} ')
        crs_axs[idx + j, i % 5].set_xlabel(f'numer iteracji')
        crs_axs[idx + j, i % 5].set_ylabel(f'Największy znaleziony zysk')
        crs_axs[idx + j, i % 5].axhline(opt_wynik, color='red', label='Najlepszy wynik')
        crs_axs[idx + j, i % 5].grid()
        crs_axs[idx + j, i % 5].legend()

    avg_time_crs.append(round((sum(counting_time) / len(counting_time)), 6))
    avg_error_crs.append(round((sum(error) / len(error) / opt_wynik * 100), 2))

tab, time_st, err = "{:>18}".format('|  Krzyzowanie   |'), "{:>18}".format('|    sredni czas |'), "{:>18}".format(
    '|    sredni blad |')
for idx, iter in enumerate(cross_type_testy):
    tab += "{:^20}".format(str(iter)) + '|'
    time_st += "{:^20}".format(str(avg_time_crs[idx])) + '|'
    err += "{:^20}".format(str(avg_error_crs[idx])) + '|'
tab += '\n'
time_st += '\n'
err += '\n'
table_frame = '-' * (25 + 20 * len(cross_type_testy)) + '\n'
w.write(table_frame)
w.write(tab)
w.write(table_frame)
w.write(time_st)
w.write(table_frame)
w.write(err)
w.write(table_frame)
w.close()
fig_crs.savefig(f'Testy_crossowanie/Wykres_podsumowanie.png')



'''Testy trial'''


fig_tr, tr_axs = plt.subplots(len(trial_limit), liczba_prob, figsize=(50, 50))
fig_tr.suptitle('Testy Trial przy liczbie iteracji 1000 i metodzie krzyżowania swap i populacji wielkości 40')
w = open(f'Testy_trial/Test_podsumowanie.txt', 'wt')
avg_error_tr = []
avg_time_tr = []
for idx, tr in enumerate(trial_limit):
    counting_time = []
    error = []
    print('\n\n\n\n\n Test liczba Triali: ', f'{tr}:\n')

    for i in range(liczba_prob):
        start_time = time.time()

        best_sol = Abc.Algorytm_ABC(populacja_start, 600,tr, 1000, Graf_testowy10, Kurier10,
                                    cross_type='swap')
        counting_time.append(time.time() - start_time)

        '''Dokument tekstowy z podsumowaniem'''
        w.write(f'\nWynik {i + 1} dla liczby triali {tr}:\n')
        find_path = Krz.PrintPath(best_sol[1][0])
        w.write(f'Najlepsza znaleziona sciezka:\n {find_path}\n')
        w.write(f'Maksymalny znaleziony zysk: {best_sol[1][1]}\n')
        error.append(opt_wynik - best_sol[1][1])
        path_str = Krz.PrintPath(ListaAdresow10)
        w.write(f'Optymalna sciezka:\n {path_str}\n')
        w.write(f'Optymalny zysk ze znanego rozwiazania: {opt_wynik}')
        w.write('\n\n\n')

        '''Subplot '''
        plot_idx = [i + 1 for i in range(len(best_sol[0]))]
        tr_axs[idx, i].plot(plot_idx, best_sol[0], label='wykres zbieżności')
        tr_axs[idx, i].set_title(f'Zbieżność test {i + 1} dla liczby triali {tr} ')
        tr_axs[idx, i].set_xlabel(f'numer iteracji')
        tr_axs[idx, i].set_ylabel(f'Największy znaleziony zysk')
        tr_axs[idx, i].axhline(opt_wynik, color='red', label='Najlepszy wynik')
        tr_axs[idx, i].grid()
        tr_axs[idx, i].legend()

    avg_time_tr.append(round((sum(counting_time) / len(counting_time)), 6))
    avg_error_tr.append(round((sum(error) / len(error) / opt_wynik * 100), 2))

tab, time_st, err = "{:>20}".format('|   Liczba triali |'), "{:>20}".format('|    sredni czas |'), "{:>20}".format(
    '|    sredni blad |')
for idx, iter in enumerate(trial_limit):
    tab += "{:^20}".format(str(iter)) + '|'
    time_st += "{:^20}".format(str(avg_time_tr[idx])) + '|'
    err += "{:^20}".format(str(avg_error_tr[idx])) + '|'
tab += '\n'
time_st += '\n'
err += '\n'
table_frame = '-' * (25 + 20 * liczba_prob) + '\n'
w.write(table_frame)
w.write(tab)
w.write(table_frame)
w.write(time_st)
w.write(table_frame)
w.write(err)
w.write(table_frame)
w.close()
fig_tr.savefig(f'Testy_trial/Wykres_podsumowanie.png')












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
