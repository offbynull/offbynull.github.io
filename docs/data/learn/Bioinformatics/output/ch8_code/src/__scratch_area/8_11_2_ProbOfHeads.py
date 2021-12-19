def prob_of_heads(total_heads: int, total_flips: int):
    return total_heads / total_flips


if __name__ == '__main__':
    print(f'{prob_of_heads(5, 10)}')
    print(f'{prob_of_heads(2, 100)}')
    print(f'{prob_of_heads(7, 10)}')