from typing import List
import random
import Graf
import copy
import math
from enum import Enum


def Funkcja_zysk_szybka(start_val,czas):
    return start_val * math.exp(-czas/275)


def Funkcja_zysk_priorytet(start_val,czas):
    return start_val * math.exp(-czas / 100)


def Funkcja_zysk_Normalna(start_val,czas):
    return start_val - (czas/70)


def Funkcja_zysk_Dlugi_czas(start_val,czas):
     return (start_val+1)- math.exp(czas/400)


class Paczka:
    def __init__(self, wartosc_poczatkowa, typ, key, adres_dostarczenia,dostarczenie: bool):
        self.key = key
        self.adres_dostarczenia = adres_dostarczenia
        self.dostarczenie = dostarczenie
        self.wartosc_poczatkowa = wartosc_poczatkowa
        self.typ = typ

        if typ == 1:
            self.fun = Funkcja_zysk_Dlugi_czas
        if typ == 2:
            self.fun = Funkcja_zysk_Normalna
        if typ == 3:
            self.fun = Funkcja_zysk_szybka
        if typ == 4:
            self.fun = Funkcja_zysk_priorytet

    def zysk(self):
        return self.wartosc_poczatkowa

    def strata(self, aktualny_czas):
        return self.wartosc_poczatkowa - self.bilans(aktualny_czas)

    def bilans(self, aktualny_czas):
        return self.fun(start_val=self.wartosc_poczatkowa, czas=aktualny_czas)

    def __str__(self):
        t_ = ''
        if self.typ == 1:
            t_ = 'Długi czas doręczenia'
        if self.typ == 2:
            t_ = "Normalna"
        if self.typ == 3:
            t_ = "Krótki czas doręczenia"
        if self.typ == 4:
            t_ = "Priorytetowa"

        if self.dostarczenie:
            return "[" + str(self.key) +',' +str(self.adres_dostarczenia) + "," + t_ + "]"
        else:
            return "[" + str(self.key) + ",Odbiór ," + t_ + "]"


def random_paczka(Kurier, Pacz_lst, liczba_iter, map: Graf.MapaPolaczen, key_Pacz_list: List[int] = [0]):

    for i in range(liczba_iter):
        Pacz_list = copy.copy(Pacz_lst)
        key = max(key_Pacz_list) + 1
        key_Pacz_list.append(key)
        adres_akt = random.choice(Pacz_list)
        index = Pacz_list.index(adres_akt)
        del Pacz_list[index]
        adres_dos = random.choice(Pacz_list)
        wartosc = random.randint(0, 480)
        typ = random.randint(1, 4)
        if key % 2 == 0:
            dostarczenie = True
            paczka_dod = Paczka(wartosc, typ, key, adres_dos, dostarczenie)
            Kurier.InsertPaczka(paczka_dod)
        else:
            dostarczenie = False
            paczka_dod = Paczka(wartosc, typ, key, adres_dos, dostarczenie)
            index = map.getPaczkomatIdx(adres_akt)
            paczko: Paczkomat = map.getPaczkomat(index)
            paczko.InsertPaczka(paczka_dod)

class Paczkomat:
    def __init__(self, adres):
        self.key_ = adres
        self.lista_odbior = []
        self.lista_dostarczenie = []

    def __eq__(self, other):
        if other is None:
            return False
        return True if self.key_ == other.key_ else False

    def __hash__(self):
        return hash(self.key_)

    def __str__(self):
        return self.key_

    def InsertPaczka(self, Paczka):
        if Paczka.dostarczenie:
            self.lista_dostarczenie.append(Paczka)
        else:
            self.lista_odbior.append(Paczka)

    def odbior_size(self):
        return len(self.lista_odbior)

    def dostarczenie_size(self):
        return len(self.lista_dostarczenie)

    def DeletePaczka(self, Paczka):
        for i in range(self.odbior_size()):
            if self.lista_odbior[i].key == Paczka.key:
                del self.lista_odbior[i]
        for i in range(self.dostarczenie_size()):
            if self.lista_dostarczenie[i].key == Paczka.key:
                del self.lista_dostarczenie[i]

    def zysk(self, time):
        suma_zysk = 0
        for i in range(self.odbior_size()):
            suma_zysk += self.lista_odbior[i].zysk()
        for i in range(self.dostarczenie_size()):
            suma_zysk += self.lista_dostarczenie[i].zysk()
        return suma_zysk

    def strata(self, time):
        suma_strat = 0
        for i in range(self.odbior_size()):
            suma_strat += self.lista_odbior[i].strata(time)
        for i in range(self.dostarczenie_size()):
            suma_strat += self.lista_dostarczenie[i].strata(time)
        return suma_strat

    def bilans(self, time):
        return self.zysk(time) - self.strata(time)

    def Print_zawartosc(self):
        str_ = str(self) + ":"
        for i in self.lista_odbior:
            str_ += " " + str(i) + " "
        for i in self.lista_dostarczenie:
            str_ += " " + str(i) + " "
        print(str_)

class Kurier:
    def __init__(self):
        self.Paczki = []

    def __str__(self):
        to_str = 'Kurier : '
        for i in range(len(self.Paczki)):
            to_str += f'[{self.Paczki[i].adres_dostarczenia} : {self.Paczki[i].key}]'
        return to_str

    def InsertPaczka(self, Paczka):
        self.Paczki.append(Paczka)

    def Dostarczenie(self, Paczkomat, czas):
        zysk_dostarczenie = 0
        for i in range(len(self.Paczki)):
            if Paczkomat == self.Paczki[i].adres_dostarczenia:
                zysk_dostarczenie += self.Paczki[i].bilans(aktualny_czas=czas)
        return zysk_dostarczenie


