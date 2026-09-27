# MIS — Conjunto Independente Máximo (PLI)

Requisitos: `pip install pulp networkx` (o solver CBC já vem com o PuLP).

- Gerar instâncias: `python gerar_instancias.py 20 0.2 1 instancias/facil.txt` (média: `100 0.1 2`, difícil: `160 0.1 3`)
- Resolver (modelo principal): `python mis.py instancias/dificil.txt`
- Comparativo (restrições de clique): `python mis_cliques.py instancias/dificil.txt`

Resultados obtidos (1 núcleo, CBC padrão):

| Instância | n | m | Relaxação | Ótimo | Nós | Tempo (s) |
|---|---|---|---|---|---|---|
| Fácil | 20 | 38 | 10,0 | 9 | 0 | 0,01 |
| Média | 100 | 484 | 50,0 | 32 | 100 | 2,28 |
| Difícil | 160 | 1246 | 80,0 | 38 | 49.120 | 215,66 |
