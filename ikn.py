import sys
from tqdm import tqdm
from pathlib import Path
from table import GramTable, read_table, convert_ngrams


class Bigram:
    def __init__(self, table, vocab_size=13938):
        self.table = table
        self.vocab_size = vocab_size

    def prob(self, w2, w1):
        """p(w2|w1)
        """
        tmp = self.table.Sigma_C([w1])
        alpha = max(self.table.C([w1, w2]) - self.table.d1, 0)
        alpha = alpha / tmp
        beta = self.table.d1 / tmp
        beta = beta * self.table.N_c([w1])
        _uniprob = self.uniprob(w2)
        return alpha + beta * _uniprob

    def uniprob (self, w2):
        """p(w2)
        """
        alpha = self.table.K ([w2])
        alpha = alpha / self.table.Sigma_K([])
        return alpha



class Trigram:
    def __init__(self, table, vocab_size=13938):
        self.table = table
        self.vocab_size = vocab_size
        self.bi_k = {}
        self.uni_k = {}

    def prob(self, w3, w1, w2):
        """p(w3|w1, w2)
        """
        tmp = self.table.Sigma_C([w1, w2])
        alpha = max(self.table.C([w1, w2, w3]) - self.table.d2, 0)
        alpha = alpha / tmp
        beta = self.table.d2 / tmp
        beta  = beta * self.table.N_c([w1, w2])
        _biprob = self.biprob(w3, w2)
        return alpha + beta * _biprob

    def biprob(self, w3, w2):
        """p(w3|w2)
        """
        tmp = self.table.Sigma_K([w2])
        alpha = max(self.table.K([w2, w3]) - self.table.d1, 0)
        alpha = alpha / tmp
        beta = self.table.d1 / tmp
        beta = beta * self.table.N_k([w2])
        _uniprob = self.uniprob (w3)
        return alpha + beta * _uniprob

    def uniprob (self, w3):
        """p(w3)
        """
        alpha = self.table.K ([w3])
        alpha = alpha / self.table.Sigma_K([])
        return alpha

def main(gram=3):
    neko_path = Path('./neko.num')
    gramTable = GramTable(neko_path, order=3)
    res = []
    if gram == 3:
        trigram = Trigram(gramTable)
        for i in tqdm(range(1, trigram.vocab_size + 1)):
            res += [trigram.prob(i, 24, 28)]
        with open('trigram.model', 'w') as f:
            for r in res:
                f.write("{:.17e}\n".format(r))
    if gram == 2:
        bigram = Bigram(gramTable)
        for i in tqdm(range(1, bigram.vocab_size + 1)):
            res += [bigram.prob(i, 28)]
        with open('bigram.model', 'w') as f:
            for r in res:
                f.write("{:.17e}\n".format(r))

if __name__ == '__main__':
    args = sys.argv
    if len(args) != 1 and args[1].isdigit():
        print('invalid argument: the argument is 3(trigram) or 2(bigram)')
    else:
        main(gram=int(args[1]))
