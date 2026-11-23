# Dados

Base pública **Student Performance** (UCI Machine Learning Repository), coletada em
duas escolas públicas de Portugal (Gabriel Pereira — GP e Mousinho da Silveira — MS)
no ano letivo de 2005/2006 e descrita por Cortez e Silva (2008).

| Arquivo | Conteúdo |
|---|---|
| `student-mat.csv` | 395 estudantes da disciplina de Matemática (separador `;`) |
| `student-por.csv` | 649 estudantes da disciplina de Português (separador `;`) |
| `student.txt` | Dicionário de variáveis original (inglês) |

Variáveis usadas: `G1`, `G2`, `G3` (notas do 1º, 2º e 3º período, escala 0–20; G3 é a
nota final do ano), `school`, `studytime` e `failures`.

**Integração das duas bases:** os 382 estudantes que cursaram as duas disciplinas são
identificados pelo mesmo procedimento do script oficial `student-merge.R`, isto é,
pela coincidência de 13 atributos (`school, sex, age, address, famsize, Pstatus, Medu,
Fedu, Mjob, Fjob, reason, nursery, internet`). Cada estudante recebe um código
`E001`…`E382` na ordem da base de Matemática.

- Fonte: https://archive.ics.uci.edu/dataset/320/student+performance
- Licença: CC BY 4.0
- Referência: CORTEZ, P.; SILVA, A. Using data mining to predict secondary school
  student performance. *In*: BRITO, A.; TEIXEIRA, J. (ed.). Proceedings of 5th Future
  Business Technology Conference (FUBUTEC 2008). Porto: EUROSIS, 2008. p. 5-12.
