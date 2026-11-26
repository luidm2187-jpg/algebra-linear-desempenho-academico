"""
main.py — Análise do Desempenho Acadêmico por meio de Operações Matriciais
==========================================================================
Executar a partir da raiz do repositório:

    python codigo/main.py
    python codigo/main.py --pesos-periodos 0.2 0.3 0.5 --pesos-disciplinas 0.6 0.4

Todos os cálculos de Álgebra Linear são feitos pelas funções MANUAIS de
algebra_matricial.py. O NumPy serve apenas para conferência (ver testes).
"""
import argparse
import json
import os
import sys

import pandas as pd

import algebra_matricial as al

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS = os.path.join(RAIZ, "dados")
SAIDA = os.path.join(RAIZ, "resultados")
GRAFICOS = os.path.join(SAIDA, "graficos")

# ----------------------------------------------------------------- parâmetros
# Pesos ADOTADOS NO ESTUDO (parâmetros, não valores oficiais da escola).
# w: pesos dos três períodos (1º, 2º, 3º). O 3º período recebe peso maior por
#    refletir a avaliação final do ano letivo. Devem somar 1.
PESOS_PERIODOS = [0.3, 0.3, 0.4]
# p: pesos das disciplinas (Matemática, Português) no índice global. Devem somar 1.
PESOS_DISCIPLINAS = [0.5, 0.5]
# Fator de escala: notas originais em 0–20 -> escala brasileira 0–10.
ESCALA = 0.5
# Nota mínima de aprovação na escala 0–10 (equivale a 10/20 no sistema português).
NOTA_APROVACAO = 5.0

DISCIPLINAS = ["Matemática", "Português"]
PERIODOS = ["P1", "P2", "P3"]
COLUNAS = ["Mat_P1", "Mat_P2", "Mat_P3", "Por_P1", "Por_P2", "Por_P3"]
# Atributos usados pela UCI (student-merge.R) para identificar o mesmo aluno
CHAVES = ["school", "sex", "age", "address", "famsize", "Pstatus", "Medu",
          "Fedu", "Mjob", "Fjob", "reason", "nursery", "internet"]


def validar_pesos(v, nome):
    if any(x < 0 for x in v) or abs(sum(v) - 1.0) > 1e-9:
        sys.exit(f"Erro: os pesos {nome} {v} devem ser não negativos e somar 1.")


# ------------------------------------------------------------- dados e matrizes
def carregar_dados():
    mat = pd.read_csv(os.path.join(DADOS, "student-mat.csv"), sep=";")
    por = pd.read_csv(os.path.join(DADOS, "student-por.csv"), sep=";")
    df = mat.merge(por, on=CHAVES, suffixes=("_mat", "_por"))
    df.insert(0, "id", [f"E{i:03d}" for i in range(1, len(df) + 1)])
    return mat, por, df


def matriz_de_notas(df):
    """A (m x 6) na escala original 0–20. Linhas = estudantes."""
    cols = ["G1_mat", "G2_mat", "G3_mat", "G1_por", "G2_por", "G3_por"]
    return [[float(x) for x in linha] for linha in df[cols].values.tolist()]


def fmt(x, c=2):
    return f"{x:.{c}f}".replace(".", ",")


def mat_str(M, c=2, linhas=None):
    linhas = M if linhas is None else M[:linhas]
    return "\n".join("[ " + "  ".join(f"{fmt(x, c):>6}" for x in l) + " ]" for l in linhas)


