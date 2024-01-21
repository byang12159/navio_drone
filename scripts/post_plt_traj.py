from matplotlib import pyplot as plt
import numpy as np
import argparse
import sys
import pickle5 as pickle

parser = argparse.ArgumentParser(description="")
parser.add_argument('--traj', type=str, help='filename to the actual trajectories.')
parser.add_argument('--save', type=bool, default=False, help='boolean to save figure')
args = parser.parse_args()

with open(args.traj, 'rb') as handle:
    data = pickle.load(handle)

data, dt, refs = data
xs, u, ref_ids, xstars, ustars = data[0]

real_t = np.arange(0, len(xs) * dt, dt)

x = xs[:, 0]
y = xs[:, 1]
z = xs[:, 2]
vx = xs[:, 3]
vy = xs[:, 4]
vz = xs[:, 5]
ax = xs[:, 6]
ay = xs[:, 7]
az = xs[:, 8]
print(ax.shape)
print(type(ax))

ref_x = xstars[:, 0]
ref_y = xstars[:, 1]
ref_z = xstars[:, 2]
ref_vx = xstars[:, 3]
ref_vy = xstars[:, 4]
ref_vz = xstars[:, 5]
ref_ax = xstars[:, 6]
ref_ay = xstars[:, 7]
ref_az = xstars[:, 8]

# Compute reference velocity
target_velocity = np.average(np.sqrt(np.square(ref_vx)+np.square(ref_vy)+np.square(ref_vz)))


fig, (xy, timedx, timedv, timeda) = plt.subplots(4, 1, figsize=(14, 10))

xy.plot(ref_x, ref_y, 'k-', label='ref')
xy.plot(x, y, 'g-', label='actual')
xy.set_xlabel('x')
xy.set_ylabel('y')
xy.legend()
xy.axis('equal')

timedx.plot(real_t, x, label='x')
timedx.plot(real_t, y, label='y')
timedx.plot(real_t, z, label='z')
timedx.plot(real_t, ref_x, label='ref_x')
timedx.plot(real_t, ref_y, label='ref_y')
timedx.plot(real_t, ref_z, label='ref_z')
timedx.legend()
timedx.set_title("Postion")

timedv.plot(real_t, vx, label='vx')
timedv.plot(real_t, vy, label='vy')
timedv.plot(real_t, vz, label='vz')
timedv.plot(real_t, ref_vx, label='ref_vx')
timedv.plot(real_t, ref_vy, label='ref_vy')
timedv.plot(real_t, ref_vz, label='ref_vz')
timedv.legend()
timedv.set_title("Velocity")


timeda.plot(real_t, ax, label='ax')
timeda.plot(real_t, ay, label='ay')
timeda.plot(real_t, az, label='az')
timeda.plot(real_t, ref_ax, label='ref_ax')
timeda.plot(real_t, ref_ay, label='ref_ay')
timeda.plot(real_t, ref_az, label='ref_az')
timeda.legend()
timeda.set_title("Acceleration")

#timed.plot(real_t, u[:, 0], label='cmd_ax')
#timed.plot(real_t, u[:, 1], label='cmd_ay')
#timed.plot(real_t, u[:, 2], label='cmd_az')


# error.plot(real_t, x-ref_x, label='error x')
# error.plot(real_t, y-ref_y, label='error y')
# error.plot(real_t, z-ref_z, label='error z')
# error.plot(real_t, vx-ref_vx, label='error Vx')
# error.plot(real_t, vy-ref_vy, label='error Vy')
# error.plot(real_t, vz-ref_vz, label='error Vz')
# error.plot(real_t, ax-ref_ax, label='error Ax')
# error.plot(real_t, ay-ref_ay, label='error Ay')
# error.plot(real_t, az-ref_az, label='error Az')
# error.legend()
# error.set_title("Error")

fig.suptitle(f'{args.traj}', fontsize=16)
plt.tight_layout()

if args.save:
    plt.savefig("traj"+args.traj+".png")

plt.show()


# Create a 3D figure
fig = plt.figure()
axes = fig.add_subplot(111, projection='3d')

print(type(ax))
x = np.zeros(len(ax))
y = np.zeros(len(ay))
z = np.zeros(len(az))

# Plot 3D vectors using ax.quiver
axes.quiver(x, y, z, ax,ay,az, length=0.1, normalize=True, color='b',linewidth=0.5,arrow_length_ratio=0.1)

# Show the plot
plt.show()
