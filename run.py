# Created by nepes_standard at 11/03/19

from itertools import zip_longest
from math import exp, pi, sqrt
from random import uniform
from platypus import NSGAII, Problem, Real
import matplotlib.pyplot as plt
import numpy as np


def f1(x):
    """First function in the form of f(x),
    describing the discomfort of the user of the smart house in terms of percentage.
    :param x: room temperature
    :return: percentage of user discomfort (0% means maximum comfort)
    """
    SD = 6                          # standard deviation of the user comfort
    MEAN = 22                       # average room temperature
    SCALING_FACTOR = 15             # normalization of the function to the range from 0 to 1
    noise = uniform(-0.01, 0.01)
    gauss_pdf = 1 / sqrt(2 * pi * SD ** 2) * exp(-(x[0] - MEAN) ** 2 / (2 * SD ** 2)) + noise

    # Filter impossible values
    f = 0
    if gauss_pdf >= 0:
        f = gauss_pdf if gauss_pdf <= 1 else 1

    return 1 - SCALING_FACTOR * f   # invert and scale the function


def f2(x):
    """Second function in the form of f(x),
    describing the cost of the user of the smart house in terms of money spent on electricity.
    Taking into account some statistics, it is assumed that, on average, it is required to spend 60 euros per month
    to keep a room heated for 20 degrees Celsius.
    :param x: room temperature
    :return: electricity cost of maintaining given temperature
    """
    noise = uniform(-20, 20)
    y = 3 * x[0] + noise
    return y if x[0] > 0 and y > 0 else 0


def fs(x):
    """Wrapper of all objective functions
    :param x: input value for objective functions
    :return: list of solutions for objective functions
    """
    return [f1(x), f2(x)]


def main():
    """Main function of the program
    :return: void
    """

    DOMAIN = (15, 35)   # range of bearable room temperatures
    xs = np.linspace(DOMAIN[0], DOMAIN[1], num=(DOMAIN[1] - DOMAIN[0]))

    # Problem definition
    problem = Problem(1, 2)
    problem.types[:] = Real(DOMAIN[0], DOMAIN[1])
    problem.function = fs

    # Solutions for multi-objective problem
    algorithm = NSGAII(problem)
    algorithm.run(10000)

    # Print solutions
    print(" Obj1\t Obj2")
    for solution in algorithm.result[:5]:
        print("%0.3f\t%0.3f" % tuple(solution.objectives))

    # Labels for graph axes
    FX_LABEL = 'temperature'
    F1_LABEL = 'user discomfort'
    F2_LABEL = 'electricity cost'
    fs_labels = [F1_LABEL, F2_LABEL]

    # Solutions for each objective function
    fs_sols = []
    for x in xs:
        fs_sols.append(fs([x, 0]))
    fs_sols = [list(tup) for tup in zip_longest(*fs_sols, fillvalue="")]   # transpose the matrix of solutions

    # Display each objective function
    for i, f_sols in enumerate(fs_sols):
        plt.scatter(xs, f_sols)
        plt.xlabel(FX_LABEL)
        plt.ylabel(fs_labels[i])
        plt.show()

    # Display the Pareto frontier
    plt.scatter([s.objectives[0] for s in algorithm.result],
                [s.objectives[1] for s in algorithm.result])
    plt.xlabel(fs_labels[0])
    plt.ylabel(fs_labels[1])
    plt.show()


if __name__ == '__main__':
    main()
