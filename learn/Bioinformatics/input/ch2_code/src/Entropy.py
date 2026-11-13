from ScoreMotifUsingEntropy import calculate_entropy

if __name__ == '__main__':
    print(f'{calculate_entropy([0.2, 0.6, 0.0, 0.2])}')
    print(f'{calculate_entropy([0.0, 0.6, 0.0, 0.4])}')
    print(f'{calculate_entropy([0.0, 0.0, 0.9, 0.1])}')

    print(f'{calculate_entropy([0.25, 0.25, 0.25, 0.25])}')  # very weak
    print(f'{calculate_entropy([1.0, 0.0, 0.0, 0.0])}')      # fully conserved
    # For a probability distribution of As, Cs, Ts, and Gs (4 values that when added equal 1), you'll get a 0.0 for
    # strongly conserved (last line) vs 2.0 for very weakly conserved (2nd last line). The closer to 0.0 the output is,
    # the more conserved the value is
