"""
MIS — formulação reforçada por cliques (comparativo).
Troca as restrições de aresta x_u + x_v <= 1 por restrições de clique:
    sum_{v in K} x_v <= 1   para cada clique K de uma cobertura das arestas.
Um conjunto independente só pode ter no máximo 1 vértice de cada clique.
"""
import sys, time
import networkx as nx
import pulp
from mis import ler_dimacs


def cobertura_por_cliques(V, E):
    """Cobre todas as arestas com cliques maximais (heurística gulosa)."""
    G = nx.Graph(); G.add_nodes_from(V); G.add_edges_from(E)
    descobertas = {frozenset(e) for e in E}
    cliques = []
    for (u, v) in E:
        if frozenset((u, v)) not in descobertas:
            continue
        K = {u, v}
        candidatos = set(G[u]) & set(G[v])
        while candidatos:  # estende o clique de forma gulosa
            w = max(candidatos, key=lambda c: len(set(G[c]) & candidatos))
            K.add(w); candidatos &= set(G[w])
        cliques.append(sorted(K))
        for a in K:
            for b in K:
                if a < b:
                    descobertas.discard(frozenset((a, b)))
    return cliques


def resolver(caminho, limite_tempo=900):
    V, E = ler_dimacs(caminho)
    cliques = cobertura_por_cliques(V, E)
    resultados = {}
    for relax in (True, False):
        m = pulp.LpProblem("MIS_cliques", pulp.LpMaximize)
        x = pulp.LpVariable.dicts("x", V, 0, 1, pulp.LpContinuous if relax else pulp.LpBinary)
        m += pulp.lpSum(x.values())
        for i, K in enumerate(cliques):
            m += pulp.lpSum(x[v] for v in K) <= 1, f"clique_{i}"
        t = time.perf_counter()
        m.solve(pulp.PULP_CBC_CMD(msg=False, timeLimit=limite_tempo, logPath=caminho + (".clq_lp.log" if relax else ".clq.log")))
        resultados["lp" if relax else "ip"] = (pulp.value(m.objective), time.perf_counter() - t)
    print(f"{caminho}: {len(cliques)} restrições de clique (vs {len(E)} de aresta)")
    print(f"Relaxação linear: {resultados['lp'][0]:.2f}")
    print(f"Ótimo inteiro   : {resultados['ip'][0]:.0f}  em {resultados['ip'][1]:.2f}s")


if __name__ == "__main__":
    resolver(sys.argv[1])
