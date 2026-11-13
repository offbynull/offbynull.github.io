from functools import lru_cache

from helpers.HashableCollections import HashableDict, HashableList


@lru_cache(maxsize=65535)
def dfs_count_paths(graph: dict[str, list[str]], node: str, end_node: str) -> int:
    if node == end_node:
        return 1
    children = graph[node]
    count = 0
    for child in children:
        count += dfs_count_paths(graph, child, end_node)
    return count


def create_grid(x: int, y: int) -> dict[str, list[str]]:
    g = HashableDict()
    for x_ in range(x+1):
        for y_ in range(y+1):
            children = g.setdefault(f'{x_}x{y_}', HashableList())
            if x_ != x:
                children.append(f'{x_+1}x{y_}')
            if y_ != y:
                children.append(f'{x_}x{y_+1}')
    return g


x = 16
y = 12
grid = create_grid(x, y)
path_count = dfs_count_paths(grid, '0x0', f'{x}x{y}')
print(f'{x}x{y}={path_count}')
