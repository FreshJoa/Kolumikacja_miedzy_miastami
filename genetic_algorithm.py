from collections import defaultdict
from itertools import repeat
import numpy as np
import random
import math
import sys
import csv


class Chromosome:
    """
      Klasa definiująca pojedynczy chromosom.
      :param cities_demand: słownik z listami zapotrzebowań (rozłożonymi na ścieżki) na każdą parę miast
      :param demand_edges_list: lista liczb kabli - liczba kabli, którą trzeba położyć na danej krawędzi, znajduje się na miejscu w liście odpowiadającym numerowi krawędzi
      :param cost: sumaryczna liczba kabli
      :param full_demand_by_pair: sumaryczne zapotrzebowanie dla pary miast
      :type cities_demand: dict
      :type demand_edges_list: list
      :type cost: int
      :type full_demand_by_pair: dict
      """

    def __init__(self):
        """
         Inicjuje pola klasy.
         """
        # słownik z listami zpotrzebowań(rozłożonymi na ścieżki) na każdą parę miast
        self.cities_demand = {}
        # lista ze stanem końcowym na krawędziach- 0 - nie przekroczyło przepustowości, 1, 2, 3... - znaczy tyle dodatkowo kabli trzeba położyć na krawędzi (mamy 18 krawędzi)
        self.demand_edges_list = list(repeat(0, 18))
        # cost - suma z demand_edges_list, czyli ilość kabli do położenia
        self.cost = 0
        # słownik: para miast - całość zapotrzebowania dla pary
        self.full_demand_by_pair = {}

    # funkacja wypełnia chromosom
    def fill_chromosome(self, demand_list, disintegrate=True):
        """
          Wypełnia rozkład zapotrzebowań na ścieżki (cities_demand) i przypisanie sumarycznego zapotrzebowania dla pary miast (full_demand_by_pair).
          :param demand_list: lista sumarycznych zapotrzebowań w kolejności odpowiadającej przyjętej kolejności par miast
          :param disintegrate: czy zapotrzebowanie dla każdej pary ma być rozłożone między ścieżkami, czy ma być wybrana jedna
          :type demand_list: list
          :type disintegrate: boolean
          """
        first_city = 0
        second_city = 1
        for demand in demand_list:
            if second_city > 11:
                first_city += 1
                second_city = first_city + 1
            self.cities_demand[f'demand_{first_city}_{second_city}'] = (
                self.get_demand_fractions_list(demand, disintegrate))
            # zamapiętaj w słowniku zapotrzebowanie dla pary miast
            self.full_demand_by_pair[f'demand_{first_city}_{second_city}'] = demand
            second_city += 1

        # print(self.cities_demand)
        # print(self.full_demand_by_pair)

    # funkcja zlicza koszt
    def count_cost(self, mapping, m):
        """
        Zlicza koszt realizacji sieci według danych w chromosomie (liczbę kabli).
        :param mapping: mapowanie krawędzi na ścieżki między miastami
        :param m: modularność krawędzi
        :type mapping: list
        :type m: int
        :return: sumaryczny koszt
        :rtype: int
        """

        for key, demand_parts_for_city in self.cities_demand.items():
            for path_number in range(0, 7):
                for edges_number in mapping[key][path_number]:
                    # obciążenie dodane do krawędzi =
                    # ułamek zapotrzebowania dla pary jaka przez nią idzie * całkowite obciążenie

                    # print(self.cities_demand[key][path_number])
                    # print(self.full_demand_by_pair[key])
                    # print(self.cities_demand[key][path_number] * self.full_demand_by_pair[key])

                    self.demand_edges_list[edges_number] += (
                            self.cities_demand[key][path_number] * self.full_demand_by_pair[key])

        self.demand_edges_list = [math.ceil(demand_edge / m) for demand_edge in self.demand_edges_list]
        self.cost = sum(self.demand_edges_list)

        return self.cost

    def crossover(self, parent_a, parent_b, crossover_probability):
        """
        Przeprowadza krzyżowanie wielopunktowe dwóch rodziców, których dzieckiem będzie dany chromosom. Wypełnia te same pola, co fill_chromosome.
        :param parent_a: rodzic
        :param parent_b: rodzic
        :type parent_a: Chromosome
        :type parent_b: Chromosome
        :param crossover_probability: prawdopodobieństwo krzyżowania
        :type crossover_probability: float
        """

        # gen to rozkład zapotrzebowania na ścieżki dla pary miast - element słownika cities_demand
        for gene_key, gene_val in parent_a.cities_demand.items():
            if np.random.random_sample() < crossover_probability:
                self.cities_demand[gene_key] = gene_val
            else:
                self.cities_demand[gene_key] = parent_b.cities_demand[gene_key]

        # liczone przy ocenianiu
        self.demand_edges_list = list(repeat(0, 18))

        # sumaryczne zapotrzebowanie dla pary się nie zmienia
        self.full_demand_by_pair = parent_a.full_demand_by_pair

    def mutation(self, mutation_probability, disintegrate=True):
        """
        Przeprowadza mutację. Zgodnie z prawdopodobieństwem mutacji dla każdego genu (rozkładu zapotrzebowań dla pary miast) zastępuje go nowym.
        :param mutation_probability: prawdopodobieństwo zastąpienia genu
        :param disintegrate: czy zapotrzebowanie dla każdej pary jest rozłożone między ścieżkami, czy jest wybrana jedna
        :param mutation_probability: float
        :param disintegrate: boolean
        """
        for gene_key, gene_val in self.cities_demand.items():
            if np.random.random_sample() < mutation_probability:
                self.cities_demand[gene_key] = (
                    self.get_demand_fractions_list(self.full_demand_by_pair[gene_key], disintegrate))

    # parametr disintegrate określa - Dezagregacja zapotrzebowań pary miast na ścieżki = True
    #                               - Agregacja zapotrzebowań pary miast na ścieżkę = False
    def get_demand_fractions_list(self, city_demand, disintegrate):
        """
        Zależnie od wartości parametru disintegrate:
        * True - rozlosowuje między ścieżkami dla zadanej pary miast, jaki ułamek zapotrzebowania mają spełniać
        * False - losuje, która ścieżka ma spełniać zapotrzebowanie
        :param city_demand: para miast, dla której ma być określony rozkład zapotrzebowania na ścieżki
        :param disintegrate: określa tryb działania
        :type city_demand:
        :type disintegrate:
        :return: rozkład zapotrzebowania na ścieżki
        :rtype: array
        """

        # część zapotrzebowania jako ułamek

        if disintegrate:
            points_of_division = np.random.random(6)
            points_of_division.sort()
            demand_fractions_list = [points_of_division[0]]
            for i in range(1, 6):
                demand_fractions_list.append(points_of_division[i] - points_of_division[i - 1])
            demand_fractions_list.append(1 - points_of_division[5])

            return demand_fractions_list

        else:
            path_number = random.randint(0, 6)
            demand_fractions_list = np.zeros(7)
            demand_fractions_list[path_number] = 1
            np.ndarray.tolist(demand_fractions_list)

        return demand_fractions_list


