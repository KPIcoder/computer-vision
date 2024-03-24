import numpy as np
from scipy.interpolate import CubicSpline
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt

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


def painter_algorithm(faces, vertices):
    # Calculate the depth of each face as the average of the z-coordinates of its vertices
    depths = np.array([np.mean([vertices[vert][2] for vert in face]) for face in faces])
    # Sort the faces by depth
    sorted_faces_indices = np.argsort(depths)[::-1]  
    sorted_faces = [faces[i] for i in sorted_faces_indices]
    return sorted_faces


keyframes = np.array([0, 45, 90, 180, 360])
angles = np.radians(keyframes)

t = np.linspace(0, 1, len(keyframes))

cs = CubicSpline(t, angles)

def display_rotated_parallelepiped(t_values):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    p = create_parallelepiped()
    faces_indices = [
        [0, 1, 2, 3], [4, 5, 6, 7],  
        [0, 1, 5, 4], [2, 3, 7, 6], 
        [1, 2, 6, 5], [0, 3, 7, 4]   
    ]
    
    for t_val in t_values:
        ax.cla()
        
        # Interpolate the angle then rotate at this t value
        theta = cs(t_val)
        rotated_p = rotate_parallelepiped_around_z(p, np.degrees(theta))
        
        vertices = rotated_p[:, :3]  # Ignore the homogeneous coordinate
        
        # Sort faces by depth using the Painter's Algorithm
        sorted_faces_indices = painter_algorithm(faces_indices, vertices)

        colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta']
        
        for i, face_indices in enumerate(sorted_faces_indices):
            face = vertices[face_indices]
            poly = Poly3DCollection([face], facecolors=colors[i], linewidths=1, edgecolors='k', alpha=0.9)
            ax.add_collection3d(poly)
        
        ax.set_xlim([-2, 2])
        ax.set_ylim([-2, 2])
        ax.set_zlim([-2, 2])
        plt.draw()
        plt.pause(0.05)
        
    plt.show()

display_rotated_parallelepiped(np.linspace(0, 1, 1000))