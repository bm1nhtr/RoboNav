"""
genetic.py — Algorithme genetique pour la recherche de chemin.

Principe
--------
Un algorithme genetique fait evoluer une population d'individus
(sequences de mouvements) sur plusieurs generations afin de minimiser
une fonction de fitness.

Cycle d'evolution
-----------------
1. Initialisation  — creation d'une population aleatoire.
2. Evaluation      — calcul du score fitness de chaque individu.
3. Selection       — conservation des meilleurs individus.
4. Croisement      — generation d'enfants a partir de deux parents.
5. Mutation        — modification aleatoire de certains mouvements.
6. Repetition      — retour a l'etape 2 jusqu'a convergence ou arrivee atteinte.

Fonction de fitness
-------------------
    fitness(chemin) = distance_manhattan(dernier_noeud, arrivee)
                    + 0.1 * longueur_du_chemin

    On penalise les chemins trop longs pour favoriser des solutions concises.

Parametres par defaut
---------------------
    taille_pop  = 50   individus par generation
    nb_pas      = 20   mouvements par individu
    generations = 100  nombre de generations

Interface publique
------------------
    genetic_search(grille, depart, arrivee) -> chemin

    Signature compatible avec le pipeline de ``main.py``.
"""

import random

# Mouvements cardinaux possibles : droite, gauche, bas, haut
MOUVEMENTS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


# ── Heuristique ────────────────────────────────────────────────────────────────

