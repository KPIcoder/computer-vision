import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import random

def create_parallelepiped():
    p = np.array([
        [0, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 1, 0, 1],
        [0, 1, 0, 1],

        [0, 0, 2, 1],
        [1, 0, 2, 1],
        [1, 1, 2, 1],
        [0, 1, 2, 1]
    ])
    
    return p

def project_xy(parallelepiped):
    projection_matrix = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],  
        [0, 0, 0, 1]
    ])
    
    xy_projection = np.dot(parallelepiped, projection_matrix.T)
    
    return xy_projection


def rotate_parallelepiped_around_z(parallelepiped, theta_degrees):
    theta = np.radians(theta_degrees)
    
    rotation_matrix_z = np.array([
        [np.cos(theta), -np.sin(theta), 0, 0],
        [np.sin(theta), np.cos(theta), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    
    rotated_parallelepiped = np.dot(parallelepiped, rotation_matrix_z.T)
    
    return rotated_parallelepiped


def init_figure():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim([-1.5, 1.5])
    ax.set_ylim([-1.5, 1.5])
    ax.set_zlim([-1.5, 1.5])
    return fig, ax


def draw_parallelepiped(ax, parallelepiped, color='blue'):
    vertices = parallelepiped[:, :3]
    faces = [
        [vertices[0], vertices[1], vertices[2], vertices[3]],
        [vertices[4], vertices[5], vertices[6], vertices[7]],
        [vertices[0], vertices[1], vertices[5], vertices[4]],
        [vertices[2], vertices[3], vertices[7], vertices[6]],
        [vertices[1], vertices[2], vertices[6], vertices[5]],
        [vertices[0], vertices[3], vertices[7], vertices[4]],
    ]
    ax.add_collection3d(Poly3DCollection(faces, facecolors=color, linewidths=0.5, edgecolors='r', alpha=0.5))


visible_duration = 3 
invisible_duration = 3

fps = 30
visible_frames = visible_duration * fps
invisible_frames = invisible_duration * fps
total_cycle_frames = visible_frames + invisible_frames

current_color = [0.5, 0.5, 0.5]
current_translation = np.array([0, 0, 0, 0])


def update_animation(frame, p, ax):
    ax.cla()
    ax.set_xlim([-3, 3])
    ax.set_ylim([-3, 3])
    ax.set_zlim([-3, 3])
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_zlabel('Z Axis')

    cycle_phase = frame % total_cycle_frames

    if cycle_phase < visible_frames:
        rotated_p = rotate_parallelepiped_around_z(p, cycle_phase * (360 / visible_frames))

        if cycle_phase == 0:
            global current_color, current_translation
            current_color = [random.random() for _ in range(3)]
            dx, dy, dz = random.uniform(-2, 2), random.uniform(-2, 2), 0
            current_translation = np.array([dx, dy, dz, 0])

        translated_p = rotated_p + current_translation
        draw_parallelepiped(ax, translated_p, color=current_color)

    return ax,


fig, ax = init_figure()
p = create_parallelepiped()
ani = FuncAnimation(fig, update_animation, frames=np.arange(0, 360, 2), fargs=(p, ax), blit=False, interval=1000 / fps)
plt.show()
