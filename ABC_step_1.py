

from random import randint
import random
from copy import deepcopy as dp
import Krzyzowanie as Krz


def EmployedBee(original_food_source, f_celu, fit, limit):
    food_source = dp(original_food_source)
    Maximize = [f_celu(limit, i) for i in food_source]
    Minimize = [fit(i) for i in Maximize]
    trial = [0 for i in food_source]

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


def OnlookerdBee(original_food_source, f_celu, fit, Maximize, Minimize, trial, limit):

    food_source = dp(original_food_source)
    bees_numebr = 0
    probabilities = [i/sum(Minimize) for i in Minimize]
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
                    bees_numebr += 1
            if bees_numebr == len(original_food_source):
                break

