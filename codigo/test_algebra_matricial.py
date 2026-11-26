"""
Testes: conferem as implementações manuais contra o NumPy.
Executar a partir da raiz:  python -m unittest discover -s codigo -v
"""
import unittest

import numpy as np

import algebra_matricial as al

rng = np.random.default_rng(42)
A = rng.integers(0, 21, size=(12, 6)).astype(float)
B = rng.integers(0, 21, size=(12, 6)).astype(float)
v = np.array([0.3, 0.3, 0.4, 0.2, 0.5, 0.3])


class TesteAlgebra(unittest.TestCase):
    def igual(self, x, y):
        np.testing.assert_allclose(np.array(x, dtype=float), y, atol=1e-10)

    def test_transposta(self):
        self.igual(al.transposta(A.tolist()), A.T)

    def test_soma_e_escalar(self):
        self.igual(al.soma(A.tolist(), B.tolist()), A + B)
        self.igual(al.escalar(0.5, A.tolist()), 0.5 * A)

    def test_mat_vet(self):
        self.igual(al.mat_vet(A.tolist(), v.tolist()), A @ v)

    def test_mat_mat(self):
        self.igual(al.mat_mat(A.T.tolist(), B.tolist()), A.T @ B)

    def test_dimensao_incompativel(self):
        with self.assertRaises(ValueError):
            al.mat_vet(A.tolist(), [1.0, 2.0])

    def test_medias(self):
        self.igual(al.media_colunas(A.tolist()), A.mean(axis=0))
        self.igual(al.media_linhas(A.tolist()), A.mean(axis=1))

    def test_covariancia_correlacao(self):
        self.igual(al.covariancia(A.tolist()), np.cov(A, rowvar=False))
        self.igual(al.correlacao(A.tolist()), np.corrcoef(A, rowvar=False))

    def test_bloco_diagonal_equivale_a_produtos_separados(self):
        w = [0.3, 0.3, 0.4]
        F = al.mat_mat(A.tolist(), al.bloco_diagonal(w, 2))
        self.igual([l[0] for l in F], A[:, :3] @ w)
        self.igual([l[1] for l in F], A[:, 3:] @ w)

    def test_medias_por_grupo(self):
        grupo = np.array([0, 1, 0, 2, 1, 0, 2, 2, 1, 0, 1, 2])
        E = np.eye(3)[grupo]
        esperado = np.array([A[grupo == k].mean(axis=0) for k in range(3)])
        self.igual(al.medias_por_grupo(E.tolist(), A.tolist()), esperado)


if __name__ == "__main__":
    unittest.main()
