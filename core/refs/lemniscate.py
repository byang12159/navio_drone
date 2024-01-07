import numpy as np

def xyz(args, real_t):
    period, sizex, sizey = args
    print('period/sizex/sizey: ', period, sizex, sizey)
    if not period:
        period = real_t[-1]
    t = real_t / period * 2 * np.pi
    x = np.sqrt(2) * np.cos(t) / (1 + np.sin(t) ** 2)
    y = x * np.sin(t)
    x = sizex * x
    y = sizey * y
    z = np.ones_like(x) * 1.5
    return x, y, z
