
import heapq

def heuristic(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])

def astar_search(grid,start,goal):
    # TODO: implement A*
    open_list=[]
    heapq.heappush(open_list,(0,start))
    return []
