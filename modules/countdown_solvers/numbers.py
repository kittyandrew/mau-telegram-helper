from itertools import combinations as comb
from itertools import permutations as perm
from itertools import zip_longest as z
from itertools import product as prod
import asyncio
import re


class NumberGame:
    signs = ['*', '+', '/', '-']
    raw_pattern = r"((\d+[+-]|\d+[-+])+\d+(?=[*\/]))|((?<=[*\/])\d+([-+]\d+|[+-]\d+)+)"

    def __init__(self, numbers: list, goal: int):
        self.numbers = numbers
        self.goal = goal

        self.raw_solution = {}

        self.regex = re.compile(self.raw_pattern)

    def _solve(self, nums:tuple, permut_tmp:tuple) -> tuple:
        for each in permut_tmp:
            permutations = set()
            eqs = "".join([str(x) + str(y if y is not None else "") for x, y in [temp for temp in z(nums, each)]])
            try:
                if hash(eqs) not in permutations:
                    permutations.add(hash(eqs))
                    yield (eqs, eval(eqs))
            except GeneratorExit:
                return
            except ZeroDivisionError:
                pass

            m = self.regex.search(eqs)
            if m:
                r = self.regex.sub(r' (\1\3) ', eqs)
                spl = [([x[1:-1], x] if '(' in x else x) for x in r.split()]
                count = sum(isinstance(i, list) for i in spl)
                for binar in prod([0, 1], repeat=count):
                    temp_r = ''
                    counter = 0
                    for rep in spl:
                        if isinstance(rep, list):
                            state = binar[counter]
                            temp_r += rep[state]
                            counter += 1
                        else:
                            temp_r += rep
                    try:
                        if hash(temp_r) not in permutations:
                            permutations.add(hash(temp_r))
                            yield (temp_r, eval(temp_r))
                    except GeneratorExit:
                        return
                    except ZeroDivisionError:
                        pass

    def solve_all(self) -> tuple:
        curr_length = 0
        for l in range(1, len(self.numbers)+1):
            for subset in comb(self.numbers, l):
                for each_possible in perm(subset):

                    if curr_length != len(each_possible):
                        curr_length = len(each_possible)
                        signs_permutations = tuple(prod(self.signs, repeat=curr_length - 1))

                    for answer in self._solve(each_possible, signs_permutations):
                        yield answer

    def get_any(self) -> tuple:
        for solution in self.solve_all():
            if solution[1] == self.goal:
                return solution

    def get_all(self) -> list:
        result = []
        for solution in self.solve_all():
            if solution[1] == self.goal:
                result.append(solution)
        return result


class AsyncNumberGame(NumberGame):

    async def _solve(self, nums:tuple, permut_tmp:tuple) -> tuple:
        for each in permut_tmp:
            permutations = set()
            eqs = "".join([str(x) + str(y if y is not None else "") for x, y in [temp for temp in z(nums, each)]])
            try:
                if hash(eqs) not in permutations:
                    permutations.add(hash(eqs))
                    yield (eqs, eval(eqs))
            except GeneratorExit:
                return
            except ZeroDivisionError:
                pass

            m = self.regex.search(eqs)
            if m:
                r = self.regex.sub(r' (\1\3) ', eqs)
                spl = [([x[1:-1], x] if '(' in x else x) for x in r.split()]
                count = sum(isinstance(i, list) for i in spl)
                for binar in prod([0, 1], repeat=count):
                    temp_r = ''
                    counter = 0
                    for rep in spl:
                        if isinstance(rep, list):
                            state = binar[counter]
                            temp_r += rep[state]
                            counter += 1
                        else:
                            temp_r += rep
                    try:
                        if hash(temp_r) not in permutations:
                            permutations.add(hash(temp_r))
                            yield (temp_r, eval(temp_r))
                    except GeneratorExit:
                        return
                    except ZeroDivisionError:
                        pass

    async def solve_all(self) -> tuple:
        curr_length = 0
        for l in range(1, len(self.numbers)+1):
            for subset in comb(self.numbers, l):
                for each_possible in perm(subset):

                    if curr_length != len(each_possible):
                        curr_length = len(each_possible)
                        signs_permutations = tuple(prod(self.signs, repeat=curr_length - 1))

                    async for answer in self._solve(each_possible, signs_permutations):
                        yield answer
                        await asyncio.sleep(0)

    async def get_any(self) -> tuple:
        async for solution in self.solve_all():
            if solution[1] == self.goal:
                return solution

    async def get_all(self) -> list:
        result = []
        async for solution in self.solve_all():
            if solution[1] == self.goal:
                result.append(solution)
        return result
