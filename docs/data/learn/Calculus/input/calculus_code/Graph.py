import inspect
import sys
from pathlib import Path
from sys import stdin

import yaml
from matplotlib import pyplot as plt
import numpy as np

from expression.Node import Node, ConstantNode, FunctionNode, VariableNode
from expression.parser.Parser import parse


def _evaluate(n: Node, vars: dict[str, float | int]):
    if isinstance(n, ConstantNode):
        return n.value
    elif isinstance(n, VariableNode):
        return vars[n.name]
    elif isinstance(n, FunctionNode):
        if n.op == '+':
            return _evaluate(n.args[0], vars) + _evaluate(n.args[1], vars)
        elif n.op == '-':
            return _evaluate(n.args[0], vars) - _evaluate(n.args[1], vars)
        elif n.op == '*':
            return _evaluate(n.args[0], vars) * _evaluate(n.args[1], vars)
        elif n.op == '/':
            return _evaluate(n.args[0], vars) / _evaluate(n.args[1], vars)
        elif n.op == '^':
            return _evaluate(n.args[0], vars) ** _evaluate(n.args[1], vars)

def graph(funcs: list[str], x_lim: tuple[float, float], y_lim: tuple[float, float] | None):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    x_min, x_max = x_lim
    x_vals = np.linspace(x_min, x_max, 1000)
    y_val_max = 0.0
    for func in funcs:
        node = parse(func)
        y_vals = [_evaluate(node, {'x': x}) for x in x_vals]
        y_val_max = max(y_val_max, abs(y_vals[-1]))
        plt.plot(x_vals, y_vals, label=func)
    plt.legend(loc="upper left")
    ax.spines['left'].set_position(('data', 0.0))
    ax.spines['bottom'].set_position(('data', 0.0))
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    if y_lim is not None:
        y_min, y_max = y_lim
        ax.set_ylim(y_min, y_max)
    else:
        ax.set_ylim(-y_val_max, y_val_max)
    in_path = Path('/input/.__UNIQUE_INPUT_ID')
    if in_path.exists():
        _id = in_path.read_text().strip()
        out_path = Path(f'/output/{_id}.svg')
        plt.savefig(out_path, bbox_inches='tight')
        print(f'![Graph(s) of {",".join(funcs)}]({_id}.svg)')
    else:
        plt.show()


def main():
    # print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        funcs = data['funcs']
        x_lim = tuple(data['x_lim'])
        y_lim = tuple(data['y_lim']) if 'y_lim' in data else None
        graph(funcs, x_lim, y_lim)
    finally:
        # print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    graph(['x^2', 'x^3', 'x^4', 'x^5'], (-5, 5), (-5, 5))
    # main()
