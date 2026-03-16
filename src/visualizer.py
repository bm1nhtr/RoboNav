"""
visualizer.py — Utilitaires generiques de visualisation de grille.

Fournit trois fonctions publiques utilisables par n'importe quel algorithme
de recherche de chemin sans modification :

    afficher_chemin(...)    — affichage ASCII colore dans le terminal
    tracer_grille(...)      — affichage graphique via matplotlib
    comparer_resultats(...) — comparaison cote a cote avec matplotlib

Les trois partagent la meme signature principale ::

    fn(grille, chemin, depart, arrivee, *, titre="", explores=None)

Repli gracieux
--------------
Si matplotlib / numpy ne sont pas installes, ``tracer_grille`` et
``comparer_resultats`` se rabattent automatiquement sur ``afficher_chemin``
afin que le projet fonctionne meme sans ces dependances.

Legende des couleurs (terminal)
---------------------------------
  S — depart    (vert vif)
  G — arrivee   (magenta vif)
  * — chemin    (cyan vif)
  o — explore   (jaune vif)
  X — obstacle  (gris)
  . — libre     (blanc)
"""

from __future__ import annotations

# ── Import optionnel matplotlib ───────────────────────────────────────────────

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.colors import ListedColormap
    import numpy as np
    _MPL = True
except ImportError:
    _MPL = False

# ── Couleurs ANSI pour le terminal ────────────────────────────────────────────

_RESET = "\033[0m"
_COULEUR: dict[str, str] = {
    "depart":   "\033[92m",   # vert vif
    "arrivee":  "\033[95m",   # magenta vif
    "chemin":   "\033[96m",   # cyan vif
    "explore":  "\033[93m",   # jaune vif
    "obstacle": "\033[90m",   # gris
    "libre":    "\033[37m",   # blanc
}

# ── Codes de type de case pour matplotlib ─────────────────────────────────────

_LIBRE    = 0
_OBSTACLE = 1
_EXPLORE  = 2
_CHEMIN   = 3
_DEPART   = 4
_ARRIVEE  = 5

# Palette de couleurs partagee par toutes les fonctions matplotlib
_PALETTE = [
    "#F5F5F5",  # 0 — libre     (gris clair)
    "#2C2C2C",  # 1 — obstacle  (noir)
    "#FFD166",  # 2 — explore   (ambre)
    "#06D6A0",  # 3 — chemin    (turquoise)
    "#118AB2",  # 4 — depart    (bleu)
    "#EF476F",  # 5 — arrivee   (rose-rouge)
]


# ── API publique ───────────────────────────────────────────────────────────────

def afficher_chemin(
    grille:   list[list[str]],
    chemin:   list[tuple[int, int]],
    depart:   tuple[int, int],
    arrivee:  tuple[int, int],
    *,
    titre:    str = "",
    explores: set[tuple[int, int]] | None = None,
) -> None:
    """Afficher une representation ASCII coloree de la grille dans le terminal.

    Parametres
    ----------
    grille : list[list[str]]
        Tableau 2D indexe comme ``grille[y][x]``.
    chemin : list[tuple[int, int]]
        Sequence ordonnee de cases ``(x, y)`` sur le chemin solution.
    depart : tuple[int, int]
        Case depart ``(x, y)``.
    arrivee : tuple[int, int]
        Case arrivee ``(x, y)``.
    titre : str, optionnel
        En-tete affiche au-dessus de la grille.
    explores : set[tuple[int, int]], optionnel
        Cases visitees pendant la recherche (affichees en ``o`` jaune).
    """
    ensemble_chemin   = set(chemin)
    ensemble_explores = set(explores) if explores else set()

    if titre:
        print(f"\n{'-' * 36}")
        print(f"  {titre}")
        print(f"{'-' * 36}")

    for y, rangee in enumerate(grille):
        cases = []
        for x, brut in enumerate(rangee):
            symbole, couleur = _case_terminal(
                (x, y), brut, ensemble_chemin, ensemble_explores, depart, arrivee
            )
            cases.append(f"{couleur}{symbole}{_RESET}")
        print("  " + "  ".join(cases))

    _afficher_legende_terminal(explores is not None)

    if chemin:
        print(f"  Longueur du chemin : {len(chemin) - 1} pas")
    else:
        print("  Aucun chemin trouve.")


