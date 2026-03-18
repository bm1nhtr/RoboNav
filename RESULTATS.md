# Comparaison des algorithmes de recherche de chemin

## Résultats

### Grille 1

| Algorithme | Longueur du chemin | Temps (ms) | Observation |
|------------|--------------------|------------|-------------|
| A*         | 8                  | 0.13       | Optimal |
| Glouton    | 8                  | 0.05       | Rapide |
| Génétique  | 12                 | 1.38       | Non optimal |

---

### Grille 2

| Algorithme | Longueur du chemin | Temps (ms) | Observation |
|------------|--------------------|------------|-------------|
| A*         | 8                  | 0.05       | Optimal |
| Glouton    | 8                  | 0.04       | Rapide |
| Génétique  | 12                 | 1.71       | Plus lent |

---

### Grille 3

| Algorithme | Longueur du chemin | Temps (ms) | Observation |
|------------|--------------------|------------|-------------|
| A*         | 8                  | 0.05       | Optimal |
| Glouton    | 8                  | 0.02       | Très rapide |
| Génétique  | 14                 | 1.07       | Non optimal |

---

## Analyse

L’algorithme A* trouve toujours le chemin optimal (8 pas) sur toutes les grilles.  
Il garantit donc une solution optimale, avec un temps d’exécution très faible.

L’algorithme glouton est le plus rapide, mais il ne garantit pas toujours un chemin optimal.  
Dans notre cas, il trouve cependant un chemin de longueur identique à A*.

L’algorithme génétique permet de trouver un chemin valide, mais celui-ci est plus long.  
Cela s’explique par son caractère aléatoire : il explore plusieurs solutions et ne garantit pas l’optimalité.

On observe également que le temps d’exécution du génétique est plus élevé que les autres algorithmes.

---

## Conclusion

A* est le meilleur algorithme pour ce problème car il combine efficacité et optimalité.  
Le glouton est intéressant pour sa rapidité mais moins fiable.  
Le génétique est utile pour explorer différentes solutions mais reste moins performant dans ce contexte.