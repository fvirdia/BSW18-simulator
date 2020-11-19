from sage.all import log, exp
from sage.all import line, save, load, identity_matrix, matrix
from fpylll import IntegerMatrix, GSO, LLL, FPLLL, BKZ
from fpylll.tools.bkz_simulator import simulate as CN11_simulate
import BSW18
import og

# n_halfs, block_size, max_loops = 50, 45, 2000
n_halfs, block_size, max_loops = 90, 170, 60
# n_halfs, block_size, max_loops = 75, 60, 50
# n_halfs, block_size, max_loops = 75, 60, 20000

# generate lattice instance
FPLLL.set_random_seed(1337)
q = 2**30
mat = IntegerMatrix.random(2*n_halfs, "qary", q=q, k=n_halfs)
A = LLL.reduction(mat)
M = GSO.Mat(A)
M.update_gso()

cn11 = CN11_simulate(M, BKZ.Param(block_size=block_size, max_loops=max_loops))
bsw18 = BSW18.simulate(M, BKZ.Param(block_size=block_size, max_loops=max_loops))
og = og.simulate(M, BKZ.Param(block_size=block_size, max_loops=max_loops))
g = line([(i, log(cn11[0][i])/2 - log(q)/2) for i in range(len(cn11[0]))]) \
    + line([(i, log(bsw18[0][i])/2 - log(q)/2) for i in range(len(bsw18[0]))], color='red', thickness=2) \
    + line([(i, log(og[0][i])/2 - log(q)/2) for i in range(len(og[0]))], color='green')
save(g, "test.png", dpi=150)

log_vol_cn11 = sum(map(lambda x: log(x)/2, cn11[0]))
log_vol_bsw18 = sum(map(lambda x: log(x)/2, bsw18[0]))
log_vol_og = sum(map(lambda x: log(x)/2, og[0]))

smat = matrix(M.d, M.d)
mat.to_matrix(smat)
vol = abs(smat.determinant())
log_vol = log(vol).n()

print("log vol %.6f" % log_vol)
print("   cn11 %.6f" % log_vol_cn11)
print("  bsw18 %.6f" % log_vol_bsw18)
print("     og %.6f" % log_vol_og)