def tracer_grille(
    grille:   list[list[str]],
    chemin:   list[tuple[int, int]],
    depart:   tuple[int, int],
    arrivee:  tuple[int, int],
    *,
    titre:    str = "",
    explores: set[tuple[int, int]] | None = None,
    sauver:   str | None = None,
) -> None:
    """Afficher une grille graphique via matplotlib.

    Se replie sur :func:`afficher_chemin` si matplotlib n'est pas installe.

    Parametres
    ----------
    grille : list[list[str]]
        Tableau 2D indexe comme ``grille[y][x]``.
    chemin : list[tuple[int, int]]
        Chemin solution en cases ``(x, y)``.
    depart : tuple[int, int]
        Case depart ``(x, y)``.
    arrivee : tuple[int, int]
        Case arrivee ``(x, y)``.
    titre : str, optionnel
        Titre de la figure.
    explores : set[tuple[int, int]], optionnel
        Cases visitees pendant la recherche.
    sauver : str, optionnel
        Si fourni, sauvegarde la figure dans ce chemin de fichier.
    """
    if not _MPL:
        print("[visualiseur] matplotlib non disponible — affichage terminal utilise.")
        afficher_chemin(grille, chemin, depart, arrivee, titre=titre, explores=explores)
        return

    lignes, cols = len(grille), len(grille[0]) if grille else 0
    fig, ax = plt.subplots(figsize=(max(4, cols * 0.9), max(3, lignes * 0.9)))

    _dessiner_sur_axe(ax, grille, chemin, depart, arrivee, explores=explores, titre=titre)

    _ajouter_legende(ax)
    plt.tight_layout()

    if sauver:
        plt.savefig(sauver, dpi=150, bbox_inches="tight")
        print(f"[visualiseur] Figure sauvegardee -> '{sauver}'")
        plt.close(fig)
    else:
        plt.show()


def comparer_resultats(
    grille:       list[list[str]],
    resultats:    dict[str, list[tuple[int, int]]],
    depart:       tuple[int, int],
    arrivee:      tuple[int, int],
    *,
    carte_explores: dict[str, set[tuple[int, int]]] | None = None,
    sauver:         str | None = None,
) -> None:
    """Tracer des grilles cote a cote pour plusieurs resultats d'algorithmes.

    Parametres
    ----------
    grille : list[list[str]]
        Tableau 2D indexe comme ``grille[y][x]``.
    resultats : dict[str, list[tuple[int, int]]]
        Correspondance ``{nom_algorithme: chemin}``.
    depart, arrivee : tuple[int, int]
        Coordonnees ``(x, y)``.
    carte_explores : dict[str, set[tuple[int, int]]], optionnel
        Correspondance ``{nom_algorithme: ensemble_explores}``.
    sauver : str, optionnel
        Chemin de fichier pour sauvegarder la figure de comparaison.

    Exemples
    --------
    >>> comparer_resultats(
    ...     grille,
    ...     resultats={"A*": chemin_astar, "Glouton": chemin_glouton},
    ...     depart=depart, arrivee=arrivee,
    ...     carte_explores={"A*": exp_astar, "Glouton": exp_glouton},
    ... )
    """
    if not _MPL:
        for nom, chemin in resultats.items():
            exp = (carte_explores or {}).get(nom)
            afficher_chemin(grille, chemin, depart, arrivee, titre=nom, explores=exp)
        return

    n      = len(resultats)
    lgn    = len(grille)
    cols   = len(grille[0]) if grille else 0

    fig, axes = plt.subplots(
        1, n,
        figsize=(max(4, cols * 0.9) * n + 1, max(3, lgn * 0.9) + 1),
    )
    # Normaliser en liste meme quand n == 1
    if n == 1:
        axes = [axes]

    for ax, (nom, chemin) in zip(axes, resultats.items()):
        exp = (carte_explores or {}).get(nom)
        _dessiner_sur_axe(ax, grille, chemin, depart, arrivee, explores=exp, titre=nom)

    _ajouter_legende(axes[-1], exterieur=True)
    plt.suptitle("Comparaison des algorithmes", fontsize=14, fontweight="bold")
    plt.tight_layout()

    if sauver:
        plt.savefig(sauver, dpi=150, bbox_inches="tight")
        print(f"[visualiseur] Comparaison sauvegardee -> '{sauver}'")
        plt.close(fig)
    else:
        plt.show()


# ── Fonctions internes ─────────────────────────────────────────────────────────

def _construire_matrice(
    grille:   list[list[str]],
    chemin:   list[tuple[int, int]],
    depart:   tuple[int, int],
    arrivee:  tuple[int, int],
    explores: set[tuple[int, int]] | None,
) -> "np.ndarray":
    """Convertir la grille + ensembles chemin/explores en matrice entiere pour imshow."""
    lignes, cols     = len(grille), len(grille[0]) if grille else 0
    matrice          = np.full((lignes, cols), _LIBRE, dtype=int)
    ensemble_chemin  = set(chemin)
    ensemble_exp     = set(explores) if explores else set()

    for y, rangee in enumerate(grille):
        for x, case in enumerate(rangee):
            pos = (x, y)
            if case == "X":
                matrice[y, x] = _OBSTACLE
            elif pos in ensemble_exp and pos not in ensemble_chemin:
                matrice[y, x] = _EXPLORE
            elif pos in ensemble_chemin:
                matrice[y, x] = _CHEMIN

    # Depart / arrivee toujours affiches par-dessus
    matrice[depart[1],  depart[0]]  = _DEPART
    matrice[arrivee[1], arrivee[0]] = _ARRIVEE

    return matrice


