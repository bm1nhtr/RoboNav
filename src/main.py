from grid import load_grid
from algorithms.greedy import greedy_search
from algorithms.astar import astar_search



# Importer les données (grid)
DATA_PATH = "data/"
grid1,start1,goal1 = load_grid( DATA_PATH + "grid1.txt" )
grid2,start2,goal2 = load_grid( DATA_PATH + "grid2.txt" )
grid3,start3,goal3 = load_grid( DATA_PATH + "grid3.txt" )

path_greedy = greedy_search(grid1,start1,goal1)
print("Greedy path:",path_greedy)

path_astar = astar_search(grid1,start1,goal1)
print("A* path:",path_astar)

#TODO : une fonction permettant de récupérer les voisins d’une case.
#TODO : algo génétique (manquant)
#TODO : Appliquer le temps de calcul et la complexité et une capture d’écran montrant un chemin trouvé.
#TODO : Visualiser les étapes pour chaque algo
#TODO : Completer le README.md et le document pour les résultats