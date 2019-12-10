import pandas as pd
from pathlib import Path
import numpy as np
import os

# sos_token_idx = 13939
eos_token_idx = -1


def read_table(path: Path) -> np.array:
    with path.open(encoding="utf-8", mode='r') as r:
        raw_table = r.readlines()
        raw_table = [  # [sos_token_idx] +
            list(map(lambda s: int(s),
                     line.rstrip(os.linesep).split(' '))) + [-1, -1]
            for line in raw_table
        ]
        raw_table = np.array(raw_table)
    return raw_table


def convert_ngrams(raw_table: np.array, order: int = 3) -> pd.DataFrame:
    ngrams = []
    for seq in raw_table:
        # seq : [1, 2, 3, -1, -1]
        ngram = [seq[i:i + order] for i in range(len(seq) - order + 1)]
        ngrams += ngram
    ngrams = np.array(ngrams)
    columns = ['1st', '2nd', '3rd']
    df = pd.DataFrame(ngrams, columns=columns, dtype=int)
    return df


class GramTable:
    def __init__(self, path: Path, order: int = 3):
        self.order = order
        self.ngramdf = convert_ngrams(read_table(path), order)
        self.n1 = len(self.ngramdf)
        self.n3 = (self.ngramdf['2nd'] != -1).sum()
        self.n2 = (self.ngramdf['3rd'] != -1).sum()
        self.d1 = self.n1 / (self.n1 + 2 * self.n2)
        self.d2 = self.n2 / (self.n2 + 2* self.n3)

    def C(self, wlist: list):
        if len(wlist) == 1:
            # wlist = [w1] -> C(w1)
            return (self.ngramdf['1st'] == wlist[0]).sum()
        if len(wlist) == 2:
            # wlist = [w1 w1] -> C(w1, w2)
            return ((self.ngramdf['1st'] == wlist[0]) &
                    (self.ngramdf['2nd'] == wlist[1])).sum()
        if len(wlist) == 3:
            # wlist = [w1 w1] -> C(w1, w2, w3)
            return ((self.ngramdf['1st'] == wlist[0]) &
                    (self.ngramdf['2nd'] == wlist[1]) &
                    (self.ngramdf['3rd'] == wlist[2])).sum()

    def K(self, wlist: list):
        if len(wlist) == 1:
            # wlist = [w2] -> K(w2) -> 'xw2' の x の種類数
            return len(self.ngramdf[(
                self.ngramdf['2nd'] == wlist[0])]['1st'].unique())
        if len(wlist) == 2:
            # wlist = [w2 w3] -> K(w2, w3) -> 'xw2w3' の x の種類数
            return len(self.ngramdf[(self.ngramdf['2nd'] == wlist[0]) & (
                self.ngramdf['3rd'] == wlist[1])]['1st'].unique())

    def N(self, wlist: list, order):
        """calculation of N_{1+}^{'}(...)
        """
        if len(wlist) == 1:
            # wlist = [w1] = |{u: c'(h, u) > 0}|
            if len(wlist) == order - 1:
                # if |h| = n - 1
                # -> c(w1, u) が 0 より大きい u の種類数
                return len(self.ngramdf[(
                    (self.ngramdf['1st'] == wlist[0]) &
                    (self.ngramdf['2nd'] != -1))]['2nd'].unique())
            else:
                # if |h| < n - 1
                # -> K(w1, u) (-> 'xw1u' の x の種類数) が 0 より大きい u の種類数
                return len(self.ngramdf[(
                    (self.ngramdf['2nd'] == wlist[0]) &
                    (self.ngramdf['3rd'] != -1))]['3rd'].unique())
        else:
            # wlist = [w1, w2]
            # -> c(w1, u) が 0 より大きい u の種類数
            # この GramTable は trigram までが対応範囲
            return len(
                self.ngramdf[((self.ngramdf['1st'] == wlist[0]) &
                              (self.ngramdf['2nd'] == wlist[1]) &
                              (self.ngramdf['3rd'] != -1))]['3rd'].unique())


def main():
    neko_path = Path('./neko.num')
    raw_table = read_table(neko_path)
    ngrams = convert_ngrams(raw_table)
    ngrams.to_csv(Path('./neko-ngrams.tsv'), index=False, sep='\t')


if __name__ == '__main__':
    main()


# def test_ngram_count(path, order) -> int:
#     ngrams = []
#     with path.open(encoding="utf-8", mode='r') as r:
#         raw_table = r.readlines()
#         raw_table = [  # [sos_token_idx] +
#             list(map(lambda s: int(s),
#                      line.rstrip(os.linesep).split(' '))) for line in raw_table
#         ]
#         raw_table = np.array(raw_table)
#         for seq in raw_table:
#             ngram = [seq[i:i + order] for i in range(len(seq) - order + 1)]
#             ngrams += ngram
#         ngrams = np.array(ngrams)
#         return len(ngrams)