class Mapping:
    """
    Klasa zawierająca przyjęte numery ścieżek i mapowanie numerów krawędzi na ścieżki między parami miast.
    :param links_dict: mapowanie krawędzi na przyjęte numery krawędzi
    :type links_dict: dict
    :param demand_mapping: mapowanie numerów krawędzi na ścieżki między parami miast (słownik list)
    :type demand_mapping: dict
    """

    def __init__(self):
        """
        Przypisuje mapowania do zmiennych.
        """
        self.links_dict = {
            'Link_0_10': 0,
            'Link_0_2': 1,
            'Link_1_2': 2,
            'Link_1_7': 3,
            'Link_1_10': 4,
            'Link_2_9': 5,
            'Link_3_4': 6,
            'Link_3_6': 7,
            'Link_3_11': 8,
            'Link_4_8': 9,
            'Link_4_10': 10,
            'Link_5_8': 11,
            'Link_5_10': 12,
            'Link_6_10': 13,
            'Link_6_11': 14,
            'Link_7_9': 15,
            'Link_7_11': 16,
            'Link_0_5': 17
        }
        self.demand_mapping = defaultdict(list)
        self.fill_demand_mapping()

    def fill_demand_mapping(self):
        """
       Realizuje mapowanie numerów krawędzi na ścieżki między parami miast.
       """
        first_city = 0
        second_city = 1
        iterator = 0
        with open('mapping_links.txt', 'r') as reader_file:
            for line in reader_file:
                row = line.strip().split(' ')
                if iterator > 6:
                    if second_city == 11:
                        first_city += 1
                        second_city = first_city + 1
                    else:
                        second_city += 1
                    iterator = 0

                list_of_links = [self.links_dict.get(link) for link in row[2:len(row) - 1]]
                self.demand_mapping[f'demand_{first_city}_{second_city}'].append(list_of_links)
                iterator += 1
        # print(self.demand_mapping)


