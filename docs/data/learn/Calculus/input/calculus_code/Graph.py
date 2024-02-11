from pathlib import Path
from sys import stdin

import yaml
from matplotlib import pyplot as plt
import numpy as np

from Evaluator import evaluate
from expression.parser.Parser import parse


def graph(
        funcs: list[str],
        x_lim: tuple[float, float],
        y_lim: tuple[float, float] | None,
        fig_size: tuple[float, float] | None = None,
        v_asymptotes: list[float] | None = None
):
    fig = plt.figure(figsize=fig_size)
    ax = fig.add_subplot(1, 1, 1)

    x_min, x_max = x_lim
    x_vals = np.linspace(x_min, x_max, 1000)
    y_val_max = 0.0
    for func in funcs:
        node = parse(func)
        y_vals = [evaluate(node, {'x': x}) for x in x_vals]
        y_val_max = max(y_val_max, abs(y_vals[-1]))
        plt.scatter(x_vals, y_vals, label=func, marker='o', s=(72./fig.dpi)**2)
    if v_asymptotes is not None:
        for x in v_asymptotes:
            plt.axvline(x=x, linestyle='--', color='000000')
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
    ax.set_xlim(x_min, x_max)
    in_path = Path('/input/.__UNIQUE_INPUT_ID')
    if in_path.exists():
        _id = in_path.read_text().strip()
        out_path = Path(f'/output/{_id}.png')
        plt.savefig(out_path, bbox_inches='tight')
        print(f'![Graph(s) of {",".join(funcs)}]({_id}.png)')
    else:
        plt.show()


def main():
    # print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        data_raw = ''.join(stdin.readlines())
        data: dict = yaml.safe_load(data_raw)
        funcs = data['funcs']
        v_asymptotes  = data['v_asymptotes'] if 'v_asymptotes' in data else None
        x_lim = tuple(data['x_lim'])
        y_lim = tuple(data['y_lim']) if 'y_lim' in data else None
        fig_size = tuple(data['fig_size']) if 'fig_size' in data else None
        graph(funcs, x_lim, y_lim, fig_size, v_asymptotes)
    finally:
        # print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    graph(['x^(1/3)', 'x'], (-3, 3), (-3, 3), None, [-.5, .5])
    # main()
