import numpy as np

if __name__ == '__main__':
    m = np.random.randint(-100, 100, (5, 5))
    inds = np.where((m < 0) & (m % 2 != 0))
    print(np.sum(m[inds]))
    print(round(np.std(m[inds]), 2))
    print(round(np.sqrt(np.sum((m[inds] - np.mean(m[inds])) ** 2) / len(m[inds])), 2))