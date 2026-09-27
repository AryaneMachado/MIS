"""Gera as 3 instâncias do MIS (grafos aleatórios Erdős–Rényi G(n,p)) em formato DIMACS."""
import random

def gerar(n, p, seed, caminho):
    rng = random.Random(seed)
    arestas = [(i, j) for i in range(1, n + 1) for j in range(i + 1, n + 1) if rng.random() < p]
    with open(caminho, "w") as f:
        f.write(f"c Grafo aleatorio G(n={n}, p={p}), seed={seed}\n")
        f.write(f"p edge {n} {len(arestas)}\n")
        for u, v in arestas:
            f.write(f"e {u} {v}\n")
    print(f"{caminho}: {n} vertices, {len(arestas)} arestas")

if __name__ == "__main__":
    import sys
    gerar(int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
