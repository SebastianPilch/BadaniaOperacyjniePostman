import Graf
import Krzyzowanie
import ABC_step_1
import Paczka_Paczkomat as PP

def MapaTestowa(wymiar:int):
    Mapa = Graf.MapaPolaczen()

    names = []
    for i in range(wymiar+1):
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
                r = 100
                if i_idx + 1 == j_idx:
                    r = 1
                Mapa.InsertEdges(i, j, r)
                Mapa.InsertEdges(j, i, r)

    return Mapa

Graf_testowy = MapaTestowa(10)
print(Graf_testowy)