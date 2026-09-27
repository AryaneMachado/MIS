"""
Problema do Conjunto Independente (Estável) Máximo — MIS
Modelo de Programação Linear Inteira em PuLP, resolvido com CBC.

    max  sum_{v in V} x_v
    s.a. x_u + x_v <= 1        para toda aresta (u,v) in E
         x_v in {0,1}          para todo v in V
"""
import sys
import time
import pulp


def ler_dimacs(caminho):
    """Lê um grafo no formato DIMACS: 'p edge n m' e linhas 'e u v'."""
    n, arestas = 0, []
    with open(caminho) as f:
        for linha in f:
            partes = linha.split()
            if not partes or partes[0] == "c":
                continue
            if partes[0] == "p":
                n = int(partes[2])
            elif partes[0] == "e":
                arestas.append((int(partes[1]), int(partes[2])))
    return list(range(1, n + 1)), arestas


def construir_modelo(V, E, relaxado=False):
    """Monta o modelo. relaxado=True troca x_v in {0,1} por 0 <= x_v <= 1 (relaxação linear)."""
    modelo = pulp.LpProblem("MIS", pulp.LpMaximize)
    categoria = pulp.LpContinuous if relaxado else pulp.LpBinary
    # Variável de decisão: x[v] = 1 se o vértice v entra no conjunto
    x = pulp.LpVariable.dicts("x", V, lowBound=0, upBound=1, cat=categoria)
    # Função objetivo: maximizar a quantidade de vértices escolhidos
    modelo += pulp.lpSum(x[v] for v in V), "Tamanho_do_conjunto"
    # Restrição: dois vértices vizinhos não podem estar ambos no conjunto
    for (u, v) in E:
        modelo += x[u] + x[v] <= 1, f"aresta_{u}_{v}"
    return modelo, x


def resolver(caminho, limite_tempo=900):
    V, E = ler_dimacs(caminho)

    # 1) Relaxação linear (limite superior do PLI)
    lp, x_lp = construir_modelo(V, E, relaxado=True)
    lp.solve(pulp.PULP_CBC_CMD(msg=False))
    valor_lp = pulp.value(lp.objective)

    # 2) Modelo inteiro resolvido por Branch-and-Cut (CBC)
    modelo, x = construir_modelo(V, E)
    solver = pulp.PULP_CBC_CMD(msg=False, timeLimit=limite_tempo, logPath=caminho + ".log")
    inicio = time.perf_counter()
    modelo.solve(solver)
    tempo = time.perf_counter() - inicio

    escolhidos = [v for v in V if x[v].value() > 0.5]
    # Verificação: nenhuma aresta com os dois extremos escolhidos
    S = set(escolhidos)
    valido = all(not (u in S and v in S) for (u, v) in E)

    print(f"Instância          : {caminho}")
    print(f"Vértices / Arestas : {len(V)} / {len(E)}")
    print(f"Variáveis / Restr. : {len(modelo.variables())} / {len(modelo.constraints)}")
    print(f"Status             : {pulp.LpStatus[modelo.status]}")
    print(f"Relaxação linear   : {valor_lp:.2f}")
    print(f"Ótimo inteiro α(G) : {len(escolhidos)}")
    print(f"Gap relaxação      : {100*(valor_lp-len(escolhidos))/len(escolhidos):.1f}%")
    print(f"Tempo (s)          : {tempo:.2f}")
    print(f"Solução válida?    : {valido}")
    print(f"Conjunto           : {sorted(escolhidos)}")
    return dict(n=len(V), m=len(E), lp=valor_lp, opt=len(escolhidos), tempo=tempo,
                status=pulp.LpStatus[modelo.status], conjunto=sorted(escolhidos))


if __name__ == "__main__":
    resolver(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 900)
