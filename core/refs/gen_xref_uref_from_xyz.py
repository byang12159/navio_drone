import numpy as np
from navio_drone.sysid.ExcitationGenerator import translate_x
from navio_drone.core.constants import xy_Tc, z_Tc

def gen_xref_uref_from_xyz(xyz, T, dt, translate=True):
    downsample_mult = 50
    dt = dt / downsample_mult
    if T is None:
        T = xyz(t=None, get_T=True)
    t = np.arange(0., T, dt)

    x, y, z = xyz(t)
    
    if translate:
        x = translate_x(x, 0)
        y = translate_x(y, 1)
        z = translate_x(z, 2)

    vx = (x[1:] - x[:-1]) / dt
    vy = (y[1:] - y[:-1]) / dt
    vz = (z[1:] - z[:-1]) / dt
    ax = (vx[1:] - vx[:-1]) / dt
    ay = (vy[1:] - vy[:-1]) / dt
    az = (vz[1:] - vz[:-1]) / dt
    jx = (ax[1:] - ax[:-1]) / dt
    jy = (ay[1:] - ay[:-1]) / dt
    jz = (az[1:] - az[:-1]) / dt

    t = t[:-3]
    x = x[:-3]
    y = y[:-3]
    z = z[:-3]
    vx = vx[:-2]
    vy = vy[:-2]
    vz = vz[:-2]
    ax = ax[:-1]
    ay = ay[:-1]
    az = az[:-1]

    xref = np.zeros([t.shape[0], 9])
    xref[:, 0] = x
    xref[:, 1] = y
    xref[:, 2] = z
    xref[:, 3] = vx
    xref[:, 4] = vy
    xref[:, 5] = vz
    xref[:, 6] = ax
    xref[:, 7] = ay
    xref[:, 8] = az

    uref = np.zeros([t.shape[0], 3])
    uref[:, 0] = jx * xy_Tc + ax
    uref[:, 1] = jy * xy_Tc + ay
    uref[:, 2] = jz * z_Tc + az

    xref = xref[::downsample_mult]
    uref = uref[::downsample_mult]
    t = t[::downsample_mult]

    return xref, uref, t
