import Paczka_Paczkomat as PP
from typing import List


def Krzyzowanie(przodek_1: List[PP.Paczkomat], przodek_2: List[PP.Paczkomat]):

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

    return potomek