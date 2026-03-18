# Comparaison des algorithmes de recherche de chemin

## Resultats

### Grille 1

| Algorithme | Longueur du chemin | Temps (ms) | Observation |
|------------|--------------------|------------|-------------|
| A*         | 8                  | 0.13       | Optimal |
| Glouton    | 8                  | 0.05       | Rapide |
| Genetique  | 12                 | 1.38       | Non optimal |

---

### Grille 2

| Algorithme | Longueur du chemin | Temps (ms) | Observation |
|------------|--------------------|------------|-------------|
| A*         | 8                  | 0.05       | Optimal |
| Glouton    | 8                  | 0.04       | Rapide |
| Genetique  | 12                 | 1.71       | Plus lent |

---

### Grille 3

| Algorithme | Longueur du chemin | Temps (ms) | Observation |
|------------|--------------------|------------|-------------|
| A*         | 8                  | 0.05       | Optimal |
| Glouton    | 8                  | 0.02       | Tres rapide |
| Genetique  | 14                 | 1.07       | Non optimal |

---

## Analyse

### Pourquoi l'algorithme glouton ne garantit-il pas toujours la solution optimale ?

L'algorithme glouton choisit a chaque etape le voisin qui minimise uniquement
l'heuristique `h(n)` (distance de Manhattan vers l'arrivee), **sans tenir compte
du cout `g(n)` deja paye** pour atteindre le noeud courant.

Il prend donc des decisions localement bonnes qui peuvent etre globalement
sous-optimales : en suivant toujours la direction apparemment la plus proche,
il peut emprunter un chemin plus long ou se retrouver bloque dans un cul-de-sac
sans possibilite de backtracking. Sur nos grilles simples il obtient par chance
un resultat identique a A*, mais ce n'est pas garanti en general.

---

### Pourquoi A\* est-il souvent plus performant pour trouver un chemin optimal ?

A\* evalue chaque noeud avec la fonction `f(n) = g(n) + h(n)` :
- `g(n)` : le cout exact deja paye depuis le depart
- `h(n)` : une estimation du cout restant (distance de Manhattan)

Grace a l'**admissibilite** de l'heuristique (`h(n)` ne surestime jamais le
cout reel), A\* garantit mathematiquement de trouver le chemin le plus court.
Contrairement au glouton, il ne sacrifie jamais le cout global pour un gain
local : il explore en priorite les noeuds qui offrent le meilleur compromis
entre progression vers l'arrivee et economie de pas.

---

### Quels sont les avantages et inconvenients d'un algorithme genetique ?

**Avantages**
- Explore un large espace de solutions en parallele (population d'individus).
- Tolerant aux environnements complexes ou les heuristiques classiques echouent.
- Flexible : les parametres (taille de population, taux de mutation) permettent
  d'adapter le comportement selon le probleme.

**Inconvenients**
- **Non deterministe** : deux executions peuvent donner des chemins differents.
- **Non optimal** : rien ne garantit que le meilleur individu final corresponde
  au chemin le plus court.
- **Lent** : evaluer une population sur plusieurs generations est bien plus couteux
  qu'une recherche guidee (A\* ou glouton).
- **Sensible aux parametres** : un mauvais reglage (trop peu de generations,
  trop peu de pas) peut donner des resultats mediocres.

---

## Conclusion

A\* est le plus adapte a ce probleme car il combine optimalite garantie et temps
d'execution faible. Le glouton est une alternative rapide lorsque l'optimalite
n'est pas critique. Le genetique est pertinent pour des espaces de recherche plus
complexes ou aucune heuristique efficace n'est disponible, mais il reste moins
performant sur des grilles simples.