# ----------------------------------------------------------------- análise
def analisar(w, p):
    os.makedirs(GRAFICOS, exist_ok=True)
    mat, por, df = carregar_dados()
    R = {}  # resultados numéricos (vão para resultados/valores.json)
    m = len(df)
    R["n_mat"], R["n_por"], R["m"] = len(mat), len(por), m

    # 1) Matriz A (0–20) e mudança de escala por multiplicação escalar: N = 0,5 A
    A = matriz_de_notas(df)
    N = al.escalar(ESCALA, A)
    R["dim_N"] = list(al.dimensao(N))

    # 2) Matrizes por período P_k (m x 2) e soma de matrizes
    P = [al.colunas(N, [k, 3 + k]) for k in range(3)]
    S = al.soma(al.soma(P[0], P[1]), P[2])
    M_arit = al.escalar(1 / 3, S)                          # média aritmética
    F_comb = al.soma(al.soma(al.escalar(w[0], P[0]), al.escalar(w[1], P[1])),
                     al.escalar(w[2], P[2]))               # combinação linear

    # 3) Produto matriz-vetor por disciplina: n_s = N_s w
    N_mat, N_por = al.colunas(N, [0, 1, 2]), al.colunas(N, [3, 4, 5])
    nota_mat, nota_por = al.mat_vet(N_mat, w), al.mat_vet(N_por, w)

    # 4) Forma compacta: F = N W, com W bloco-diagonal (6 x 2)
    W = al.bloco_diagonal(w, 2)
    F = al.mat_mat(N, W)
    # verificação: as três formas coincidem
    dif = max(abs(F[i][0] - nota_mat[i]) + abs(F[i][1] - nota_por[i]) +
              abs(F[i][0] - F_comb[i][0]) + abs(F[i][1] - F_comb[i][1]) for i in range(m))
    R["verificacao_F_max_dif"] = dif

    # 5) Índice global g = F p
    g = al.mat_vet(F, p)

    # 6) Médias: por disciplina/período (A^T 1 / m) e por estudante
    mu_N = al.media_colunas(N)
    mu_F = al.media_colunas(F)
    R["media_periodos"] = dict(zip(COLUNAS, mu_N))
    R["media_ponderada_disciplinas"] = dict(zip(DISCIPLINAS, mu_F))
    R["media_aritmetica_disciplinas"] = dict(zip(DISCIPLINAS, al.media_colunas(M_arit)))
    R["media_indice_global"] = sum(g) / m

    # 7) Aprovação: matriz indicadora I (m x 2), taxa = (1/m) I^T 1
    I = al.indicadora(F, NOTA_APROVACAO)
    taxa = al.media_colunas(I)
    R["taxa_aprovacao"] = dict(zip(DISCIPLINAS, taxa))
    ambas = sum(1 for i in range(m) if I[i][0] == 1 and I[i][1] == 1)
    nenhuma = sum(1 for i in range(m) if I[i][0] == 0 and I[i][1] == 0)
    R["aprovados_ambas"], R["reprovados_ambas"] = ambas, nenhuma

    # 8) Covariância e correlação: C = X_c^T X_c / (m-1)
    C6 = al.covariancia(N)
    Corr6 = al.correlacao(N)
    CF = al.covariancia(F)
    CorrF = al.correlacao(F)
    R["desvio_padrao_F"] = dict(zip(DISCIPLINAS, [CF[0][0] ** 0.5, CF[1][1] ** 0.5]))
    R["correlacao_Mat_Por_F"] = CorrF[0][1]
    R["covariancia_F"] = CF
    R["correlacao_6x6"] = Corr6

    # 9) Notas zero no 3º período (ausência na avaliação final)
    zeros_mat = sum(1 for l in A if l[2] == 0)
    zeros_por = sum(1 for l in A if l[5] == 0)
    R["zeros_P3"] = {"Matemática": zeros_mat, "Português": zeros_por}
    sem_zero = [i for i in range(m) if A[i][2] > 0 and A[i][5] > 0]
    F_sz = [F[i] for i in sem_zero]
    R["m_sem_zero"] = len(sem_zero)
    R["media_F_sem_zero"] = dict(zip(DISCIPLINAS, al.media_colunas(F_sz)))
    R["taxa_aprovacao_sem_zero"] = dict(zip(DISCIPLINAS, al.media_colunas(al.indicadora(F_sz, NOTA_APROVACAO))))
    R["correlacao_Mat_Por_sem_zero"] = al.correlacao(F_sz)[0][1]

    # 10) Sensibilidade aos pesos: N_s * Wc, Wc (3 x 3) tem 3 vetores de pesos nas colunas
    cenarios = {"Uniforme (1/3; 1/3; 1/3)": [1 / 3, 1 / 3, 1 / 3],
                "Adotado (" + "; ".join(fmt(x, 1) for x in w) + ")": w,
                "Ênfase final (0,2; 0,3; 0,5)": [0.2, 0.3, 0.5]}
    Wc = al.transposta(list(cenarios.values()))
    sens = {}
    for nome_d, Ns in (("Matemática", N_mat), ("Português", N_por)):
        Y = al.mat_mat(Ns, Wc)  # m x 3
        med = al.media_colunas(Y)
        apr = al.media_colunas(al.indicadora(Y, NOTA_APROVACAO))
        for k, c in enumerate(cenarios):
            sens.setdefault(c, {})[nome_d] = {"media": med[k], "aprovacao": apr[k]}
    R["sensibilidade_pesos"] = sens

    # 11) Comparação entre grupos: G = (E^T E)^{-1} E^T F
    grupos = {}
    for var, rot in (("school", {"GP": "Gabriel Pereira", "MS": "Mousinho da Silveira"}),
                     ("studytime_mat", {1: "<2 h", 2: "2–5 h", 3: "5–10 h", 4: ">10 h"}),
                     ("failures_mat", {0: "0", 1: "1", 2: "2", 3: "3 ou mais"})):
        valores = list(rot.keys())
        E = [[1.0 if (min(v, 3) if var == "failures_mat" else v) == c else 0.0 for c in valores]
             for v in df[var].tolist()]
        G = al.medias_por_grupo(E, F)
        cont = al.mat_vet(al.transposta(E), al.vetor_uns(m))
        grupos[var] = [{"grupo": rot[c], "n": int(cont[k]), "Matemática": G[k][0],
                        "Português": G[k][1]} for k, c in enumerate(valores)]
    R["grupos"] = grupos

    # 12) Ranking pelo índice global
    ordem = sorted(range(m), key=lambda i: g[i], reverse=True)
    R["top5"] = [(df["id"][i], g[i]) for i in ordem[:5]]
    R["bottom5"] = [(df["id"][i], g[i]) for i in ordem[-5:]]
    # Evolução entre períodos: diferença P3 - P1 (subtração de matrizes)
    Delta = al.subtracao(P[2], P[0])
    R["evolucao_media_P3_menos_P1"] = dict(zip(DISCIPLINAS, al.media_colunas(Delta)))

    # ------------------------------------------------------------ saídas
    out = pd.DataFrame(N, columns=COLUNAS)
    out.insert(0, "id", df["id"])
    out.to_csv(os.path.join(SAIDA, "matriz_N_notas_0a10.csv"), index=False, sep=";", decimal=",")
    tab = pd.DataFrame({"id": df["id"], "escola": df["school"],
                        "nota_ponderada_Mat": nota_mat, "nota_ponderada_Por": nota_por,
                        "indice_global": g,
                        "aprovado_Mat": [int(x[0]) for x in I], "aprovado_Por": [int(x[1]) for x in I]})
    tab["posicao_ranking"] = tab["indice_global"].rank(ascending=False, method="min").astype(int)
    tab.to_csv(os.path.join(SAIDA, "notas_ponderadas_e_indice.csv"), index=False, sep=";", decimal=",")
    pd.DataFrame(Corr6, index=COLUNAS, columns=COLUNAS).round(4).to_csv(
        os.path.join(SAIDA, "matriz_correlacao.csv"), sep=";", decimal=",")
    with open(os.path.join(SAIDA, "valores.json"), "w", encoding="utf-8") as f:
        json.dump(R, f, ensure_ascii=False, indent=2)

    demonstracao(N_mat, w, df)
    relatorio(R, w, p)
    graficos(N, F, mu_N, Corr6, R)
    return R


