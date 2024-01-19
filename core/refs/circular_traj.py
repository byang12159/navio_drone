import numpy as np

def xyz(args, real_t):
    period, size_radius = args
    print('period/size radius: ', period, size_radius)

    t = (real_t / period) * (2 * np.pi)
    x = np.cos(t) 
    y = np.sin(t)
    x = size_radius * x
    y = size_radius * y
    z = np.ones_like(x) * 1.5

    return x, y, z



