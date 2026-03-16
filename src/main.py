"""
main.py — Point d'entree du projet de comparaison d'algorithmes de chemin.

Charge les trois cartes de grille, execute chaque algorithme implemente,
affiche une vue terminale coloree et sauvegarde des figures matplotlib.

Images produites (dans results/)
---------------------------------
Pour chaque grille et chaque algorithme :
    resultats_{grille}_{algo}.png      — chemin individuel
Pour chaque grille :
    resultats_{grille}_comparaison.png — tous les algorithmes cote a cote

Utilisation
-----------
Lancer depuis le repertoire ``src/`` ::

    python main.py
"""

import os
import time

from grid                  import load_grid
from algorithms.astar      import astar_search
from algorithms.greedy     import greedy_search
from algorithms.genetic    import genetic_search
from visualizer            import afficher_chemin, tracer_grille, comparer_resultats

# ── Configuration ──────────────────────────────────────────────────────────────

_ICI       = os.path.dirname(os.path.abspath(__file__))
REP_DATA   = os.path.join(_ICI, "..", "data")
REP_SORTIE = os.path.join(_ICI, "..", "results")
os.makedirs(REP_SORTIE, exist_ok=True)

FICHIERS_GRILLE = ["grid1.txt", "grid2.txt", "grid3.txt"]

# {nom_affichage: (fonction, slug_fichier)}
# Le slug sert a nommer les fichiers images de facon unique et lisible.
ALGORITHMES: dict[str, tuple[callable, str]] = {
    "A*":        (astar_search,   "astar"),
    "Glouton":   (greedy_search,  "glouton"),
    "Genetique": (genetic_search, "genetique"),
}


# ── Fonctions utilitaires ──────────────────────────────────────────────────────

def executer_algorithme(
    nom:     str,
    fn:      callable,
    grille:  list[list[str]],
    depart:  tuple[int, int],
    arrivee: tuple[int, int],
) -> tuple[list[tuple[int, int]], set[tuple[int, int]], float]:
    """Executer *fn* sur la grille et retourner ``(chemin, explores, duree_ms)``.

    Gere les deux signatures de retour possibles :
        - complete : ``fn() -> (chemin, explores)``
        - simple   : ``fn() -> chemin``  (algorithmes des collegues)

    Parametres
    ----------
    nom     : str             Nom affiche dans la sortie console.
    fn      : callable        Fonction de l'algorithme.
    grille  : list[list[str]]
    depart  : tuple[int, int]
    arrivee : tuple[int, int]

    Retourne
    --------
    chemin   : list[tuple[int, int]]
    explores : set[tuple[int, int]]
    duree    : float   Temps d'execution en millisecondes.
    """
    t0       = time.perf_counter()
    resultat = fn(grille, depart, arrivee)
    duree    = (time.perf_counter() - t0) * 1_000

    if isinstance(resultat, tuple) and len(resultat) == 2:
        chemin, explores = resultat
    else:
        # L'algorithme retourne uniquement la liste du chemin
        chemin, explores = resultat, set()

    statut = f"{len(chemin) - 1} pas" if chemin else "aucun chemin trouve"
    print(f"    [{nom:<12}]  {statut:<22}  {duree:.3f} ms")

    return chemin, explores, duree


# ── Fonction principale ────────────────────────────────────────────────────────

def main() -> None:
    for fichier in FICHIERS_GRILLE:
        grille, depart, arrivee = load_grid(os.path.join(REP_DATA, fichier))
        nom_grille = fichier.replace(".txt", "")

        print(f"\n{'=' * 54}")
        print(f"  Grille : {fichier}   depart={depart}   arrivee={arrivee}")
        print(f"{'=' * 54}")

        chemins:   dict[str, list[tuple[int, int]]] = {}
        carte_exp: dict[str, set[tuple[int, int]]]  = {}

        # ── Execution de chaque algorithme ──────────────────────────────────
        for nom_algo, (fn_algo, _slug) in ALGORITHMES.items():
            chemin, explores, _ = executer_algorithme(
                nom_algo, fn_algo, grille, depart, arrivee
            )
            chemins[nom_algo]   = chemin
            carte_exp[nom_algo] = explores

        # ── Affichage terminal ──────────────────────────────────────────────
        for nom_algo, chemin in chemins.items():
            afficher_chemin(
                grille, chemin, depart, arrivee,
                titre    = f"{nom_algo} - {fichier}",
                explores = carte_exp[nom_algo],
            )

        # ── Images individuelles : results/resultats_{grille}_{algo}.png ────
        for nom_algo, (_, slug) in ALGORITHMES.items():
            nom_fichier = f"resultats_{nom_grille}_{slug}.png"
            tracer_grille(
                grille, chemins[nom_algo], depart, arrivee,
                titre    = f"{nom_algo} - {fichier}",
                explores = carte_exp[nom_algo],
                sauver   = os.path.join(REP_SORTIE, nom_fichier),
            )

        # ── Image de comparaison : results/resultats_{grille}_comparaison.png
        comparer_resultats(
            grille, chemins, depart, arrivee,
            carte_explores = carte_exp,
            sauver = os.path.join(REP_SORTIE, f"resultats_{nom_grille}_comparaison.png"),
        )


if __name__ == "__main__":
    main()