def heuristique(a: tuple[int, int], b: tuple[int, int]) -> int:
    """Distance de Manhattan entre deux positions.

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


# ── Construction du chemin ────────────────────────────────────────────────────

def appliquer_mouvements(
    depart:     tuple[int, int],
    mouvements: list[tuple[int, int]],
    grille:     list[list[str]],
) -> list[tuple[int, int]]:
    """Appliquer une sequence de mouvements depuis *depart* pour construire un chemin.

    Les mouvements qui sortent de la grille ou tombent sur un obstacle
    sont ignores silencieusement.

    Parametres
    ----------
    depart : tuple[int, int]
        Position initiale ``(x, y)``.
    mouvements : list[tuple[int, int]]
        Sequence de deplacements ``(dx, dy)`` a appliquer.
    grille : list[list[str]]
        Grille 2D indexee comme ``grille[y][x]``.

    Retourne
    --------
    list[tuple[int, int]]
        Chemin construit, incluant *depart*.
    """
    x, y = depart
    chemin = [depart]

    for dx, dy in mouvements:
        nx, ny = x + dx, y + dy

        # Verifier les limites de la grille et l'absence d'obstacle
        if 0 <= ny < len(grille) and 0 <= nx < len(grille[0]):
            if grille[ny][nx] != "X":
                x, y = nx, ny
                chemin.append((x, y))

    return chemin


# ── Fitness ───────────────────────────────────────────────────────────────────

def evaluer(chemin: list[tuple[int, int]], arrivee: tuple[int, int]) -> float:
    """Evaluer la qualite d'un chemin (plus le score est bas, meilleur est le chemin).

    Parametres
    ----------
    chemin : list[tuple[int, int]]
        Chemin construit par ``appliquer_mouvements``.
    arrivee : tuple[int, int]
        Coordonnees ``(x, y)`` de l'arrivee.

    Retourne
    --------
    float
        Score = distance_manhattan(derniere_case, arrivee) + 0.1 * longueur.
        Un score de 0 signifie que l'arrivee est atteinte avec le chemin minimal.
    """
    derniere_case = chemin[-1]
    distance = heuristique(derniere_case, arrivee)
    # Penalite sur la longueur pour decourager les chemins inutilement longs
    return distance + 0.1 * len(chemin)


# ── Operateurs genetiques ─────────────────────────────────────────────────────

def individu_aleatoire(nb_pas: int) -> list[tuple[int, int]]:
    """Creer un individu aleatoire (sequence de mouvements).

    Parametres
    ----------
    nb_pas : int
        Nombre de mouvements dans l'individu.

    Retourne
    --------
    list[tuple[int, int]]
        Sequence de *nb_pas* deplacements choisis aleatoirement dans MOUVEMENTS.
    """
    return [random.choice(MOUVEMENTS) for _ in range(nb_pas)]


def muter(
    individu: list[tuple[int, int]],
    taux:     float = 0.1,
) -> list[tuple[int, int]]:
    """Muter un individu en remplacant aleatoirement certains mouvements.

    Parametres
    ----------
    individu : list[tuple[int, int]]
        Sequence de mouvements a muter.
    taux : float
        Probabilite de mutation par mouvement (defaut : 10 %).

    Retourne
    --------
    list[tuple[int, int]]
        Nouvel individu mute (l'original n'est pas modifie).
    """
    return [
        random.choice(MOUVEMENTS) if random.random() < taux else mouvement
        for mouvement in individu
    ]


def croisement(
    parent1: list[tuple[int, int]],
    parent2: list[tuple[int, int]],
) -> list[tuple[int, int]]:
    """Croisement monopoint entre deux parents pour produire un enfant.

    Parametres
    ----------
    parent1, parent2 : list[tuple[int, int]]
        Sequences de mouvements des deux parents.

    Retourne
    --------
    list[tuple[int, int]]
        Enfant constitue du debut de *parent1* et de la fin de *parent2*.
    """
    point_coupe = random.randint(0, len(parent1) - 1)
    return parent1[:point_coupe] + parent2[point_coupe:]


# ── Algorithme genetique principal ────────────────────────────────────────────

def genetic_search(
    grille:     list[list[str]],
    depart:     tuple[int, int],
    arrivee:    tuple[int, int],
    taille_pop: int = 50,
    nb_pas:     int = 20,
    generations: int = 100,
) -> list[tuple[int, int]]:
    """Trouver un chemin de *depart* a *arrivee* par algorithme genetique.

    Parametres
    ----------
    grille : list[list[str]]
        Grille 2D indexee comme ``grille[y][x]``.
    depart : tuple[int, int]
        Coordonnees ``(x, y)`` du point de depart.
    arrivee : tuple[int, int]
        Coordonnees ``(x, y)`` du point d'arrivee.
    taille_pop : int
        Nombre d'individus par generation (defaut : 50).
    nb_pas : int
        Nombre de mouvements par individu (defaut : 20).
    generations : int
        Nombre de generations d'evolution (defaut : 100).

    Retourne
    --------
    list[tuple[int, int]]
        Meilleur chemin trouve. Peut ne pas etre optimal selon les parametres.
    """
    # Initialisation de la population avec des individus aleatoires
    population = [individu_aleatoire(nb_pas) for _ in range(taille_pop)]

    for _generation in range(generations):
        # Evaluer chaque individu et construire son chemin
        scores = []
        for ind in population:
            chemin = appliquer_mouvements(depart, ind, grille)
            score  = evaluer(chemin, arrivee)

            # Arret immediat si l'arrivee est atteinte
            if heuristique(chemin[-1], arrivee) == 0:
                return chemin

            scores.append((score, ind))

        # Trier par score croissant (meilleur score = plus bas)
        scores.sort(key=lambda x: x[0])

        # Selection des 10 meilleurs individus (elitisme)
        elite = [ind for _, ind in scores[:10]]

        # Construction de la nouvelle population
        nouvelle_population = list(elite)  # on conserve l'elite

        # Completer avec des enfants issus de croisement + mutation
        while len(nouvelle_population) < taille_pop:
            p1    = random.choice(elite)
            p2    = random.choice(elite)
            enfant = muter(croisement(p1, p2))
            nouvelle_population.append(enfant)

        population = nouvelle_population

    # Aucune solution parfaite trouvee : retourner le meilleur chemin final
    meilleur = min(
        population,
        key=lambda ind: evaluer(appliquer_mouvements(depart, ind, grille), arrivee),
    )
    return appliquer_mouvements(depart, meilleur, grille)
