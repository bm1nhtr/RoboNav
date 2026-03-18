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


# ── Fonction execution complete ────────────────────────────────────────────────────────

def execution_complete() -> None:
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

# ── Menu interactif ───────────────────────────────────────────────────────────

def afficher_menu():
    print("\n===== MENU =====")
    print("1 - Mode interactif")
    print("2 - Affichage complet (tous les algos)")
    print("3 - Quitter")


# ── Fonction interactive principal ───────────────────────────────────────────────────────────

def main():

    while True:

        afficher_menu()
        choix = input("Votre choix : ")

        # ── Mode interactif ────────────────────────────────────────────────
        if choix == "1":

            # ── choix de l'algorithme ───────────────────────────────
            print("\nChoisir un algorithme :")
            print("1 - A*")
            print("2 - Glouton")
            print("3 - Genetique")

            choix_algo = input("Votre choix : ")

            if choix_algo == "1":
                nom_algo = "A*"
            elif choix_algo == "2":
                nom_algo = "Glouton"
            elif choix_algo == "3":
                nom_algo = "Genetique"
            else:
                print("Choix invalide")
                continue

            # ── choix de la grille ───────────────────────────────
            print("\nChoisir une grille :")
            print("1 - grid1")
            print("2 - grid2")
            print("3 - grid3")
            print("4 - Toutes les grilles")

            choix_grille = input("Votre choix : ")

            fn_algo, _ = ALGORITHMES[nom_algo]

            # ── cas : toutes les grilles ─────────────────────────
            if choix_grille == "4":

                for fichier in FICHIERS_GRILLE:

                    print("\n==============================")
                    print(f"{nom_algo} - {fichier}")
                    print("==============================")

                    grille, depart, arrivee = load_grid(os.path.join(REP_DATA, fichier))

                    chemin, explores, _ = executer_algorithme(
                        nom_algo, fn_algo, grille, depart, arrivee
                    )

                    afficher_chemin(
                        grille, chemin, depart, arrivee,
                        titre=nom_algo,
                        explores=explores
                    )

            # ── cas : une seule grille ─────────────────────────
            else:

                if choix_grille == "1":
                    fichier = "grid1.txt"
                elif choix_grille == "2":
                    fichier = "grid2.txt"
                elif choix_grille == "3":
                    fichier = "grid3.txt"
                else:
                    print("Choix invalide")
                    continue

                grille, depart, arrivee = load_grid(os.path.join(REP_DATA, fichier))

                chemin, explores, _ = executer_algorithme(
                    nom_algo, fn_algo, grille, depart, arrivee
                )

                afficher_chemin(
                    grille, chemin, depart, arrivee,
                    titre=nom_algo,
                    explores=explores
                )

        # ── Mode complet (code original) ───────────────────────────────────
        elif choix == "2":

            print("\nExecution complete...\n")
            execution_complete()

        # ── Quitter ────────────────────────────────────────────────────────
        elif choix == "3":
            print("Au revoir !")
            break

        else:
            print("Choix invalide")


# ── Lancement ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    main()
