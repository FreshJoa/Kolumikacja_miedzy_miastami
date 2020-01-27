Komunikacja między miastami

Sieć telekomunikacji między miastami można przedstawić jako graf nieskierowany, gdzie wierzchołkami są miasta, a krawędziami bezpośrednie kanały komunikacyjne między miastami. Dla każdych dwóch miast podane jest zapotrzebowanie, które musi być osiągalne do spełnienia w komunikacji między nimi (zbiór zapotrzebowań D). Wymaganie spełnienia zapotrzebowania dla pary miast można spełnić przez użycie kilku łączących je ścieżek; również jedna krawędź może brać udział w komunikacji między wieloma parami miast. Początkowo dowolna krawędź umożliwia spełnienie zapotrzebowania nie większego niż m. Zwiększenie tego limitu dla każdej pojedynczej krawędzi generuje koszt P. Należy znaleźć takie rozłożenie spełniania międzymiastowych zapotrzebowań na ścieżki w sieci, żeby liczba krawędzi wymagających zwiększenia limitu była jak najmniejsza.
Problem rozwiązany jest  dla sieci polskiej, z podanymi do wykorzystania ścieżkami między miastami.

Żeby znaleźć rozwiązanie minimalizujące koszty, posłużymy się algorytmem genetycznym.
Chromosom będzie zawierał przypisanie ułamka zapotrzebowania między każdą parą miast
do każdej ścieżki między nimi. Kolejność ścieżek dla pary miast jest w strukturze
chromosomu stała. Proponowane są dwa podejścia podziału zapotrzebowań.

1. Dezagregacja zapotrzebowań między parą miast na kilka ścieżek
2. Agregacja zapotrzebowań między parą miast na jedną ścieżkę.

Operatory genetyczne
Krzyżowanie
Zastosowane zostanie krzyżowanie wielopunktowe.


Krzyżowanie wielopunktowe będzie polegało na ustaleniu dla pary rodziców
prawdopodobieństwa p z jakim będą losowane geny z pierwszego rodzica. Brakujące geny
będą uzupełniane odpowiadającymi im genami drugiego rodzica. Dziecko będzie mieć
rozkład z około p*100% par miast od rodzica pierwszego i z (1-p)*100% od rodzica
drugiego.

Mutacja
Mutacja będzie zastąpieniem genu nowym – rozkład zapotrzebowań między jedną parą miast
w chromosomie zostanie wylosowany na nowo. Mutowanych w każdym obiegu pętli
algorytmu będzie M procent osobników.

Algorytm zawarty w pliku genetic_algorithm.py uruchamiać z następującymi parametrami :
* modularność,
* populacja początkowa,
* prawdopodobieństwo krzyżowania,
* prawdopodobieństwo mutacji,
* dezagregacja zapotrzebowań,
* liczba iteracji,
* nazwa pliku wyjściowego
    
Testy zawarte w pliku tests.py należy uruchomić w następujący sposób:
* modularność, 
* dezagregacja zapotrzebowań (True/False)
* nazwa pliku wyjściowego, 
* liczebność populacji (domyślne 100), 
* prawdopodobieństwo krzyżowania (domyślne 0),
* wykonanie testu na prawdopodobieństwo krzyżowania (domyślnie True, w przypadku opcji False, 
  wykonanie testu na liczebność populacji)
* liczba iteracji (domyslne 100).

