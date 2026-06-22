"""4D geometry + 4D to 3D projection, rendered with vispy (which does 3D to 2D).

The pipeline:  4D world to our code to  3D  to vispy/GPU to 2D screen

A tesseract is the 4D analogue of a cube.
"""
import itertools
import numpy as np

import vispy
vispy.use("PyQt6")
from vispy import scene
from vispy.app import Timer


#Geometry in 4d
def tesseract():
    """16 vertices (every +/-1 combo) and 32 edges (differ in one coord)."""
    vertices = np.array(list(itertools.product((-1, 1), repeat=4)), dtype=np.float32)
    edges = [(vertex_a, vertex_b) for vertex_a, vertex_b in itertools.combinations(range(len(vertices)), 2)
        if np.count_nonzero(vertices[vertex_a] != vertices[vertex_b]) == 1 ] # exactly one axis differs
    return vertices, np.array(edges)


#Rotation in a plane (4D rotates in planes, not about axes)
def rotation_4d(plane, angle):
    """4x4 rotation in the given plane, e.g. plane=(0, 3) is the xw-plane."""
    axis_a, axis_b = plane
    matrix = np.eye(4, dtype=np.float32)
    cos_angle, sin_angle = np.cos(angle), np.sin(angle)
    matrix[axis_a, axis_a], matrix[axis_a, axis_b] = cos_angle, -sin_angle
    matrix[axis_b, axis_a], matrix[axis_b, axis_b] = sin_angle, cos_angle
    return matrix


# Perspective projection 4d to 3d
def project_to_3d(verts4, distance=3.0):
    """Push points "toward" the 4D viewer: larger w => bigger. distance=inf is orthographic."""
    factor = distance / (distance - verts4[:, 3:4])  # shape (N, 1), broadcasts over xyz
    return verts4[:, :3] * factor


# Render
def main():
    verts4, edges = tesseract()

    canvas = scene.SceneCanvas(title="Tesseract", size=(900, 900),
                               bgcolor="black", keys="interactive", show=True)
    view = canvas.central_widget.add_view()
    view.camera = scene.cameras.TurntableCamera(fov=45, distance=6)

    line = scene.visuals.Line(connect=edges, color="cyan", width=2, parent=view.scene)

    state = {"angle": 0.0} 

    def on_timer(_event):
        state["angle"] += 0.01
        # Rotate in two w-planes so the surface turns "inside-out" through 4D.
        rotation = rotation_4d((0, 3), state["angle"]) @ rotation_4d((2, 3), state["angle"] * 0.7)
        line.set_data(pos=project_to_3d(verts4 @ rotation.T))

    timer = Timer(interval=1 / 60, connect=on_timer, start=True)
    vispy.app.run()
    return timer  # keep alive

#main
if __name__ == "__main__":
    main()