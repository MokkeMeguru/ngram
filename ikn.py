from pathlib import Path
from table import GramTable, read_table, convert_ngrams


class Bigram:
    def __init__(self, table, vocab_size=13938):
        self.table = table
        self.vocab_size = vocab_size

    def prob(self, w2, w1):
        """p(w2|w1)
        """
        a = max(self.table.C([w1, w2]) - self.table.d1, 0)
        a = a / self.table.C([w1])
        beta = self.table.d1 / self.table.C([w1])
        beta = beta * self.table.N([w1], order=2)
        _prob = self.table.K([w2]) / sum(
            [self.table.K([w]) for w in range(1, self.vocab_size + 1)])
        return a + beta * _prob


class Trigram:
    def __init__(self, table, vocab_size=13938):
        self.table = table
        self.vocab_size = vocab_size
        self.bi_k = {}
        self.uni_k = {}

        def prob(self, w3, w1, w2):
            """p(w3|w1, w2)
            """
            alpha = max(self.table.C([w1, w2, w3]) - self.table.d2, 0)
            beta = self.table.d2 / self.table.C([w1, w2])
            beta = beta * self.table.N([w1, w2], order=3)  # TODO: check
            _biprob = biprob(w3, w2)
            return alpha + beta * _biprob

        def biprob(self, w3, w2):
            """p(w3|w2)
            """
            alpha = max(self.table.K([w2, w3]) - self.table.d1, 0)
            if str (w2)  in self.bi_k:
                beta = self.table.d1 / self.bi_k [str (w2)]
            else:
                tmp = sum(
                    [self.table.K([w2, w]) for w in range(1, self.vocab_size + 1)])
                self.bi_k [str (w2)] = tmp
                beta = self.table.d1 / tmp
            beta = beta * self.table.N ([w2], order=2)
            _uniprob = uniprob (w3)
            return alpha + beta * _uniprob
        def uniprob (self, w3):
            """p(w3)
            """
            alpha = self.table.K ([w3])
            # if uni_k
            # alpha = alpha /  len(df[(df['2nd' != -1])]['1st', '2nd'].unique())
            # return alpha
            raise Exception ("not implemented")

def main():
    neko_path = Path('./neko.num')
    gramTable = GramTable(neko_path, order=3)
    bigram = Bigram(gramTable)
    res = []
    for i in range(1, bigram.vocab_size + 1):
        res += [bigram.prob(i, 28)]
    with open('bigram.model', 'w') as f:
        for r in res:
            f.write("{:.17e}".format(r))


if __name__ == '__main__':
    main()
