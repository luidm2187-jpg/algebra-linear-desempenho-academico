"""
nomes.py — nomes FICTÍCIOS para os estudantes (uso apenas no painel)

A base Student Performance é anônima. Para deixar o painel mais fácil de
apresentar, cada estudante recebe um nome inventado, coerente com o sexo
registrado na base (F/M). A semente fixa garante que o mesmo estudante receba
sempre o mesmo nome. Os nomes não correspondem a pessoas reais.
"""
import random

FEMININOS = ["Ana", "Beatriz", "Carolina", "Daniela", "Eduarda", "Fernanda", "Gabriela",
             "Helena", "Isabela", "Júlia", "Larissa", "Laura", "Leticia", "Luana", "Manuela",
             "Mariana", "Marta", "Natália", "Patrícia", "Rafaela", "Raquel", "Rita", "Sara",
             "Sofia", "Teresa", "Valentina", "Vitória", "Inês", "Clara", "Alice", "Bianca",
             "Camila", "Joana", "Lívia", "Matilde", "Yasmin"]
MASCULINOS = ["André", "Bruno", "Caio", "Daniel", "Diogo", "Eduardo", "Felipe", "Gabriel",
              "Gustavo", "Henrique", "Igor", "João", "José", "Leonardo", "Lucas", "Marcos",
              "Mateus", "Miguel", "Nuno", "Paulo", "Pedro", "Rafael", "Ricardo", "Rodrigo",
              "Samuel", "Thiago", "Tomás", "Vítor", "Arthur", "Bernardo", "Davi", "Enzo",
              "Heitor", "Renato", "Sérgio", "Rui"]
SOBRENOMES = ["Almeida", "Alves", "Andrade", "Barbosa", "Barros", "Cardoso", "Carvalho",
              "Castro", "Costa", "Cunha", "Dias", "Duarte", "Fernandes", "Ferreira", "Fonseca",
              "Freitas", "Gomes", "Lima", "Lopes", "Machado", "Marques", "Martins", "Melo",
              "Mendes", "Monteiro", "Moreira", "Nascimento", "Nunes", "Oliveira", "Pereira",
              "Pinto", "Ramos", "Reis", "Ribeiro", "Rocha", "Santos", "Silva", "Sousa",
              "Teixeira", "Vieira"]


def gerar_nomes(sexos, semente=2026):
    """Recebe a lista de sexos ('F'/'M') e devolve um nome único para cada estudante."""
    rng = random.Random(semente)
    usados, nomes = set(), []
    for s in sexos:
        primeiros = FEMININOS if s == "F" else MASCULINOS
        while True:
            nome = f"{rng.choice(primeiros)} {rng.choice(SOBRENOMES)}"
            if nome not in usados:
                usados.add(nome)
                nomes.append(nome)
                break
    return nomes
