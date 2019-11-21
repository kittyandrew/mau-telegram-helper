from itertools import combinations as comb
from itertools import permutations as perm
import enchant


class TextGame:
    def __init__(self, letters:list):
        self.letters = letters

    def _get_all_combinations(self, from_smaller=False, join=False):
        result = []
        for l in range(1, len(self.letters)+1):
            for subset in comb(self.letters, l if from_smaller else (len(self.letters) - l)):
                for each_possible in perm(subset):
                    if join:
                        yield ''.join(each_possible)
                    else:
                        yield each_possible

    def get_best(self, bad_search=False):
        dictinonary_us = enchant.Dict('en_US')
        dictinonary_en = enchant.Dict('en_UK')
        for each in self._get_all_combinations(join=True):
            # Have to suppress exceptions because 'pyenchant'
            # is not maintainted anymore and it sucks in general
            try:
                if dictinonary_us.check(each) or dictinonary_en.check(each):
                    if bad_search or len(each) > 3:
                        return each
            except Exception as e:
                pass

    def get_all(self, from_smaller=False, bad_search=False):
        result = []
        dictinonary_us = enchant.Dict('en_US')
        dictinonary_en = enchant.Dict('en_UK')
        for each in self._get_all_combinations(from_smaller=from_smaller, join=True):
            # Have to suppress exceptions because 'pyenchant'
            # is not maintainted anymore and it sucks in general
            try:
                if dictinonary_us.check(each) or dictinonary_en.check(each):
                    if each not in result:
                        if bad_search or len(each) > 3:
                            result.append(each)
            except Exception as e:
                pass
        return result
