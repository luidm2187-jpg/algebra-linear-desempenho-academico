"""
painel.py — gera e abre o painel interativo (resultados/painel.html)

    python codigo/painel.py

O painel usa a MESMA matriz N (382 x 6) construída por main.py e reproduz, no
navegador, as mesmas fórmulas de algebra_matricial.py (F = N W, g = F p,
médias, covariância, correlação e médias por grupo), permitindo alterar os
pesos e ver os resultados mudarem na hora. Não precisa de internet.
"""
import json
import os
import unicodedata
import webbrowser

import algebra_matricial as al
from main import ESCALA, SAIDA, carregar_dados, matriz_de_notas
from nomes import gerar_nomes

AQUI = os.path.dirname(os.path.abspath(__file__))


def gerar_painel(abrir=True):
    _, _, df = carregar_dados()
    N = al.escalar(ESCALA, matriz_de_notas(df))          # N = 0,5 A
    nomes = gerar_nomes(df["sex"].tolist())                # nomes fictícios
    # Linhas em ordem alfabética pelo nome. Trocar a ordem das linhas é multiplicar
    # N por uma matriz de permutação (PN): nenhuma média, nota ou ranking muda.
    sem_acento = lambda t: unicodedata.normalize("NFD", t).encode("ascii", "ignore").decode().lower()
    ordem = sorted(range(len(nomes)), key=lambda i: sem_acento(nomes[i]))
    col = lambda serie: [serie[i] for i in ordem]
    dados = {
        "ids": col(df["id"].tolist()),
        "nomes": col(nomes),
        "N": col(N),
        "escola": col(df["school"].tolist()),
        "school": col(df["school"].tolist()),
        "studytime": col(df["studytime_mat"].astype(int).tolist()),
        "failures": col(df["failures_mat"].astype(int).tolist()),
    }
    with open(os.path.join(AQUI, "painel_modelo.html"), encoding="utf-8") as f:
        html = f.read().replace("__DADOS__", json.dumps(dados, ensure_ascii=False))
    os.makedirs(SAIDA, exist_ok=True)
    destino = os.path.join(SAIDA, "painel.html")
    with open(destino, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Painel gerado em: {destino}")
    if abrir:
        webbrowser.open("file://" + os.path.abspath(destino))
    return destino


if __name__ == "__main__":
    gerar_painel()
