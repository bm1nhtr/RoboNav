"""
main.py — Point d'entree du projet de comparaison d'algorithmes de chemin.

Charge les trois cartes de grille, execute chaque algorithme implemente,
affiche une vue terminale coloree et sauvegarde une figure matplotlib de
comparaison par grille.

Utilisation
-----------
Lancer depuis le repertoire ``src/`` ::

    python main.py

Sorties
-------
- Grille ASCII coloree dans le terminal pour chaque couple (grille, algorithme).
- Une image ``resultats_<nom_grille>.png`` par grille, sauvegardee a la racine
  du projet.
"""

import os
import time

from grid                import load_grid
from algorithms.astar    import astar_search
from visualizer          import afficher_chemin, comparer_resultats

# ── Configuration ──────────────────────────────────────────────────────────────

# Chemin vers data/ relatif a ce fichier, independant du repertoire courant.
_ICI       = os.path.dirname(os.path.abspath(__file__))
REP_DATA   = os.path.join(_ICI, "..", "data")
REP_SORTIE = os.path.join(_ICI, "..", "results")   # figures sauvegardees dans results/
os.makedirs(REP_SORTIE, exist_ok=True)

FICHIERS_GRILLE = ["grid1.txt", "grid2.txt", "grid3.txt"]

# Algorithmes a evaluer : {nom_affichage: fonction}
ALGORITHMES: dict[str, callable] = {
    "A*": astar_search,
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

    Gere les deux signatures possibles de retour :
        - nouvelle : ``fn() -> (chemin, explores)``
        - legacy/stub : ``fn() -> chemin``


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
    t0      = time.perf_counter()
    resultat = fn(grille, depart, arrivee)
    duree   = (time.perf_counter() - t0) * 1_000

    if isinstance(resultat, tuple) and len(resultat) == 2:
        chemin, explores = resultat
    else:
        # Legacy / stub : la fonction retourne uniquement la liste du chemin
        chemin, explores = resultat, set()

    statut = f"{len(chemin) - 1} pas" if chemin else "aucun chemin trouve"
    print(f"    [{nom:<10}]  {statut:<22}  {duree:.3f} ms")

    return chemin, explores, duree


# ── Fonction principale ────────────────────────────────────────────────────────

def main() -> None:
    for fichier in FICHIERS_GRILLE:
        chemin_fichier = os.path.join(REP_DATA, fichier)
        grille, depart, arrivee = load_grid(chemin_fichier)
        nom_grille = fichier.replace(".txt", "")

        print(f"\n{'=' * 50}")
        print(f"  Grille : {fichier}   depart={depart}   arrivee={arrivee}")
        print(f"{'=' * 50}")

        chemins:      dict[str, list[tuple[int, int]]] = {}
        carte_exp:    dict[str, set[tuple[int, int]]]  = {}

        for nom_algo, fn_algo in ALGORITHMES.items():
            chemin, explores, _ = executer_algorithme(
                nom_algo, fn_algo, grille, depart, arrivee
            )
            chemins[nom_algo]   = chemin
            carte_exp[nom_algo] = explores

        # ── Affichage terminal (un bloc par algorithme) ─────────────────────
        for nom_algo, chemin in chemins.items():
            afficher_chemin(
                grille, chemin, depart, arrivee,
                titre    = f"{nom_algo} - {fichier}",
                explores = carte_exp[nom_algo],
            )

        # ── Comparaison graphique (sauvegardee a la racine du projet) ───────
        sortie = os.path.join(REP_SORTIE, f"resultats_{nom_grille}.png")
        comparer_resultats(
            grille, chemins, depart, arrivee,
            carte_explores = carte_exp,
            sauver         = sortie,
        )


if __name__ == "__main__":
    main()
