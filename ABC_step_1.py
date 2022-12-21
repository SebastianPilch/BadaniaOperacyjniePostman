

from random import randint
import random
from copy import deepcopy as dp
import Krzyzowanie as Krz
import main

def funkcja_fit(wartosc_f_celu):
    if wartosc_f_celu >= 0:
        return 1/(1+wartosc_f_celu)
    else:
        return 1 + abs(wartosc_f_celu)

def EmployedBee(original_food_source, f_celu, fit, limit, Maximize, Minimize, trial):
    food_source = dp(original_food_source)
    for przodek1_idx,przodek1 in enumerate(food_source):

        przodek2_idx = randint(0, len(food_source)-1)
        if przodek1_idx == przodek2_idx:
            if przodek2_idx != len(food_source)-1:
                przodek2_idx +=1
            else:
                przodek2_idx -=1

        potomek = Krz.Krzyzowanie(przodek1, original_food_source[przodek2_idx])
        potomek_max = f_celu(limit, potomek)
        potomek_min = fit(potomek_max)
        if potomek_min > Minimize[przodek1_idx]:
            trial[przodek1_idx] += 1
        else:
            food_source[przodek1_idx] = potomek
            Maximize[przodek1_idx] = potomek_max
            Minimize[przodek1_idx] = potomek_min
            trial[przodek1_idx] = 0
    return food_source, Maximize, Minimize, trial


def OnlookerdBee(original_food_source, f_celu, fit, Maximize, Minimize, trial, limit):
    food_source = dp(original_food_source)
    bees_numebr = 0
    probabilities = [i/sum(Minimize) for i in Minimize]
    current_max = 0
    current_max_idx = 0
    while bees_numebr != len(original_food_source):
        for bee_idx, bee in enumerate(food_source):
            r = random.random()
            if r < probabilities[bee_idx]:

                przodek2_idx = randint(0, len(food_source) - 1)
                if bee_idx == przodek2_idx:
                    if przodek2_idx != len(food_source) - 1:
                        przodek2_idx += 1
                    else:
                        przodek2_idx -= 1

                    potomek = Krz.Krzyzowanie(bee, original_food_source[przodek2_idx])
                    potomek_max = f_celu(limit, potomek)
                    potomek_min = fit(potomek_max)
                    if potomek_min > Minimize[bee_idx]:
                        trial[bee_idx] += 1
                    else:
                        food_source[bee_idx] = potomek
                        Maximize[bee_idx] = potomek_max
                        Minimize[bee_idx] = potomek_min
                        trial[bee_idx] = 0
                    if current_max < Maximize[bee_idx]:
                        current_max = Maximize[bee_idx]
                        current_max_idx = bee_idx
                    bees_numebr += 1
            if bees_numebr == len(original_food_source):
                break
    return food_source, Maximize, Minimize, trial, current_max_idx


def Scout_bee(original_food_source, f_celu, fit, Maximize, Minimize, trial, time_limit, scout_limit,Graf, max_idx):
    food_source = dp(original_food_source)
    for bee_idx, bee in enumerate(food_source):
        if trial[bee_idx] > scout_limit and bee_idx != max_idx:
            new_solution = Krz.losowa_sciezka(Graf)
            food_source[bee_idx] = new_solution
            new_max = f_celu(time_limit, new_solution)
            Maximize[bee_idx] = new_max
            Minimize[bee_idx] = fit(new_max)
            trial[bee_idx] = 0

    return food_source, Maximize, Minimize, trial


def Algorytm_ABC(original_food_source, f_celu, fit, time_limit, scout_limit, MaxIteracje, Graf):
    Maximize = [f_celu(time_limit, i) for i in original_food_source]
    Minimize = [fit(i) for i in Maximize]
    trial = [0 for i in original_food_source]
    current_best = (0, 0, 0)
    iter = 0
    best_sol = []
    while iter < MaxIteracje:
        food_source_phaseEB, Maximize_phase_EB, Minimize_phase_EB, trial_phase_EB = EmployedBee(original_food_source, f_celu, fit, time_limit, Maximize, Minimize, trial)
        food_source_phaseOlB, Maximize_phase_OlB, Minimize_phase_OlB, trial_phase_OlB, max_idx= OnlookerdBee(food_source_phaseEB, f_celu, fit, Maximize_phase_EB, Minimize_phase_EB, trial_phase_EB, time_limit)
        if current_best[1] < Maximize_phase_OlB[max_idx]:
            current_best = food_source_phaseOlB[max_idx], Maximize_phase_OlB[max_idx], iter
        original_food_source, Maximize, Minimize, trial = Scout_bee(food_source_phaseOlB, f_celu, fit, Maximize_phase_OlB, Minimize_phase_OlB, trial_phase_OlB, time_limit, scout_limit, Graf, max_idx)
        #
        iter += 1
        best_sol.append(current_best[1])
    return best_sol, current_best