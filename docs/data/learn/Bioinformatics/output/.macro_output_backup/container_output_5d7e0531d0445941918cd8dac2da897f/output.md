`{bm-disable-all}`[ch3_code/src/FindGraphAnomalies.py](ch3_code/src/FindGraphAnomalies.py) (lines 53 to 105):`{bm-enable-all}`

```python
def find_head_convergences(graph: Graph[T], branch_len: int) -> List[Tuple[Optional[T], List[T], Optional[T]]]:
    root_nodes = filter(lambda n: graph.get_in_degree(n) == 0, graph.get_nodes())

    ret = []
    for n in root_nodes:
        for child in graph.get_outputs(n):
            path_from_child = walk_outs_until_converge(graph, child)
            if path_from_child is None:
                continue
            diverging_node = None
            branch_path = [n] + path_from_child[:-1]
            converging_node = path_from_child[-1]
            path = (diverging_node, branch_path, converging_node)
            if len(branch_path) <= branch_len:
                ret.append(path)
    return ret


def find_tail_divergences(graph: Graph[T], branch_len: int) -> List[Tuple[Optional[T], List[T], Optional[T]]]:
    tail_nodes = filter(lambda n: graph.get_out_degree(n) == 0, graph.get_nodes())

    ret = []
    for n in tail_nodes:
        for child in graph.get_inputs(n):
            path_from_child = walk_ins_until_diverge(graph, child)
            if path_from_child is None:
                continue
            diverging_node = path_from_child[0]
            branch_path = path_from_child[1:] + [n]
            converging_node = None
            path = (diverging_node, branch_path, converging_node)
            if len(branch_path) <= branch_len:
                ret.append(path)
    return ret


def find_bubbles(graph: Graph[T], branch_len: int) -> List[Tuple[Optional[T], List[T], Optional[T]]]:
    branching_nodes = filter(lambda n: graph.get_out_degree(n) > 1, graph.get_nodes())

    ret = []
    for n in branching_nodes:
        for child in graph.get_outputs(n):
            path_from_child = walk_outs_until_converge(graph, child)
            if path_from_child is None:
                continue
            diverging_node = n
            branch_path = path_from_child[:-1]
            converging_node = path_from_child[-1]
            path = (diverging_node, branch_path, converging_node)
            if len(branch_path) <= branch_len:
                ret.append(path)
    return ret
```