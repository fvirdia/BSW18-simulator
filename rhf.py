from sage.all import log, exp
from sage.all import line, save, load, identity_matrix, matrix
from fpylll import IntegerMatrix, GSO, LLL, FPLLL, BKZ
from fpylll.tools.bkz_simulator import simulate as CN11_simulate
import BSW18

n_halfs, block_size, max_loops = 90, 170, 60

# generate lattice instance
FPLLL.set_random_seed(1337)
q = 2**30
mat = IntegerMatrix.random(2*n_halfs, "qary", q=q, k=n_halfs)
A = LLL.reduction(mat)
M = GSO.Mat(A)
M.update_gso()
smat = matrix(M.d, M.d)
mat.to_matrix(smat)
vol = abs(smat.determinant())
log_vol = log(vol).n()


def rhf(b_1_sqr, log_vol, dim):
    log_b_sqr = log(b_1_sqr)
    log_rhf = (0.5 * log_b_sqr - log_vol/dim)/dim
    return exp(log_rhf)


profile_bsw18 = [M.get_r(i, i) for i in range(M.d)]
profile_cn11 = [M.get_r(i, i) for i in range(M.d)]
rhfs_bsw18 = []
rhfs_cn11 = []
rhfs_bsw18.append((0, rhf(profile_bsw18[0], log_vol, M.d)))
rhfs_cn11.append((0, rhf(profile_cn11[0], log_vol, M.d)))
for tour in range(1, max_loops+1):
    profile_bsw18 = BSW18.simulate(profile_bsw18, BKZ.Param(
        block_size=block_size, max_loops=1))[0]
    profile_cn11 = CN11_simulate(profile_cn11, BKZ.Param(
        block_size=block_size, max_loops=1))[0]
    rhfs_bsw18.append((tour, rhf(profile_bsw18[0], log_vol, M.d)))
    rhfs_cn11.append((tour, rhf(profile_cn11[0], log_vol, M.d)))

g = line(rhfs_bsw18, legend_label="BSW18", linestyle="dashed",
         title=f"dim = {M.d}, beta = {block_size}",
         axes_labels=["tours", "rhf"])
g += line(rhfs_cn11, legend_label="CN11", linestyle="dashed", color="red")
save(g, f"rhf-{M.d}-{block_size}.png", dpi=150)
