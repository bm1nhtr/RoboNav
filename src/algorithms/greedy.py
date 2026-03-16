def heuristic(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])


def greedy_search(grid, start, goal):
    path = [start]
    current = start
    while current != goal:

        x, y = current

        neighbors = [
            (x+1, y),
            (x-1, y),
            (x, y+1),
            (x, y-1)
        ]

        valid_neighbors = []

        # on verif que les voisins sont dans la grille et pas des obstacles
        for nx, ny in neighbors:
            if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
                if grid[ny][nx] != "X":
                    valid_neighbors.append((nx, ny))

        if not valid_neighbors:
            return path

        # on cherche le voisin le plus proche du goal
        best_neighbor = valid_neighbors[0]
        best_distance = heuristic(best_neighbor, goal)

        for neighbor in valid_neighbors:
            distance = heuristic(neighbor, goal)
            if distance < best_distance:
                best_distance = distance
                best_neighbor = neighbor

        next_node = best_neighbor

        path.append(next_node)
        current = next_node


    return path
