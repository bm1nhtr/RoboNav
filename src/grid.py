
def load_grid(file):
    """
    todo add docstring
    :param file:
    :return:
    """
    grid=[]
    start=None
    goal=None

    with open(file) as f:
        for y,line in enumerate(f):
            row=line.strip().split()
            for x,val in enumerate(row):
                if val=="S":
                    start=(x,y)
                if val=="G":
                    goal=(x,y)
            grid.append(row)

    print('Grid:\n',grid)

    return grid,start,goal
