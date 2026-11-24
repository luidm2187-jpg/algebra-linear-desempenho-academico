"""
algebra_matricial.py
--------------------
Implementação MANUAL (sem NumPy) das operações de Álgebra Linear usadas no
projeto. Cada função segue a definição matemática apresentada no artigo.

Uma matriz é representada como lista de linhas:  A = [[a11, a12], [a21, a22]]
Um vetor coluna é representado como lista simples: v = [v1, v2, v3]

O NumPy é usado apenas nos testes (test_algebra_matricial.py) para CONFERIR
que estas implementações produzem os mesmos resultados.
"""


# ---------------------------------------------------------------- utilidades
def dimensao(A):
    """Retorna (m, n): número de linhas e de colunas de A."""
    m = len(A)
    n = len(A[0]) if m > 0 else 0
    for linha in A:
        if len(linha) != n:
            raise ValueError("Matriz mal formada: linhas com tamanhos diferentes.")
    return m, n


def vetor_uns(m):
    """Vetor 1 = (1, 1, ..., 1) com m componentes."""
    return [1.0] * m


# ------------------------------------------------------------ operações base
def transposta(A):
    """(A^T)_{ij} = A_{ji}.  Se A é m x n, A^T é n x m."""
    m, n = dimensao(A)
    return [[A[i][j] for i in range(m)] for j in range(n)]


def soma(A, B):
    """(A + B)_{ij} = A_{ij} + B_{ij}. Exige A e B de mesma dimensão."""
    if dimensao(A) != dimensao(B):
        raise ValueError(f"Soma impossível: {dimensao(A)} e {dimensao(B)}.")
    m, n = dimensao(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(m)]


def subtracao(A, B):
    """(A - B)_{ij} = A_{ij} - B_{ij}."""
    return soma(A, escalar(-1.0, B))


def escalar(k, A):
    """(kA)_{ij} = k * A_{ij}."""
    return [[k * a for a in linha] for linha in A]


def mat_vet(A, v):
    """
    Produto matriz-vetor: se A é m x n e v tem n componentes,
        (Av)_i = sum_{j=1..n} A_{ij} * v_j      (resultado com m componentes)
    """
    m, n = dimensao(A)
    if len(v) != n:
        raise ValueError(f"Dimensões incompatíveis: A é {m}x{n}, v tem {len(v)}.")
    return [sum(A[i][j] * v[j] for j in range(n)) for i in range(m)]


def mat_mat(A, B):
    """
    Produto matricial: se A é m x n e B é n x p,
        (AB)_{ik} = sum_{j=1..n} A_{ij} * B_{jk}   (resultado m x p)
    """
    m, n = dimensao(A)
    n2, p = dimensao(B)
    if n != n2:
        raise ValueError(f"Dimensões incompatíveis: {m}x{n} vezes {n2}x{p}.")
    Bt = transposta(B)  # acesso por colunas de B
    return [[sum(A[i][j] * Bt[k][j] for j in range(n)) for k in range(p)] for i in range(m)]


def produto_externo(u, v):
    """u v^T: matriz len(u) x len(v) com (u v^T)_{ij} = u_i v_j."""
    return [[ui * vj for vj in v] for ui in u]


def colunas(A, indices):
    """Submatriz formada pelas colunas indicadas."""
    return [[linha[j] for j in indices] for linha in A]


def diagonal(v):
    """Matriz diagonal D com D_{ii} = v_i."""
    n = len(v)
    return [[v[i] if i == j else 0.0 for j in range(n)] for i in range(n)]


def bloco_diagonal(w, blocos):
    """
    Matriz W (len(w)*blocos x blocos) com o vetor w repetido na diagonal:
        W = [[w, 0], [0, w]]  para blocos = 2.
    """
    k = len(w)
    W = [[0.0] * blocos for _ in range(k * blocos)]
    for b in range(blocos):
        for t in range(k):
            W[b * k + t][b] = w[t]
    return W


# --------------------------------------------- operações estatísticas matriciais
def media_colunas(A):
    """mu = (1/m) A^T 1  -> média de cada coluna (ex.: média por disciplina)."""
    m, _ = dimensao(A)
    return [x / m for x in mat_vet(transposta(A), vetor_uns(m))]


def media_linhas(A):
    """r = (1/n) A 1  -> média de cada linha (ex.: média por estudante)."""
    _, n = dimensao(A)
    return [x / n for x in mat_vet(A, vetor_uns(n))]


def centralizar(A):
    """X_c = A - 1 mu^T  (subtrai de cada coluna a sua média)."""
    m, _ = dimensao(A)
    return subtracao(A, produto_externo(vetor_uns(m), media_colunas(A)))


def covariancia(A):
    """C = (1/(m-1)) X_c^T X_c   (matriz n x n, simétrica)."""
    m, _ = dimensao(A)
    Xc = centralizar(A)
    return escalar(1.0 / (m - 1), mat_mat(transposta(Xc), Xc))


def correlacao(A):
    """R = D^{-1/2} C D^{-1/2}, com D = diag(C)."""
    C = covariancia(A)
    n = len(C)
    d = diagonal([1.0 / C[i][i] ** 0.5 for i in range(n)])
    return mat_mat(mat_mat(d, C), d)


def medias_por_grupo(E, A):
    """
    Médias de A dentro de grupos codificados pela matriz indicadora E (m x g),
    onde E_{ik} = 1 se o estudante i pertence ao grupo k:
        G = (E^T E)^{-1} E^T A
    E^T E é diagonal (quantidade de estudantes em cada grupo), logo a inversa é
    obtida invertendo cada elemento da diagonal.
    """
    EtE = mat_mat(transposta(E), E)
    g = len(EtE)
    inv = diagonal([1.0 / EtE[k][k] if EtE[k][k] else 0.0 for k in range(g)])
    return mat_mat(inv, mat_mat(transposta(E), A))


def indicadora(A, limite):
    """I_{ij} = 1 se A_{ij} >= limite, senão 0 (aprovação)."""
    return [[1.0 if a >= limite else 0.0 for a in linha] for linha in A]
