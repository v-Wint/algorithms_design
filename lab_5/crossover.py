import random as rand
from individual import Individual


def even(a, b):
    chromosome = []
    a, b = a.chromosome, b.chromosome
    for x, y in zip(a, b):
        chromosome += rand.choice([x, y]),
    return Individual(chromosome)


def one_point(a, b):
    a, b = a.chromosome, b.chromosome
    point = rand.randint(0, len(a)-1)
    return Individual(a[:point+1] + b[point+1:])


def two_point(a, b):
    a, b = a.chromosome, b.chromosome
    point1 = rand.randint(0, len(a)//2)
    point2 = rand.randint(point1, len(b) - 1)
    return Individual(a[:point1 + 1] + b[point1 + 1:point2+1] + a[point2+1:])
