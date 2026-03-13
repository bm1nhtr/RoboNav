# ProjetBDMLoptimisation

Algorithmes de recherche de chemin sur des grilles 2D avec obstacles.
Projet academique pour le cours **Complexite algorithmique S6** a Efrei Paris.

---

## Etat des algorithmes

| Algorithme | Statut | Fichier |
|------------|--------|---------|
| A\* | Done | `src/algorithms/astar.py` |
| Glouton (Best-First) | Stub — a implementer | `src/algorithms/greedy.py` |
| Genetique | Prevu | — |

---

## Arborescence du projet

```
ProjetBDMLoptimisation/
├── data/
│   ├── grid1.txt              # Grilles de test 4 x 6
│   ├── grid2.txt
│   └── grid3.txt
├── results/                   # Images generees automatiquement
│   ├── resultats_grid1.png
│   ├── resultats_grid2.png
│   └── resultats_grid3.png
├── src/
│   ├── main.py                # Point d'entree
│   ├── grid.py                # Modele de grille : load_grid() + get_neighbors()
│   ├── visualizer.py          # Visualisation generique (terminal + matplotlib)
│   └── algorithms/
│       ├── astar.py           # A* avec heuristique Manhattan  f(n) = g(n) + h(n)
│       └── greedy.py          # Glouton Best-First (stub)
├── requirements.txt
└── README.md
```

---

## Format des grilles

Fichiers texte avec des tokens separes par des espaces :

| Token | Signification |
|-------|---------------|
| `S` | Case depart |
| `G` | Case arrivee |
| `X` | Obstacle (infranchissable) |
| `0` | Case libre |

Exemple (`grid1.txt`) :

```
S 0 0 0 X 0
0 X 0 0 X 0
0 X 0 0 0 0
0 0 0 X 0 G
```

---

## Demarrage rapide

### 1 — Cloner et installer les dependances

```bash
git clone <repo-url>
cd ProjetBDMLoptimisation
pip install -r requirements.txt
```

### 2 — Lancer

```bash
cd src
python main.py
```

Cela va :
- Afficher une grille ASCII coloree dans le terminal pour chaque grille.
- Sauvegarder une image de comparaison par grille dans le dossier `results/`.

---

## Algorithme A\*

La fonction d'evaluation est **f(n) = g(n) + h(n)** :

| Terme | Description |
|-------|-------------|
| `g(n)` | Cout exact (nombre de pas) depuis le depart jusqu'a `n` |
| `h(n)` | Heuristique de distance de Manhattan — admissible et consistante |

Comme `h(n)` ne surestime jamais le cout reel, A\* garantit de trouver
le **chemin optimal** quand il existe.

---

## API du visualiseur

Trois fonctions publiques utilisables par n'importe quel algorithme :

```python
from visualizer import afficher_chemin, tracer_grille, comparer_resultats
```

| Fonction | Description |
|----------|-------------|
| `afficher_chemin(grille, chemin, depart, arrivee, *, titre, explores)` | Affichage ASCII colore dans le terminal |
| `tracer_grille(grille, chemin, depart, arrivee, *, titre, explores, sauver)` | Figure matplotlib |
| `comparer_resultats(grille, resultats, depart, arrivee, *, carte_explores, sauver)` | Comparaison cote a cote |

### Exemple d'utilisation

```python
from grid       import load_grid
from visualizer import afficher_chemin, comparer_resultats

grille, depart, arrivee = load_grid("data/grid1.txt")

# Apres execution de votre algorithme :
chemin, explores = mon_algo(grille, depart, arrivee)

# Affichage terminal
afficher_chemin(grille, chemin, depart, arrivee, titre="Mon Algo", explores=explores)

# Comparaison de plusieurs algorithmes
comparer_resultats(
    grille,
    resultats       = {"A*": chemin_astar, "Mon Algo": chemin_mien},
    depart          = depart,
    arrivee         = arrivee,
    carte_explores  = {"A*": exp_astar, "Mon Algo": exp_mien},
    sauver          = "results/comparaison.png",
)
```

### Legende des couleurs

| Couleur | Signification |
|---------|---------------|
| Bleu    | Depart (S) |
| Rose    | Arrivee (G) |
| Turquoise | Chemin solution |
| Ambre   | Cases explorees |
| Noir    | Obstacle |

---

## Utilitaires de grille

```python
from grid import load_grid, get_neighbors

grille, depart, arrivee = load_grid("data/grid1.txt")
voisins = get_neighbors(grille, (2, 1))  # voisins orthogonaux accessibles de (2,1)
```

---

## Ajouter un nouvel algorithme

1. Creer `src/algorithms/mon_algo.py`.
2. Implementer :
   ```python
   def mon_algo_search(grille, depart, arrivee) -> tuple[list, set]:
       ...
       return chemin, explores   # (chemin: list de (x,y), explores: set de (x,y))
   ```
3. L'importer et l'ajouter dans le dict `ALGORITHMES` de `main.py` :
   ```python
   from algorithms.mon_algo import mon_algo_search
   ALGORITHMES["Mon Algo"] = mon_algo_search
   ```

Le visualiseur et la mesure de temps le prendront en compte automatiquement.
