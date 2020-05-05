from typing import Union

import numpy as np
from numpy.random import default_rng
import math


def comb(n, m):
    if n < m:
        return 0
    else:
        return math.factorial(n) / (math.factorial(m) * math.factorial(n - m))


class Hyperopinion:
    W = 2

    def set_to_index(self, composite: set) -> int:
        ceil = 0
        for i in range(1, len(composite) + 1):
            ceil += comb(self.k, i)

        left = len(composite)
        for element in composite:
            pos_elem = self.k - element - 1
            ceil -= comb(pos_elem, left)
            left -= 1

        return int(ceil - 1)

    def index_to_set(self, index):
        index += 1
        composite = []
        n_elem = 1
        while True:
            aux = comb(self.k, n_elem)
            if aux < index:
                index -= aux
                n_elem += 1
            else:
                break

        pos_choosing = 0
        while len(composite) < n_elem:
            aux = comb(self.k - pos_choosing - 1, n_elem - len(composite) - 1)

            if n_elem - len(composite) == 1:
                composite.append(int(pos_choosing + index - 1))
            elif aux < index:
                index -= aux
                pos_choosing += 1
            else:
                composite.append(pos_choosing)
                pos_choosing += 1
        return set(composite)

    @staticmethod
    def generate_random_belief(k, a=None):
        rng = default_rng()
        l = np.array([rng.random() for i in range(2 ** k - 1)])
        l = l / np.sum(l)
        return Hyperopinion(k, l[0:-1], a)

    def __calculate_a(self, a_size_k):
        self.a = np.zeros(self.kappa)
        for x in range(self.kappa):
            setx = self.index_to_set(x)
            for index_from_set in setx:
                self.a[x] += a_size_k[index_from_set]

    def relative_a(self, x: Union[int, set], xi: Union[int, set]):
        if isinstance(x, int):
            x = self.index_to_set(x)
        if isinstance(xi, int):
            xi = self.index_to_set(xi)
        if x.intersection(xi) == set():
            return 0
        return self.a[self.set_to_index(x.intersection(xi))] / self.a[self.set_to_index(xi)]

    def __calculate_P(self):
        self.P = np.zeros(self.k)
        for x in range(self.k):
            for xi in range(self.kappa):
                self.P[x] += self.relative_a(x, xi) * self.b[xi]
            self.P[x] += self.a[x] * self.u

    def __init__(self, k, b, a=None):
        self.k = k
        self.kappa = 2 ** self.k - 2
        self.b = np.array(b)
        if self.kappa != len(self.b):
            raise Exception('Size of belief mass distribution and size of domain (k) are not compatible.')
        if sum(self.b) > 1:
            raise Exception('Sum of belief mass distribution is greater than 1. It should be equal or less than 1.')
        self.u = 1 - np.sum(self.b)

        if a is None:
            a = np.array([1 / self.k for _ in range(self.k)])
        else:
            a = np.array(a)
        if np.sum(a) != 1:
            raise Exception('Sum of base rate distribution is not 1. It should be equal to 1.')
        self.__calculate_a(a)

        self.__calculate_P()


def main():
    #hyp = Hyperopinion.generate_random_belief(3)
    hyp = Hyperopinion(3, [4/9, 3/9, 2/9, 0, 0, 0])
    print(hyp.b)
    print(hyp.u)
    print(hyp.a)
    print(sum(hyp.b) + hyp.u)
    print(hyp.P)


if __name__ == "__main__":
    main()
