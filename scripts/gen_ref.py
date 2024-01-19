#!/usr/bin/env python
import numpy as np
import argparse
import importlib
import pickle5 as pickle
from matplotlib import pyplot as plt
from DroneExperiments.core.refs.gen_xref_uref_from_xyz import gen_xref_uref_from_xyz
from DroneExperiments.core.constants import dt, xy_Tc, z_Tc
from functools import partial

parser = argparse.ArgumentParser(description="")
parser.add_argument('--T', type=float, default=30., help='Time horizon of the curve.')
parser.add_argument('--save', type=str, help='Filename to save the data.')
parser.add_argument('--type', type=str, default='lemniscate', help='Type of curve.')
parser.add_argument('--vis', dest='vis', action='store_true', help='Visualize the curve.')
parser.set_defaults(vis=True)
parser.add_argument('--gen_args', nargs='+', default=[1.0,1.0,10.0], type=float, help='Arguments to the curve generator.')
args = parser.parse_args()

curve_gen = importlib.import_module('DroneExperiments.core.refs.'+args.type)

def gen_xref_uref(xyz):
    xyz = partial(xyz, args.gen_args)
    xref, uref, t = gen_xref_uref_from_xyz(xyz, args.T, dt)
    start_position = xref[0,:3]

    if args.save:
        with open(args.save, 'wb') as handle:
            pickle.dump({'start_position': start_position, 'xref': xref, 'uref': uref}, handle, protocol=pickle.HIGHEST_PROTOCOL)

    if args.vis:
        fig = plt.figure(figsize=(20, 10))
        xy = fig.add_subplot(2, 1, 1)
        timed = fig.add_subplot(2, 1, 2)
        xy.plot(xref[:,0], xref[:,1])
        xy.set_xlabel('x')
        xy.set_ylabel('y')

        timed.plot(t, xref[:, 0], label='x')
        timed.plot(t, xref[:, 1], label='y')
        timed.plot(t, xref[:, 3], label='vx')
        timed.plot(t, xref[:, 4], label='vy')
        timed.plot(t, xref[:, 6], label='ax')
        timed.plot(t, xref[:, 7], label='ay')
        timed.legend()

        plt.show()

gen_xref_uref(curve_gen.xyz)    
