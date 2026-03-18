"""
grid.py — Modele de grille et utilitaires spatiaux.

Definit la representation de grille 2D partagee par tous les algorithmes
de recherche de chemin, et expose les deux fonctions essentielles :
    - load_grid()     : charger un fichier texte en grille
    - get_neighbors() : renvoyer les voisins accessibles d'une case

Convention de coordonnees
-------------------------
grid[y][x]  avec l'origine (0, 0) en haut a gauche.
x croissant vers la droite, y croissant vers le bas.

Tokens des cases
----------------
S — case depart
G — case arrivee
X — obstacle (infranchissable)
0 — case libre
"""

# ── Constantes ─────────────────────────────────────────────────────────────────

OBSTACLE = "X"
DEPART   = "S"
ARRIVEE  = "G"

# Quatre directions cardinales : droite, gauche, bas, haut
_DIRECTIONS: list[tuple[int, int]] = [(1, 0), (-1, 0), (0, 1), (0, -1)]


# ── API publique ───────────────────────────────────────────────────────────────

def load_grid(chemin: str) -> tuple[list[list[str]], tuple[int, int], tuple[int, int]]:
    """Analyser un fichier texte en grille 2D et localiser le depart et l'arrivee.

    Format du fichier — tokens separes par des espaces, une ligne par rangee ::

        S 0 X 0
        0 0 X G

    Parametres
    ----------
    chemin : str
        Chemin vers le fichier ``.txt`` de la grille.

    Retourne
    --------
    grille : list[list[str]]
        Tableau 2D indexe comme ``grille[y][x]``.
    depart : tuple[int, int]
        Coordonnees ``(x, y)`` de la case depart ``'S'``.
    arrivee : tuple[int, int]
        Coordonnees ``(x, y)`` de la case arrivee ``'G'``.

    Leve
    ----
    ValueError
        Si le fichier ne contient pas a la fois un depart (``'S'``) et une
        arrivee (``'G'``).
    FileNotFoundError
        Si *chemin* ne pointe pas vers un fichier existant.
    """
    grille: list[list[str]] = []
    depart:  tuple[int, int] | None = None
    arrivee: tuple[int, int] | None = None

    with open(chemin) as f:
        for y, ligne in enumerate(f):
            rangee = ligne.strip().split()
            for x, token in enumerate(rangee):
                if token == DEPART:
                    depart = (x, y)
                elif token == ARRIVEE:
                    arrivee = (x, y)
            grille.append(rangee)

    if depart is None or arrivee is None:
        raise ValueError(
            f"Le fichier '{chemin}' doit contenir un depart ('{DEPART}') "
            f"et une arrivee ('{ARRIVEE}')."
        )

    return grille, depart, arrivee


def get_neighbors(
    grille: list[list[str]],
    pos:    tuple[int, int],
) -> list[tuple[int, int]]:
    """Renvoyer les voisins orthogonaux accessibles de *pos* dans *grille*.

    Seules les quatre directions cardinales sont considerees (pas de diagonales).
    Les cases marquees ``OBSTACLE`` (``'X'``) et les positions hors limites sont
    exclues.

    Parametres
    ----------
    grille : list[list[str]]
        Tableau 2D indexe comme ``grille[y][x]``.
    pos : tuple[int, int]
        Coordonnees ``(x, y)`` de la case courante.

    Retourne
    --------
    list[tuple[int, int]]
        Liste des coordonnees ``(x, y)`` voisines valides, dans l'ordre :
        droite -> gauche -> bas -> haut.

    Exemples
    --------
    >>> grille = [["S", "0"], ["X", "G"]]
    >>> get_neighbors(grille, (0, 0))
    [(1, 0)]
    """
    x, y  = pos                                    # coordonnees de la case courante
    lignes = len(grille)                           # nombre de lignes de la grille
    cols   = len(grille[0]) if lignes > 0 else 0  # nombre de colonnes (0 si grille vide)

    return [
        (x + dx, y + dy)
        for dx, dy in _DIRECTIONS          # pour chaque direction cardinale
        if 0 <= x + dx < cols              # verif : x dans les bornes de la grille
        and 0 <= y + dy < lignes           # verif : y dans les bornes de la grille
        and grille[y + dy][x + dx] != OBSTACLE  # verif : case non obstacle
    ]
