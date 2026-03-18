"""
greedy.py — Algorithme de recherche gloutonne (Greedy Best-First Search).

Principe
--------
La recherche gloutonne explore toujours le voisin qui semble le plus
proche de l'arrivee selon l'heuristique h(n), sans tenir compte du cout
deja paye g(n).

Avantages / Limites
-------------------
- Tres rapide en pratique sur des grilles simples.
- Ni optimale (ne garantit pas le chemin le plus court) ni complete
  (peut boucler ou rester bloque sur certaines configurations).

Heuristique utilisee
--------------------
Distance de Manhattan : |ax - bx| + |ay - by|

Interface publique
------------------
    greedy_search(grille, depart, arrivee) -> chemin

    Signature compatible avec le pipeline de ``main.py``.
"""


# ── Heuristique ───────────────────────────────────────────────────────────────

def heuristique(a: tuple[int, int], b: tuple[int, int]) -> int:
    """Distance de Manhattan entre deux cases.

    Parametres
    ----------
    a, b : tuple[int, int]
        Coordonnees ``(x, y)`` dans la grille.

    Retourne
    --------
    int
        ``|ax - bx| + |ay - by|``
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ── Recherche gloutonne ───────────────────────────────────────────────────────

def greedy_search(
    grid:  list[list[str]],
    start: tuple[int, int],
    goal:  tuple[int, int],
) -> list[tuple[int, int]]:
    """Trouver un chemin de *start* a *goal* par recherche gloutonne.

    A chaque etape, on choisit le voisin le plus proche de *goal* selon
    l'heuristique de Manhattan, sans backtracking.

    Parametres
    ----------
    grid : list[list[str]]
        Grille 2D indexee comme ``grid[y][x]``.
    start : tuple[int, int]
        Coordonnees ``(x, y)`` du point de depart.
    goal : tuple[int, int]
        Coordonnees ``(x, y)`` du point d'arrivee.

    Retourne
    --------
    list[tuple[int, int]]
        Liste ordonnee de cases ``(x, y)`` constituant le chemin trouve.
        Peut ne pas etre le chemin optimal.
    """
    path = [start]
    current = start

    while current != goal:
        x, y = current

        # Generation des quatre voisins cardinaux
        neighbors = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ]

        # Filtrer : garder uniquement les cases dans la grille et non-obstacles
        valid_neighbors = [
            (nx, ny)
            for nx, ny in neighbors
            if 0 <= ny < len(grid)
            and 0 <= nx < len(grid[0])
            and grid[ny][nx] != "X"
        ]

        # Aucun voisin accessible : chemin partiel retourne
        if not valid_neighbors:
            return path

        # Selectionner le voisin le plus proche de l'arrivee
        best_neighbor = min(valid_neighbors, key=lambda n: heuristique(n, goal))

        path.append(best_neighbor)
        current = best_neighbor

    return path
