import sys
import numpy as np
from genetic_algorithm import Algorithm


def genetic_algorithm_test(modularity, disintegrate, file_name, population_number=100, probability_cross=0.0,
                           test_crossover_probability=True, iterations=100):
    if test_crossover_probability:
        for p_cross in np.arange(0, 1.05, 0.05):
            for p_mut in np.arange(0, 1.05, 0.05):
                algorithm = Algorithm(modularity, population_number, round(p_cross, 2), round(p_mut, 2), disintegrate)
                algorithm.run(iterations, file_name)
    else:
        for popul_number in range(2, 101, 2):
            for p_mut in np.arange(0, 1.05, 0.05):
                algorithm = Algorithm(modularity, popul_number, round(probability_cross, 2), round(p_mut, 2),
                                      disintegrate)
                algorithm.run(iterations, file_name)


if __name__ == '__main__':
    """
    Uruchamia testy z  możliwością ustawienie poniższych parametrów (niektóre są domyślne)
    Parametry uruchomienia:
    * modularność, 
    * dezagregacja zapotrzebowań (True/False)
    * nazwa pliku wyjściowego, 
    * liczebność populacji (domyślne 100), 
    * prawdopodobieństwo krzyżowania (domyślne 0),
    * wykonanie testu na prawdopodobieństwo krzyżowania (domyślnie True, w przypadku opcji False, 
        wykonanie testu na liczebność populacji
    * liczba iteracji (domyslne 100).
"""
    genetic_algorithm_test(sys.argv[0], sys.argv[1], sys.argv[2], population_number=int(sys.argv[3]),
                           probability_cross=int(sys.argv[4]), test_crossover_probability=bool(sys.argv[5]),
                           iterations=int(sys.argv[6]))
