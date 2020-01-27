import numpy as np
from genetic_algorithm import Algorithm
import argparse


def genetic_algorithm_test(modularity, disintegrate, file_name, population_number, probability_cross,
                           test_crossover_probability, iterations):
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


def add_argprase():
    praser = argparse.ArgumentParser()
    praser.add_argument('modularity', type=int, help='modularność krawędzi')
    praser.add_argument('demand_disaggregation', type=bool, help='dezagregacja zapotrzebowań')
    praser.add_argument('output_csv_file_name', type=str, help='nazwa pliku wyjściowego')
    praser.add_argument('--initial_population', type=int, help='liczebność populacji początkowej, domyślnie 15',
                        required=False, default=15)
    praser.add_argument('--cross_probability_test', type=bool, help='''wykonanie testu na prawdopodobieństwo 
                                                                  krzyżowania (domyślnie True,
                                                                   w przypadku opcji False,
                                                                    wykonanie testu na liczebność populacji, domyślnie True''',
                        required=False, default=True)

    praser.add_argument('--iterations_number', type=int, help='liczba iteracji, domyślnie 100', required=False,
                        default=100)
    praser.add_argument('--crossing_probability', type=float, help='prawdopodobieństwo krzyżowania, domyślnie 0.0',
                        required=False, default=0.0)

    return praser.parse_args()


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
        wykonanie testu na liczebność populacji)
    * liczba iteracji (domyslne 100).
"""

    args = add_argprase()
    genetic_algorithm_test(args.modularity, args.demand_disaggregation, args.output_csv_file_name,
                           args.initial_population, args.crossing_probability,
                           args.cross_probability_test,
                           args.iterations_number)
