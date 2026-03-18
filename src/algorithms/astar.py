"""
astar.py — Algorithme de recherche de chemin A*.

Implemente la recherche A* avec l'heuristique de distance de Manhattan.

Fonction d'evaluation
---------------------
    f(n) = g(n) + h(n)

    g(n) — cout exact (nombre de pas) depuis le noeud de depart jusqu'a n.
            Chaque deplacement a un cout uniforme de 1.
    h(n) — heuristique admissible : distance de Manhattan de n vers l'arrivee.
            Admissible  -> h(n) ne surestime jamais le cout reel.
            Consistante -> h(n) <= cout(n, n') + h(n') pour tout successeur n'.
            Ces deux proprietes garantissent qu'A* trouve le chemin optimal.

Complexite (pire cas)
---------------------
    Temps  : O(b^d)  ou b = facteur de branchement (<= 4), d = profondeur solution.
    Espace : O(b^d)  — tous les noeuds sont conserves en memoire (tas + dicts).

Interface publique
------------------
    astar_search(grille, depart, arrivee) -> (chemin, explores)

    Compatible avec l'API generique du visualiseur dans ``visualizer.py``.
"""

import heapq

from grid import get_neighbors


# ── Heuristique ────────────────────────────────────────────────────────────────

def heuristique(a: tuple[int, int], b: tuple[int, int]) -> int:
    """Distance de Manhattan entre deux cases de la grille.

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


# ── Recherche A* ───────────────────────────────────────────────────────────────

def astar_search(
    grille:  list[list[str]],
    depart:  tuple[int, int],
    arrivee: tuple[int, int],
) -> tuple[list[tuple[int, int]], set[tuple[int, int]]]:
    """Trouver le chemin le plus court de *depart* a *arrivee* avec A*.

    La liste ouverte est un tas-min ordonne par ``f = g + h``.
    Les egalites sur ``f`` sont departageees par ``g`` (on prefere les noeuds
    geometriquement plus proches de l'arrivee, c'est-a-dire avec un g plus grand).

    Parametres
    ----------
    grille : list[list[str]]
        Grille 2D indexee comme ``grille[y][x]``.
    depart : tuple[int, int]
        Coordonnees ``(x, y)`` du point de depart.
    arrivee : tuple[int, int]
        Coordonnees ``(x, y)`` du point d'arrivee.

    Retourne
    --------
    chemin : list[tuple[int, int]]
        Liste ordonnee de cases ``(x, y)`` de *depart* a *arrivee* (inclus).
        Liste vide si aucun chemin n'existe.
    explores : set[tuple[int, int]]
        Toutes les cases entierement developpees (extraites du tas) pendant
        la recherche — utile pour visualiser le front d'exploration.
    """
    # Entrees du tas : (f, g, noeud)
    # Stocker g evite de le recalculer et assure un departage deterministe.
    tas_ouvert: list[tuple[int, int, tuple[int, int]]] = []
    heapq.heappush(tas_ouvert, (heuristique(depart, arrivee), 0, depart))

    # Meilleur cout g connu pour atteindre chaque noeud
    cout_g: dict[tuple[int, int], int] = {depart: 0}

    # Predecesseur de chaque noeud sur le chemin le moins couteux
    precedent: dict[tuple[int, int], tuple[int, int] | None] = {depart: None}

    # Noeuds entierement developpes (liste fermee)
    explores: set[tuple[int, int]] = set()

    while tas_ouvert:
        _f, g, courant = heapq.heappop(tas_ouvert)

        # Ignorer les entrees perimees (noeud deja developpe avec un g inferieur)
        if courant in explores:
            continue

        explores.add(courant)

        if courant == arrivee:
            return _reconstruire_chemin(precedent, arrivee), explores

        for voisin in get_neighbors(grille, courant):
            g_tentative = g + 1  # cout de deplacement uniforme = 1

            if g_tentative < cout_g.get(voisin, float("inf")):
                # Nouveau chemin moins couteux vers ce voisin — on l'enregistre
                cout_g[voisin]    = g_tentative
                precedent[voisin] = courant
                f_voisin = g_tentative + heuristique(voisin, arrivee)
                heapq.heappush(tas_ouvert, (f_voisin, g_tentative, voisin))

    # Tous les noeuds accessibles ont ete explores sans trouver l'arrivee
    return [], explores


# ── Fonctions internes ────────────────────────────────────────────────────────

def _reconstruire_chemin(
    precedent: dict[tuple[int, int], tuple[int, int] | None],
    arrivee:   tuple[int, int],
) -> list[tuple[int, int]]:
    """Remonter la chaine *precedent* pour reconstruire le chemin solution."""
    chemin: list[tuple[int, int]] = []
    noeud: tuple[int, int] | None = arrivee

    while noeud is not None:
        chemin.append(noeud)
        noeud = precedent[noeud]

    chemin.reverse()
    return chemin
