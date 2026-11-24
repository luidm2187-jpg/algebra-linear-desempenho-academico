# Guia de entrega — passo a passo

## 1. Antes de tudo (5 min)
- [ ] Coloquem os **nomes completos** dos três em `artigo/artigo.tex` (linhas 6–8) e no `README.md` do repositório.
- [ ] Confiram a linha `\Instituicao` (linha 9 do .tex) e ajustem se necessário.
- [ ] Depois de criar o repositório, troquem `USUARIO` pelo usuário do GitHub em `\Repositorio` (linha 10) e no README.
- [ ] Recompilem o PDF: abram o `.tex` no **Overleaf** (Novo projeto → Upload → enviem `artigo.tex` + pasta `graficos/`) e cliquem em *Recompile*. Também funciona localmente com `pdflatex artigo.tex`.
- [ ] Confiram com a professora quais livros são da **bibliografia da disciplina**. O artigo cita Boldrini et al., Steinbruch e Winterle, Anton e Rorres, e Lay. Se o plano de ensino usar outro, troquem uma das referências.

## 2. Repositório no GitHub (commits dos TRÊS)
A professora avalia os commits de cada integrante. Dividam assim (cada um faz o seu commit, com a própria conta):

| Integrante | O que sobe | Mensagem sugerida |
|---|---|---|
| 1 | cria o repositório `algebra-linear-desempenho-academico` + `dados/` + `.gitignore` + `requirements.txt` | `Adiciona base Student Performance (UCI) e dependências` |
| 2 | `codigo/algebra_matricial.py` + `codigo/test_algebra_matricial.py` | `Implementa operações matriciais manuais e testes` |
| 3 | `codigo/main.py` + `resultados/` | `Adiciona pipeline de análise, gráficos e resultados` |
| 1, 2 ou 3 | `README.md` com os nomes | `Adiciona README com instruções de execução` |

Comandos (o Integrante 1 cria; os outros fazem `git clone` primeiro):
```bash
git clone https://github.com/USUARIO/algebra-linear-desempenho-academico.git
cd algebra-linear-desempenho-academico
# copiar os arquivos da sua parte para cá
git add .
git commit -m "mensagem da tabela"
git push
```
O Integrante 1 adiciona os outros dois como colaboradores: **Settings → Collaborators → Add people**.

## 3. Acesso da professora (obrigatório)
**Settings → Collaborators (seção Access) → Add people → `KarlaHaryanna`**.
Repositório privado sem esse acesso conta como projeto não entregue.

## 4. Testar antes de entregar
```bash
pip install -r requirements.txt
python codigo/main.py
python -m unittest discover -s codigo -v
```
Precisa aparecer o relatório e "Ran 9 tests ... OK".

## 5. Classroom
Postem o **PDF** do artigo e coloquem o **link do repositório no comentário** da postagem.
Prazo: quarta-feira da semana de avaliações da II Unidade. Atraso custa −2,0 pontos por dia.

## 6. Preparação para a arguição oral (qualquer um pode ser chamado)
Cada integrante deve saber responder:
1. **Por que N é 382 × 6?** 382 estudantes (linhas) × 3 períodos × 2 disciplinas (colunas).
2. **Por que N·w existe?** N_Mat tem 3 colunas e w tem 3 componentes; o resultado tem 382 componentes, uma nota por aluno.
3. **Por que os pesos somam 1?** Para o resultado ser uma média ponderada e continuar na escala 0–10.
4. **O que é W bloco-diagonal?** Coloca w na coluna de Matemática e na de Português, e assim F = NW calcula as duas disciplinas de uma vez.
5. **Como Aᵀ1/m dá a média?** Cada linha de Aᵀ é uma coluna de A; multiplicar por 1 soma os elementos; dividir por m dá a média.
6. **O que é (EᵀE)⁻¹EᵀF?** EᵀE é diagonal com o tamanho de cada grupo, EᵀF soma as notas de cada grupo, e a inversa divide: o resultado é a média do grupo.
7. **Refazer à mão** a conta de n₁ = 2,85 e r = 0,577 (Seção 4 do artigo).
8. **Por que tantos zeros em Matemática?** 39 alunos com zero no 3º período depois de notas positivas: provável ausência na prova final, e não nota obtida. Discutido na seção de análise crítica.
9. **Por que implementar à mão se existe NumPy?** Para a Álgebra Linear ser o motor da solução. O NumPy só confere as contas nos testes.
