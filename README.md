# ProjetBDMLoptimisation

Algorithmes de recherche de chemin sur grilles 2D avec obstacles.
Projet academique — S6 Complexite algorithmique, Efrei Paris.

---

## Structure

```
ProjetBDMLoptimisation/
├── data/
│   ├── grid1.txt              # Grilles de test 4 x 6
│   ├── grid2.txt
│   └── grid3.txt
├── results/                   # Images generees automatiquement
│   ├── resultats_{grille}_{algo}.png
│   └── resultats_{grille}_comparaison.png
├── src/
│   ├── main.py                # Point d'entree — menu interactif + mode complet
│   ├── grid.py                # load_grid() + get_neighbors()
│   ├── visualizer.py          # Visualisation terminal (ASCII) et graphique (matplotlib)
│   └── algorithms/
│       ├── astar.py           # A* — f(n) = g(n) + h(n), heuristique Manhattan
│       ├── greedy.py          # Glouton Best-First — choisit le voisin le plus proche de G
│       └── genetic.py         # Genetique — evolution d'une population de sequences de mouvements
├── RESULTATS.md               # Tableaux de comparaison et analyse
├── requirements.txt
└── README.md
```

---

## Implementation

### Modele de grille (`grid.py`)

La grille est un tableau 2D `grille[y][x]` charge depuis un fichier `.txt`.
Chaque case est un token : `S` (depart), `G` (arrivee), `X` (obstacle), `0` (libre).

`get_neighbors(grille, pos)` retourne les 4 voisins cardinaux accessibles
(hors limites et obstacles exclus).

### A\* (`algorithms/astar.py`)

Recherche du chemin **optimal** via `f(n) = g(n) + h(n)` :
- `g(n)` : nombre de pas depuis le depart
- `h(n)` : distance de Manhattan vers l'arrivee (admissible et consistante)

Utilise un tas-min (`heapq`) pour la file de priorite.
Retourne le chemin solution et l'ensemble des cases explorees.

### Glouton (`algorithms/greedy.py`)

A chaque etape, choisit le voisin minimisant `h(n)` sans tenir compte de `g(n)`.
Rapide mais non optimal et non complet (pas de backtracking).

### Genetique (`algorithms/genetic.py`)

Fait evoluer une population de sequences de mouvements sur 100 generations :
- **Fitness** : `distance_manhattan(derniere_case, arrivee) + 0.1 x longueur`
- **Selection** : conservation des 10 meilleurs (elitisme)
- **Croisement** : monopoint entre deux parents
- **Mutation** : remplacement aleatoire au taux de 10 %

### Visualiseur (`visualizer.py`)

Trois fonctions utilisables par tous les algorithmes :
- `afficher_chemin(...)` : affichage ASCII colore dans le terminal
- `tracer_grille(...)` : figure matplotlib sauvegardee dans `results/`
- `comparer_resultats(...)` : comparaison cote a cote de plusieurs algorithmes

---

## Resultats

### Lire l'analyse

Ouvrir **`RESULTATS.md`** — il contient :
- les tableaux de comparaison (longueur du chemin, temps d'execution) pour chaque grille
- l'explication de pourquoi le glouton n'est pas toujours optimal
- l'explication du fonctionnement et des garanties de A\*
- les avantages et inconvenients de l'algorithme genetique
- une conclusion comparative

### Lire les images

Les captures sont dans **`results/`**, generees en choisissant **option 2** au lancement :

| Fichier | Contenu |
|---------|---------|
| `resultats_{grille}_astar.png` | Chemin trouve par A\* |
| `resultats_{grille}_glouton.png` | Chemin trouve par le glouton |
| `resultats_{grille}_genetique.png` | Chemin trouve par le genetique |
| `resultats_{grille}_comparaison.png` | Les trois algorithmes cote a cote |

Legende des couleurs sur les images :

| Couleur | Signification |
|---------|---------------|
| Bleu | Depart (S) |
| Rose | Arrivee (G) |
| Turquoise | Cases du chemin solution |
| Ambre | Cases explorees (A\* uniquement) |
| Noir | Obstacle |

---

## Lancement

```bash
pip install -r requirements.txt
cd src
python main.py
```

Le programme affiche un menu :

```
===== MENU =====
1 - Mode interactif      # choisir un algorithme et une grille, affichage terminal uniquement
2 - Affichage complet    # lance les 3 algorithmes sur les 3 grilles et sauvegarde les images
3 - Quitter
```

> **Pour generer les images dans `results/`, choisir l'option 2.**
