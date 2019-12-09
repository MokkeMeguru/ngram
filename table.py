import pandas as pd
from pathlib import Path
import numpy as np
import os

sos_token_idx = 13939


def read_table(path: Path) -> np.array:
    with path.open(encoding="utf-8", mode='r') as r:
        raw_table = r.readlines()
        raw_table = [[sos_token_idx] + line.rstrip(os.linesep).split(' ') for line in raw_table]
        raw_table = np.array(raw_table)
    return raw_table

    # def n_gram(arr: np.array, n: int) -> np.array:

def main():
    neko_path = Path('./neko.num')
    raw_table = read_table(neko_path)
    neko_npy_path = Path('./neko.num.npy')
    np.save(neko_npy_path, raw_table)
