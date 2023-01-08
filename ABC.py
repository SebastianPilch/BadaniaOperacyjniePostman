from random import randint
import random
from copy import deepcopy as dp
import Krzyzowanie as Krz
import main
import Graf
import Paczka_Paczkomat as PP


def zysk_z_drogi(limit_czasu, path, Mapa: Graf.MapaPolaczen, kurier: PP.Kurier):
    """
    funkcja obliczająca zysk wygenerowny przez ścieżkę
    funkcja jakości
    """
    czas_drogi = 0
    poprzedni = path[0]
    kolejny = path[1]
    zysk_calkowity = poprzedni.bilans(0)
    zysk_calkowity += kurier.Dostarczenie(poprzedni, 0)
    for i in range(len(path) - 1):
        for edge in Mapa.Dict_[poprzedni]:
            if edge.Paczkomat_in_ == kolejny and edge.Paczkomat_out_ == poprzedni:
                zysk_calkowity += kurier.Dostarczenie(edge.Paczkomat_in_, czas_drogi)
                czas_drogi += edge.time_
                if i < len(path) - 2:
                    poprzedni = path[1 + i]
                    kolejny = path[2 + i]
                if czas_drogi <= limit_czasu:
                    zysk_calkowity += edge.Paczkomat_in_.bilans(czas_drogi)
                else:
                    break
    return zysk_calkowity


def fit(wartosc_zysk_z_drogi):
    if wartosc_zysk_z_drogi >= 0:
        return 1 / (1 + wartosc_zysk_z_drogi)
    else:
        return 1 + abs(wartosc_zysk_z_drogi)


def EmployedBee(original_food_source, Maximize, Minimize, trial, limit, Mapa: Graf.MapaPolaczen, kurier: PP.Kurier,cross_type:str,f_celu=zysk_z_drogi,f_fit = fit):
    '''Krzyżowanie każdego osobnika przepisanie food source o ile uzyskamy lepszy rezultat'''
    food_source = dp(original_food_source)
    for przodek1_idx, przodek1 in enumerate(food_source):

        if cross_type == 'Cross':
            przodek2_idx = randint(0, len(food_source) - 1)
            if przodek1_idx == przodek2_idx:
                if przodek2_idx != len(food_source) - 1:
                    przodek2_idx += 1
                else:
                    przodek2_idx -= 1

            potomek = Krz.Cross(przodek1, original_food_source[przodek2_idx])

        if cross_type == 'swap':
            potomek = Krz.Swap(przodek1)

        potomek_max = f_celu(limit, potomek, Mapa, kurier)
        potomek_min = f_fit(potomek_max)
        if potomek_min > Minimize[przodek1_idx]:
            trial[przodek1_idx] += 1
        else:
            food_source[przodek1_idx] = potomek
            Maximize[przodek1_idx] = potomek_max
            Minimize[przodek1_idx] = potomek_min
            trial[przodek1_idx] = 0
    return food_source, Maximize, Minimize, trial


def OnlookerdBee(original_food_source, Maximize, Minimize, trial, limit, Mapa: Graf.MapaPolaczen, kurier: PP.Kurier,cross_type:str, f_celu = zysk_z_drogi, f_fit = fit):

    '''Faza krzyżowania na bazie prawdopodobieństwa, liczba krzyżowań musi być równa liczebności populacji,
     ale nie zawsze krzyżowane są wszystkie osobniki niektóre mogą być krzyżowane kilkukrotnie o ile mają
     wysoki wskaźnik prawdopodobieństwa'''
    food_source = dp(original_food_source)
    probabilities = [i / sum(Minimize) for i in Minimize]
    Onlooker_max = 0
    max_idx = 0
    for bee_idx, bee in enumerate(food_source):
        r = random.random()
        if r < probabilities[bee_idx]:

            if cross_type == 'Cross':
                przodek2_idx = randint(0, len(food_source) - 1)
                if bee_idx == przodek2_idx:
                    if przodek2_idx != len(food_source) - 1:
                        przodek2_idx += 1
                    else:
                        przodek2_idx -= 1
                potomek = Krz.Cross(bee, original_food_source[przodek2_idx])
            if cross_type == 'swap':
                potomek = Krz.Swap(bee)

            potomek_max = f_celu(limit, potomek, Mapa, kurier)
            potomek_min = f_fit(potomek_max)
            if potomek_min > Minimize[bee_idx]:
                trial[bee_idx] += 1
            else:
                food_source[bee_idx] = potomek
                Maximize[bee_idx] = potomek_max
                Minimize[bee_idx] = potomek_min
                trial[bee_idx] = 0
    for max_val_idx, max_val in enumerate(Maximize):
        if Onlooker_max < max_val:
            Onlooker_max = max_val
            max_idx = max_val_idx
    return food_source, Maximize, Minimize, trial, max_idx


def Scout_bee(original_food_source, Maximize, Minimize, trial, limit, scout_limit, max_idx, Mapa,
              kurier: PP.Kurier, f_celu = zysk_z_drogi, f_fit = fit, f_losujaca=Krz.losowa_sciezka):
    ''' Wymiana rozwiązań które nie poprawiły swojego wskaźnika jakości przez więcej niż scout_limit razy na nowe losowe'''
    food_source = dp(original_food_source)
    for bee_idx, bee in enumerate(food_source):
        if trial[bee_idx] > scout_limit and bee_idx != max_idx:
            new_solution = f_losujaca(Mapa)
            food_source[bee_idx] = new_solution
            new_max = f_celu(limit, new_solution, Mapa, kurier)
            Maximize[bee_idx] = new_max
            Minimize[bee_idx] = f_fit(new_max)
            trial[bee_idx] = 0

    return food_source, Maximize, Minimize, trial


def Algorytm_ABC(original_food_source, time_limit, scout_limit, MaxIteracje, Mapa: Graf.MapaPolaczen, kurier: PP.Kurier,cross_type:str="swap"):
    Maximize = [zysk_z_drogi(time_limit, i, Mapa, kurier) for i in original_food_source]
    Minimize = [fit(i) for i in Maximize]
    trial = [0 for i in original_food_source]
    current_best = (0, 0, 0)
    iter = 0
    best_sol = []
    while iter < MaxIteracje:
        '''Employee bee'''
        food_source_phaseEB, Maximize_phase_EB, Minimize_phase_EB, trial_phase_EB = EmployedBee(original_food_source, Maximize,
                                                                                                Minimize, trial,
                                                                                                time_limit, Mapa, kurier,cross_type)
        '''Onlooker bee'''
        food_source_phaseOlB, Maximize_phase_OlB, Minimize_phase_OlB, trial_phase_OlB, max_idx = OnlookerdBee(
            food_source_phaseEB, Maximize_phase_EB, Minimize_phase_EB, trial_phase_EB, time_limit, Mapa, kurier,cross_type)

        if current_best[1] < Maximize_phase_OlB[max_idx]:
            current_best = food_source_phaseOlB[max_idx], Maximize_phase_OlB[max_idx], iter
        '''Scout bee'''
        original_food_source, Maximize, Minimize, trial = Scout_bee(food_source_phaseOlB, Maximize_phase_OlB,
                                                                    Minimize_phase_OlB, trial_phase_OlB, time_limit, max_idx,
                                                                    scout_limit, Mapa, kurier)
        iter += 1
        best_sol.append(current_best[1])
    return best_sol, current_best
