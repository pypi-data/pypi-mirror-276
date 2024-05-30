a = ['X = [-9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7]', 'p = Fraction(1, len(X))',
     'Px = [p, p, p, p, p, p, p, p, p, p, p, p, p, p, p, p, p]']


def saaave(name):
    result = '\n'.join(a)
    my_file = open(f"{name}.py", "w+")
    my_file.write(f'{result}')
    my_file.close()
    return 'Все получилось'