class Algorithm:
    """
    Klasa algorytmu genetycznego.
    :param modularity: przepustowość jednego kabla
    :type modularity: int
    :param population_number: początkowa liczność populacji
    :type population_number: int
    :param crossover_probability: prawdopodobieństwo krzyżowania
    :type crossover_probability: float
    :param mutation_probabilty: prawdopodobieństwo zastąpienia genu
    :type mutation_probabilty: float
    :param disintegrate: dezagregacja zapotrzebowań
    :type disintegrate: bool
    :param all_demand: sumaryczne zapotrzebowania dla kolejnych par miast
    :param all_demand: list
    :param mapping: mapowanie krawędzi na ścieżki między parami miast
    :type mapping: dict
    :param population: populacja - tablica chromosomów
    :type population: collections.iterable
    """

    def __init__(self, modularity, population_number, crossover_probability, mutation_probabilty, disintegrate=True):
        """
       Inicjuje pola klaasy.
       """
        self.modularity = modularity
        self.population_number = population_number
        self.crossover_probability = crossover_probability
        self.mutation_probabilty = mutation_probabilty

        # demand.txt - plik z zapotrzebowaniem na pary miast
        self.all_demand = np.genfromtxt('demand.txt', delimiter='\n')
        self.mapping = Mapping().demand_mapping

        # populacja początkowa
        self.population = []

        for _ in range(self.population_number):
            self.population.append(Chromosome())

        for chromosome in self.population:
            chromosome.fill_chromosome(self.all_demand, disintegrate)

        # jesli badamy liczebność populacji prawd_krzyzow = False

    def run(self, iterations, file_name):
        """
      Wykonuje algorytm przez zadaną liczbę iteracji.
      :param iterations: liczba iteracji algorytmu
      :type iterations: int
      :param file_name: nazwa pliku wyjściowego
      :type file_name: str
      """

        # przykład  - porównanie dwóch rodziców i ich dziecka

        # print(self.population[0].cities_demand)
        # print(self.population[1].cities_demand)
        # child = Chromosome()
        # child.crossover(self.population[0], self.population[1], self.crossover_probability)
        # child.mutation(self.mutation_probabilty)
        # print(child.cities_demand)

        with open(file_name, 'w') as write_file:
            csv_writer = csv.writer(write_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['liczebnosc_populacji', 'prawd_krzyz', 'prawd_mutacji', 'min_koszt'])

            iterator = 0
            stop_condition = 0
            last_best_cost = 0
            while iterator != iterations and stop_condition < 10:
                if iterator == 1:
                    last_best_cost = self.population[0].cost
                # tyle dzieci z krzyżowań ile osobników w populacji - populacja się podwaja

                children = []
                for _ in self.population:
                    parent_a = self.population[np.random.randint(self.population_number)]
                    parent_b = self.population[np.random.randint(self.population_number)]
                    child = Chromosome()
                    child.crossover(parent_a, parent_b, self.crossover_probability)
                    children.append(child)

                self.population = self.population + children

                # mutacja
                for p in self.population:
                    p.mutation(self.mutation_probabilty)

                # sortowanie od najlepiej do najgorzej przystosowanych
                self.population.sort(key=lambda p: p.count_cost(self.mapping, self.modularity), reverse=False)

                # przycięcie populacji do pierwotnego rozmiaru
                self.population = self.population[:self.population_number]

                if (last_best_cost < self.population[0].cost) and (iterator > 0):
                    stop_condition = stop_condition + 1
                else:
                    stop_condition = 0
                    last_best_cost = self.population[0].cost

                iterator = iterator + 1

            csv_writer.writerow(
                [self.population_number, self.crossover_probability, self.mutation_probabilty, last_best_cost])


if __name__ == '__main__':
    """
    Uruchamia algorytm z parametrami podanymi przy uruchomieniu programu lub z domyślnymi.
    Parametry uruchomienia:
    * modularność, 
    * populacja początkowa, 
    * prawdopodobieństwo krzyżowania, 
    * prawdopodobieństwo mutacji,
    * dezagregacja zapotrzebowań (domyślnie True),
    * liczba iteracji,
    * nazwa pliku wyjściowego
    """
    if len(sys.argv) > 1:
        algorithm = Algorithm(sys.argv[0], sys.argv[1], sys.argv[2], sys.argv[3], bool(sys.argv[4]))
        algorithm.run(sys.argv[5], sys.argv[6])
    else:
        algorithm = Algorithm(10, 10, 0.5, 0.4)
        algorithm.run(10, 'result.csv')
        algorithm = Algorithm(100, 10, 0.4, 0.0)
        algorithm.run(500, 'result.csv')
