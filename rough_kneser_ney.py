class N_gram:
    def __init__(self, ngram, table=None, revtable=None):
        "docstring"
        self.ngram = ngram
        self.table = table
        self.revtable = revtable

    def prob_i(self,w, h):

        """
        Args:
        - w: int
        word id
        - h: list<int>
        given sequence

        Example:
        3-gram model
        [he, ll, o] == [10, 8, 2]
        prob_i(2, [10, 8]) # = 0.001 \in [0, 1]
        """
        if len (h) == 0:
            return self.alpha(w, h)
        else:
            return self.alpha(w, h) + self.beta(h) * self.prob_i(w, self.pi(h))

    def alpha(self, w, h):
        return (max(self.c(h + [w]) - self.d(len(h)), 0) /
                self.Sigma(lambda w: self.c_prime(h + [w])))

    def pi(self, h):
        """
        Args:
        - h: list<int>
        given sequence
        """
        if len(h) == 0:
            raise ValueError ("error")
        else:
            return h[1:]

    def beta(self, h):
        """
        Args:
        - h: list<int>
        given sequence
        - w: int
        predict word id
        """
        return (self.d(len(h)) /
                self.Sigma(lambda w: self.c_prime(h + [w])) * self.N_prime(h))
    def d(self, h_len):
        # TODO hyper parameter?
        return 0.5
    def c_prime(self, seq):
        """
        Args:
        - seq: list<int>
        whole sequence
        """
        if len(seq) == self.ngram:
            return self.c(seq)
        else:
            return self.K(seq)
    def c(self, seq):
        # TODO
        # self.table.trace_freq(seq)
        return 2
    def K(self, seq):
        # TODO
        # self.rev_table.trace_var(seq)
        return 2
    def N_prime(self, h):
        # TODO
        # len([self.table.trace_var(h + [u]) for u in self.table.get_whole_vocab()])
        return 2
    def Sigma (self, f):
        """
        Args:
        - f: int -> int
        word id -> count candidate
        Returns:
        sum of count candidate
        """
        # TODO
        # return sum([f(w) for w in self.table.get_whole_vocab()])
        return 100

# ngram = N_gram (2)
# ngram.prob_i(1, [1])
