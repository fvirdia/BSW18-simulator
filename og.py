"""
Wrapper to original implementation of BSW18.
"""

import random
from math import log, exp
from fpylll.fplll.integer_matrix import IntegerMatrix
from fpylll.fplll.gso import MatGSO, GSO
from fpylll import FPLLL
from probabilistic_simulator import probabilistic_bkz_simulator

rk = (
    0.789527997160000,
    0.780003183804613,
    0.750872218594458,
    0.706520454592593,
    0.696345241018901,
    0.660533841808400,
    0.626274718790505,
    0.581480717333169,
    0.553171463433503,
    0.520811087419712,
    0.487994338534253,
    0.459541470573431,
    0.414638319529319,
    0.392811729940846,
    0.339090376264829,
    0.306561491936042,
    0.276041187709516,
    0.236698863270441,
    0.196186341673080,
    0.161214212092249,
    0.110895134828114,
    0.0678261623920553,
    0.0272807162335610,
    -0.0234609979600137,
    -0.0320527224746912,
    -0.0940331032784437,
    -0.129109087817554,
    -0.176965384290173,
    -0.209405754915959,
    -0.265867993276493,
    -0.299031324494802,
    -0.349338597048432,
    -0.380428160303508,
    -0.427399405474537,
    -0.474944677694975,
    -0.530140672818150,
    -0.561625221138784,
    -0.612008793872032,
    -0.669011014635905,
    -0.713766731570930,
    -0.754041787011810,
    -0.808609696192079,
    -0.859933249032210,
    -0.884479963601658,
    -0.886666930030433,
)


def simulate(r, param, prng_seed=0xdeadbeef):
    """
    Wraps original BSW18 simulator for ease of comparison.
    """
    if not prng_seed:
        prng_seed = FPLLL.randint(0, 2**32-1)

    random.seed(prng_seed)

    if isinstance(r, IntegerMatrix):
        r = GSO.Mat(r)
    if isinstance(r, MatGSO):
        r.update_gso()
        r = r.r()

    n = len(r)

    # code uses ln of squared norms, FPLLL uses squared norms
    l = list(map(log, r))

    if param.max_loops:
        N = param.max_loops
    else:
        N = n

    # using original.rk_ln
    # l1 = probabilistic_bkz_simulator.bkz_simulation_stochastic(
    #       l, param.block_size, N, original.rk_ln)

    # using rk from this file -- more direct comparison, essentially the same
    log2_e = log(exp(1), 2)
    l1 = probabilistic_bkz_simulator.bkz_simulation_stochastic(
        l, param.block_size, N, list(map(lambda x: x / log2_e, rk)))

    l1 = list(map(exp, l1))
    return l1, N
