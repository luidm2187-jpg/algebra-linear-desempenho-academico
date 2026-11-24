# Análise do Desempenho Acadêmico por meio de Operações Matriciais

**Uma aplicação da Álgebra Linear** — Projeto da disciplina Álgebra Linear e Geometria Analítica

**Integrantes:** NOME DO INTEGRANTE 1 · NOME DO INTEGRANTE 2 · NOME DO INTEGRANTE 3

## O problema

Como operações matriciais podem auxiliar na análise do desempenho acadêmico, permitindo
identificar disciplinas com maior dificuldade, comparar rendimentos e calcular indicadores
de forma sistemática? Usamos notas **reais** de 382 estudantes de duas escolas portuguesas
que cursaram Matemática e Português (base *Student Performance*, UCI). As notas formam a
matriz **N** (382 × 6; linhas = estudantes, colunas = 3 períodos × 2 disciplinas). A partir
dela, transposição, soma, multiplicação por escalar, produto matriz-vetor com pesos
**w = (0,3; 0,3; 0,4)**, produto matricial com matriz bloco-diagonal, covariância
**C = X_cᵀX_c/(m−1)** e médias por grupo **G = (EᵀE)⁻¹EᵀF** produzem todos os indicadores.

## Resultado principal

| Indicador (nota ponderada, 0–10) | Matemática | Português |
|---|---|---|
| Média | **5,31** | **6,16** |
| Desvio-padrão | 1,92 | 1,28 |
| Taxa de aprovação (≥ 5,0) | **57,1 %** | **85,9 %** |
| Variação média P3 − P1 | −0,24 | +0,20 |
| Notas zero no 3º período | 39 | 5 |

Matemática é a disciplina de maior dificuldade: média menor, dispersão maior, queda ao
longo do ano e 42,9 % de reprovação. A correlação entre as duas disciplinas é moderada
(r = 0,58), e o histórico de reprovações é o fator que mais separa os grupos
(5,67 → 3,02 em Matemática). A troca dos pesos dos períodos altera a média em menos de
0,05 ponto, o que mostra que o diagnóstico não depende da escolha de **w**.

## Estrutura

```
algebra-linear-desempenho-academico/
├── README.md
├── requirements.txt
├── codigo/
│   ├── algebra_matricial.py      # operações de Álgebra Linear implementadas à mão
│   ├── main.py                   # pipeline: dados → matrizes → indicadores → gráficos
│   └── test_algebra_matricial.py # confere cada operação manual contra o NumPy
├── dados/
│   ├── student-mat.csv, student-por.csv, student.txt
│   └── LEIAME_DADOS.md           # origem, licença e integração das bases
└── resultados/                   # gerado pelo código
    ├── relatorio_resultados.txt
    ├── demonstracao_passo_a_passo.txt
    ├── matriz_N_notas_0a10.csv, notas_ponderadas_e_indice.csv, matriz_correlacao.csv
    ├── valores.json
    └── graficos/ (fig1 … fig5)
```

## Como executar

- **Python:** 3.10 ou superior (testado no 3.13)
- **Bibliotecas:** numpy, pandas, matplotlib

```bash
git clone https://github.com/<usuario>/algebra-linear-desempenho-academico.git
cd algebra-linear-desempenho-academico
pip install -r requirements.txt
python codigo/main.py
```

Testes (conferem as operações manuais contra o NumPy):

```bash
python -m unittest discover -s codigo -v
```

Alterar os pesos (devem ser não negativos e somar 1):

```bash
python codigo/main.py --pesos-periodos 0.2 0.3 0.5 --pesos-disciplinas 0.6 0.4
```

Os pesos padrão estão no início de `codigo/main.py` (`PESOS_PERIODOS`, `PESOS_DISCIPLINAS`).
São **parâmetros adotados para o estudo**, não pesos oficiais das escolas.

## Por que as operações foram implementadas à mão

`algebra_matricial.py` implementa transposição, soma, multiplicação por escalar, produto
matriz-vetor, produto matricial, covariância, correlação e médias por grupo usando só as
definições (por exemplo, `(AB)_ik = Σ_j A_ij B_jk`). Todos os resultados do projeto saem
dessas funções. O NumPy é usado apenas nos testes, para conferir que as contas estão certas.

## Fonte dos dados

CORTEZ, P.; SILVA, A. *Using data mining to predict secondary school student performance*.
FUBUTEC 2008, p. 5-12. Base disponível em
https://archive.ics.uci.edu/dataset/320/student+performance (licença CC BY 4.0).
