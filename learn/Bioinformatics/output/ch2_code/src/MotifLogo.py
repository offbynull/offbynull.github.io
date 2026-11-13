from os import path
from hashlib import md5
from math import log
from typing import List, Dict

import logomaker as lm
import pandas as pd
import matplotlib.pyplot as plt
from logomaker import Logo

from MotifMatrixCount import motif_matrix_count
from MotifMatrixProfile import motif_matrix_profile

# MARKDOWN
def calculate_entropy(values: List[float]) -> float:
    ret = 0.0
    for value in values:
        ret += value * (log(value, 2.0) if value > 0.0 else 0.0)
    ret = -ret
    return ret

def create_logo(motif_matrix_profile: Dict[str, List[float]]) -> Logo:
    columns = list(motif_matrix_profile.keys())
    data = [motif_matrix_profile[k] for k in motif_matrix_profile.keys()]
    data = list(zip(*data))  # trick to transpose data

    entropies = list(map(lambda x: 2 - calculate_entropy(x), data))

    data_scaledby_entropies = [[p * e for p in d] for d, e in zip(data, entropies)]

    df = pd.DataFrame(
        columns=columns,
        data=data_scaledby_entropies
    )
    logo = lm.Logo(df)
    logo.ax.set_ylabel('information (bits)')
    logo.ax.set_xlim([-1, len(df)])
    return logo
# MARKDOWN


def main():
    print("<div style=\"border:1px solid black;\">", end="\n\n")
    print("`{bm-disable-all}`", end="\n\n")
    try:
        dnas = []
        while True:
            try:
                dna = input().strip().upper()
                if len(dna) > 0:
                    dnas.append(dna)
            except EOFError:
                break

        hasher = md5()
        hasher.update(str(dnas).encode('utf-8'))
        logo_filename = 'motif_logo_' + hasher.hexdigest() + '.svg'
        if path.isdir('/output'):
            logo_path = '/output/' + logo_filename
        else:
            logo_path = '/tmp/' + logo_filename

        print(f'Generating logo for the following motif matrix...\n\n')
        print(f'{"<br>".join(dnas)}\n\n')
        counts = motif_matrix_count(dnas)
        profile = motif_matrix_profile(counts)
        logo = create_logo(profile)
        plt.savefig(logo_path)
        print(f'Result...\n\n')
        print(f'![Motif Logo]({logo_filename})\n\n')
    finally:
        print("</div>", end="\n\n")
        print("`{bm-enable-all}`", end="\n\n")


if __name__ == '__main__':
    main()