# ----------------------------------------------- demonstração passo a passo
def demonstracao(N_mat, w, df):
    L = ["DEMONSTRAÇÃO PASSO A PASSO — produto matriz-vetor  n = N_Mat(1:4) · w",
         "Dados reais: 4 primeiros estudantes da base integrada (escala 0–10).", "",
         "1) Matriz original (4 x 3; colunas = P1, P2, P3 de Matemática):",
         mat_str(N_mat[:4], 1), "",
         f"2) Operação: produto de matriz (4x3) por vetor de pesos w (3x1) = "
         f"({fmt(w[0], 1)}; {fmt(w[1], 1)}; {fmt(w[2], 1)})^T -> resultado 4x1.",
         "   Compatível porque o nº de colunas da matriz (3) = nº de componentes de w (3).", "",
         "3) Cálculo de cada elemento  n_i = a_i1*w1 + a_i2*w2 + a_i3*w3:"]
    res = []
    for i in range(4):
        a = N_mat[i]
        termos = [a[j] * w[j] for j in range(3)]
        r = sum(termos)
        res.append(r)
        L.append(f"   n_{i+1} ({df['id'][i]}) = {fmt(a[0],1)}·{fmt(w[0],1)} + {fmt(a[1],1)}·{fmt(w[1],1)} + "
                 f"{fmt(a[2],1)}·{fmt(w[2],1)} = {fmt(termos[0])} + {fmt(termos[1])} + {fmt(termos[2])} = {fmt(r)}")
    L += ["", "4) Resultado: n = (" + "; ".join(fmt(x) for x in res) + ")^T",
          "", "5) Interpretação: cada componente é a nota ponderada de Matemática do estudante; "
          f"valores abaixo de {fmt(NOTA_APROVACAO,1)} indicam reprovação."]
    with open(os.path.join(SAIDA, "demonstracao_passo_a_passo.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L))


def relatorio(R, w, p):
    L = ["RELATÓRIO DE RESULTADOS", "=" * 60,
         f"Pesos dos períodos w = {w} | pesos das disciplinas p = {p}",
         f"Estudantes: Matemática={R['n_mat']}, Português={R['n_por']}, em ambas (m)={R['m']}",
         f"Matriz N: {R['dim_N'][0]} x {R['dim_N'][1]}",
         f"Verificação F = N W = combinação linear dos P_k (dif. máx.): {R['verificacao_F_max_dif']:.2e}", "",
         "Médias por período (0–10):"]
    L += [f"  {k}: {fmt(v)}" for k, v in R["media_periodos"].items()]
    L += ["", "Indicadores por disciplina (nota ponderada):"]
    for d in DISCIPLINAS:
        L.append(f"  {d}: média={fmt(R['media_ponderada_disciplinas'][d])}  "
                 f"desvio={fmt(R['desvio_padrao_F'][d])}  aprovação={fmt(100*R['taxa_aprovacao'][d],1)}%  "
                 f"zeros no P3={R['zeros_P3'][d]}  evolução P3-P1={fmt(R['evolucao_media_P3_menos_P1'][d])}")
    L += [f"Índice global médio: {fmt(R['media_indice_global'])}",
          f"Aprovados nas duas: {R['aprovados_ambas']} | reprovados nas duas: {R['reprovados_ambas']}",
          f"Correlação Mat x Por (notas ponderadas): {fmt(R['correlacao_Mat_Por_F'],3)}", "",
          f"Sem estudantes com zero no P3 (m={R['m_sem_zero']}):"]
    for d in DISCIPLINAS:
        L.append(f"  {d}: média={fmt(R['media_F_sem_zero'][d])} aprovação={fmt(100*R['taxa_aprovacao_sem_zero'][d],1)}%")
    L.append(f"  correlação Mat x Por = {fmt(R['correlacao_Mat_Por_sem_zero'],3)}")
    L += ["", "Sensibilidade aos pesos dos períodos:"]
    for c, v in R["sensibilidade_pesos"].items():
        L.append(f"  {c}: " + " | ".join(f"{d}: média {fmt(v[d]['media'])}, aprov. {fmt(100*v[d]['aprovacao'],1)}%" for d in DISCIPLINAS))
    L += ["", "Médias por grupo  G = (E^T E)^(-1) E^T F:"]
    for var, lst in R["grupos"].items():
        L.append(f"  {var}:")
        L += [f"    {x['grupo']:<22} n={x['n']:<4} Mat={fmt(x['Matemática'])}  Por={fmt(x['Português'])}" for x in lst]
    L += ["", "Top 5 (índice global): " + ", ".join(f"{i} ({fmt(v)})" for i, v in R["top5"]),
          "Últimos 5: " + ", ".join(f"{i} ({fmt(v)})" for i, v in R["bottom5"])]
    with open(os.path.join(SAIDA, "relatorio_resultados.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print("\n" + "\n".join(L))


# ------------------------------------------------------------------ gráficos
def graficos(N, F, mu_N, Corr6, R):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    AZUL, LARANJA = "#2a78d6", "#eb6834"   # Matemática, Português
    TINTA, CINZA = "#2b2b2b", "#8a8a8a"
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                         "axes.edgecolor": CINZA, "axes.labelcolor": TINTA, "xtick.color": TINTA,
                         "ytick.color": TINTA, "axes.grid": True, "grid.color": "#e6e6e6",
                         "grid.linewidth": 0.6, "savefig.dpi": 200, "savefig.bbox": "tight"})

    # Fig. 1 — média por período
    fig, ax = plt.subplots(figsize=(6, 3.4))
    x = [1, 2, 3]
    for d, idx, cor in (("Matemática", [0, 1, 2], AZUL), ("Português", [3, 4, 5], LARANJA)):
        y = [mu_N[j] for j in idx]
        ax.plot(x, y, color=cor, lw=2, marker="o", ms=7, label=d)
        for xi, yi in zip(x, y):
            ax.annotate(fmt(yi), (xi, yi), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=9, color=TINTA)
    ax.axhline(NOTA_APROVACAO, color=CINZA, lw=1, ls="--")
    ax.text(3.15, NOTA_APROVACAO, "aprovação", va="center", fontsize=8, color=CINZA)
    ax.set_xticks(x, ["1º período", "2º período", "3º período"])
    ax.set_ylim(4, 7)
    ax.set_ylabel("Média da turma (0–10)")
    ax.legend(frameon=False, loc="upper left")
    fig.savefig(os.path.join(GRAFICOS, "fig1_media_por_periodo.png"))
    plt.close(fig)

    # Fig. 2 — distribuição das notas ponderadas
    fig, ax = plt.subplots(figsize=(6, 3.4))
    bins = [i * 0.5 for i in range(21)]
    ax.hist([[l[0] for l in F], [l[1] for l in F]], bins=bins, color=[AZUL, LARANJA],
            label=["Matemática", "Português"], rwidth=0.9)
    ax.axvline(NOTA_APROVACAO, color=CINZA, lw=1, ls="--")
    ax.set_xlabel("Nota ponderada (0–10)")
    ax.set_ylabel("Nº de estudantes")
    ax.legend(frameon=False)
    fig.savefig(os.path.join(GRAFICOS, "fig2_distribuicao_notas_ponderadas.png"))
    plt.close(fig)

    # Fig. 3 — matriz de correlação 6x6
    rot = ["Mat P1", "Mat P2", "Mat P3", "Por P1", "Por P2", "Por P3"]
    fig, ax = plt.subplots(figsize=(5.2, 4.4))
    im = ax.imshow(Corr6, cmap="Blues", vmin=0, vmax=1)
    ax.grid(False)
    ax.set_xticks(range(6), rot, rotation=45, ha="right")
    ax.set_yticks(range(6), rot)
    for i in range(6):
        for j in range(6):
            ax.text(j, i, fmt(Corr6[i][j]), ha="center", va="center", fontsize=8,
                    color="white" if Corr6[i][j] > 0.6 else TINTA)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="Correlação")
    fig.savefig(os.path.join(GRAFICOS, "fig3_matriz_correlacao.png"))
    plt.close(fig)

    # Fig. 4 — dispersão Mat x Por
    fig, ax = plt.subplots(figsize=(5, 4.2))
    ax.scatter([l[0] for l in F], [l[1] for l in F], s=22, color=AZUL, alpha=0.55,
               edgecolor="white", linewidth=0.6)
    ax.axvline(NOTA_APROVACAO, color=CINZA, lw=1, ls="--")
    ax.axhline(NOTA_APROVACAO, color=CINZA, lw=1, ls="--")
    ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    ax.set_xlabel("Nota ponderada — Matemática")
    ax.set_ylabel("Nota ponderada — Português")
    ax.text(0.3, 9.5, f"r = {fmt(R['correlacao_Mat_Por_F'], 2)}", fontsize=10, color=TINTA)
    fig.savefig(os.path.join(GRAFICOS, "fig4_dispersao_mat_por.png"))
    plt.close(fig)

    # Fig. 5 — médias por tempo de estudo e por reprovações anteriores
    fig, axs = plt.subplots(1, 2, figsize=(8, 3.3), sharey=True)
    for ax, var, tit in ((axs[0], "studytime_mat", "Tempo de estudo semanal"),
                         (axs[1], "failures_mat", "Reprovações anteriores")):
        lst = R["grupos"][var]
        xs = range(len(lst))
        ax.bar([i - 0.2 for i in xs], [g["Matemática"] for g in lst], 0.38, color=AZUL, label="Matemática")
        ax.bar([i + 0.2 for i in xs], [g["Português"] for g in lst], 0.38, color=LARANJA, label="Português")
        ax.set_xticks(list(xs), [f"{g['grupo']}\n(n={g['n']})" for g in lst], fontsize=8)
        ax.set_title(tit, fontsize=10, color=TINTA)
        ax.axhline(NOTA_APROVACAO, color=CINZA, lw=1, ls="--")
    axs[0].set_ylabel("Nota ponderada média")
    fig.legend(*axs[0].get_legend_handles_labels(), frameon=False, ncol=2, loc="upper center", bbox_to_anchor=(0.5, 1.06))
    fig.savefig(os.path.join(GRAFICOS, "fig5_medias_por_grupo.png"))
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pesos-periodos", nargs=3, type=float, default=PESOS_PERIODOS, metavar=("W1", "W2", "W3"))
    ap.add_argument("--pesos-disciplinas", nargs=2, type=float, default=PESOS_DISCIPLINAS, metavar=("PMAT", "PPOR"))
    a = ap.parse_args()
    validar_pesos(a.pesos_periodos, "dos períodos")
    validar_pesos(a.pesos_disciplinas, "das disciplinas")
    analisar(a.pesos_periodos, a.pesos_disciplinas)
    print(f"\nArquivos gerados em: {SAIDA}")


if __name__ == "__main__":
    main()
