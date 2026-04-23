import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import solve_ivp
from matplotlib.animation import PillowWriter

m = 1.0     # mass (kg)
L = 1.0     # arm length (m)
I = m*L**2  # inertia about pivot (point mass)
g = 9.81

def tau(t):
    return 0.0 # free rotation

def dynamics (t, x):
    theta, theta_dot = x
    theta_c_dot = (np.deg2rad(22*2*np.pi*0.6*np.cos(2*np.pi*0.6*t) + 5*2*np.pi*2.2*np.cos(2*np.pi*2.2*t)))
    theta_ddot = tau(t) / I
    theta_dot = theta_c_dot
    return [theta_dot, theta_ddot]

t_span = (0.0, 6.0)
t_eval = np.arange(0.0, 6.0, 0.02)

x0 = [0.0, 0.0] # initial angle and rate
sol = solve_ivp(dynamics, t_span, x0, t_eval=t_eval)
theta = sol.y[0]
x=L*np.cos(theta)
y=L*np.sin(theta)
z= np.zeros_like(x)

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_zlim(-1.2, 1.2)

# Camera angle (Matplotlib view_init sets elev/azim).
ax.view_init(elev=20, azim=35)

# Gravity direction
ax.quiver(0, 0, 0.25, 0, 0, -0.5, color='k', linewidth=2)

#ax.text(0, 0, -1.1, 'g', color='k')

arm, = ax.plot([], [], [], 'b-', lw=3)

def init():
    arm.set_data([], [])
    arm.set_3d_properties([])
    return arm,

def update(i):
    arm.set_data([0, x[1]], [0, y[i]])
    arm.set_3d_properties([0, z[1]])
    return arm,

ani = FuncAnimation(fig, update, frames=len(t_eval),init_func=init, interval=30)
writer = PillowWriter(fps=int(1/0.02))
ani.save("rot_arm.gif", writer=writer)
plt.show()