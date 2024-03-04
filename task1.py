import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation

def create_pentagon(size):
    angle = np.deg2rad(360 / 5)
    return [[size * np.cos(i * angle), size * np.sin(i * angle), 1] for i in range(5)]

def normalise_vertices(vertices):
    return [(x / hc, y / hc) for x, y, hc in vertices]

# Функції трансформацій
def move(vertices, dx, dy):
    translation_matrix = np.array([
        [1, 0, dx],
        [0, 1, dy],
        [0, 0, 1]
    ])
    vertices_matrix = np.array(vertices)
    translated_vertices = np.dot(vertices_matrix, translation_matrix.T)

    return translated_vertices.tolist()

def scale(vertices, factor):
    scale_matrix = np.array([
        [factor, 0, 0],
        [0, factor, 0],
        [0, 0, 1]
    ])
    vertices_matrix = np.array(vertices)
    scaled_vertices = np.dot(vertices_matrix, scale_matrix.T)

    return scaled_vertices.tolist()

def rotate(vertices, degree):
    rad = np.deg2rad(degree)
    cos_angle, sin_angle = np.cos(rad), np.sin(rad)
    rotation_matrix = np.array([
        [cos_angle, -sin_angle, 0],
        [sin_angle, cos_angle, 0],
        [0, 0, 1]
    ])
    vertices_matrix = np.array(vertices)
    rotated_vertices = np.dot(vertices_matrix, rotation_matrix.T)
    return rotated_vertices.tolist()

size = 1
vertices = create_pentagon(size)

fig, ax = plt.subplots()
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
normalised_vertices = normalise_vertices(vertices)
pentagon_patch = patches.Polygon(normalised_vertices, closed=True)
ax.add_patch(pentagon_patch)

def draw():
    pentagon_patch.set_xy(normalised_vertices)
    return [pentagon_patch,]

def cycle_rotate(degree):
    rotated = rotate(vertices, degree)
    pentagon_patch.set_xy(normalise_vertices(rotated))
    return [pentagon_patch,]

ani = FuncAnimation(fig, cycle_rotate, frames=np.arange(0, 360, 2), init_func=draw, blit=True)

plt.show()