def _dessiner_sur_axe(
    ax,
    grille:   list[list[str]],
    chemin:   list[tuple[int, int]],
    depart:   tuple[int, int],
    arrivee:  tuple[int, int],
    *,
    explores: set[tuple[int, int]] | None = None,
    titre:    str = "",
) -> None:
    """Afficher une grille sur un objet Axes matplotlib."""
    lignes, cols    = len(grille), len(grille[0]) if grille else 0
    matrice         = _construire_matrice(grille, chemin, depart, arrivee, explores)
    ensemble_chemin = set(chemin)

    cmap = ListedColormap(_PALETTE)
    ax.imshow(matrice, cmap=cmap, vmin=0, vmax=5)

    # Quadrillage
    ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, lignes, 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=1.5)
    ax.tick_params(which="both", bottom=False, left=False,
                   labelbottom=False, labelleft=False)

    # Etiquettes de case
    _cases_sombres = {_OBSTACLE, _CHEMIN, _DEPART, _ARRIVEE}
    for y, rangee in enumerate(grille):
        for x in range(len(rangee)):
            etiquette = _etiquette_case_mpl((x, y), depart, arrivee, ensemble_chemin)
            if etiquette:
                couleur = "white" if matrice[y, x] in _cases_sombres else "#444"
                ax.text(x, y, etiquette, ha="center", va="center",
                        fontsize=12, fontweight="bold", color=couleur)

    info = f"{len(chemin) - 1} pas" if chemin else "aucun chemin"
    ax.set_title(f"{titre}\n({info})", fontsize=11, fontweight="bold")


def _ajouter_legende(ax, *, exterieur: bool = False) -> None:
    """Ajouter une legende de couleurs a un objet Axes matplotlib."""
    patches = [
        mpatches.Patch(color=_PALETTE[_DEPART],   label="Depart (S)"),
        mpatches.Patch(color=_PALETTE[_ARRIVEE],  label="Arrivee (G)"),
        mpatches.Patch(color=_PALETTE[_CHEMIN],   label="Chemin"),
        mpatches.Patch(color=_PALETTE[_EXPLORE],  label="Explore"),
        mpatches.Patch(color=_PALETTE[_OBSTACLE], label="Obstacle"),
    ]
    loc  = "upper right"
    bbox = (1.35, 1.0) if exterieur else None
    ax.legend(handles=patches, loc=loc,
              bbox_to_anchor=bbox, fontsize=8, framealpha=0.9)


def _case_terminal(
    pos:             tuple[int, int],
    brut:            str,
    ensemble_chemin: set[tuple[int, int]],
    ensemble_exp:    set[tuple[int, int]],
    depart:          tuple[int, int],
    arrivee:         tuple[int, int],
) -> tuple[str, str]:
    """Renvoyer (symbole, couleur_ANSI) pour une case du terminal."""
    if pos == depart:
        return "S", _COULEUR["depart"]
    if pos == arrivee:
        return "G", _COULEUR["arrivee"]
    if pos in ensemble_chemin:
        return "*", _COULEUR["chemin"]
    if pos in ensemble_exp:
        return "o", _COULEUR["explore"]
    if brut == "X":
        return "X", _COULEUR["obstacle"]
    return ".", _COULEUR["libre"]


def _etiquette_case_mpl(
    pos:             tuple[int, int],
    depart:          tuple[int, int],
    arrivee:         tuple[int, int],
    ensemble_chemin: set[tuple[int, int]],
) -> str:
    """Renvoyer le texte a superposer sur une case matplotlib."""
    if pos == depart:
        return "S"
    if pos == arrivee:
        return "G"
    if pos in ensemble_chemin:
        return "*"
    return ""


def _afficher_legende_terminal(avec_explores: bool) -> None:
    """Afficher la ligne de legende coloree dans le terminal."""
    elements: list[tuple[str, str]] = [
        ("S", "depart"),
        ("G", "arrivee"),
        ("*", "chemin"),
    ]
    if avec_explores:
        elements.append(("o", "explore"))
    elements.append(("X", "obstacle"))

    parties = [f"{_COULEUR[cle]}{sym}{_RESET}={cle}" for sym, cle in elements]
    print("  " + " | ".join(parties))
