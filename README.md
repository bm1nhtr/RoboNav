# ProjetBDMLoptimisation

Algorithmes de recherche de chemin sur grilles 2D — S6 Complexite algorithmique, Efrei Paris.

## Structure

```
ProjetBDMLoptimisation/
├── data/
│   ├── grid1.txt
│   ├── grid2.txt
│   └── grid3.txt
├── results/                  # Images generees (cree automatiquement)
├── src/
│   ├── main.py               # Point d'entree
│   ├── grid.py               # load_grid() + get_neighbors()
│   ├── visualizer.py         # Visualisation (terminal + matplotlib)
│   └── algorithms/
│       ├── astar.py          # A* — f(n) = g(n) + h(n)
│       ├── greedy.py         # Glouton Best-First
│       └── genetic.py        # Algorithmique genetique
├── requirements.txt
└── README.md
```

## Lancement

```bash
# Installer les dependances
pip install -r requirements.txt

# Lancer depuis src/
cd src
python main.py
```

Les images sont sauvegardees dans `results/` :
- `resultats_{grille}_{algo}.png` — chemin par algorithme
- `resultats_{grille}_comparaison.png` — comparaison cote a cote

## Algorithmes

| Algorithme | Fichier | Statut |
|------------|---------|--------|
| A\* | `algorithms/astar.py` | Implemente |
| Glouton | `algorithms/greedy.py` | Implemente |
| Genetique | `algorithms/genetic.py` | Implemente |

## Ajouter un algorithme

1. Creer `src/algorithms/mon_algo.py` avec la fonction :
   ```python
   def mon_algo_search(grid, start, goal) -> list | tuple[list, set]:
       ...
   ```
2. L'enregistrer dans `ALGORITHMES` (dans `main.py`) :
   ```python
   from algorithms.mon_algo import mon_algo_search
   ALGORITHMES["Mon Algo"] = (mon_algo_search, "mon_algo")
   ```
