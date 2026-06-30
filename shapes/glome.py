"""4D geometry + 4D to 3D projection, rendered with vispy (which does 3D to 2D).

The pipeline:  4D world to our code to  3D  to vispy/GPU to 2D screen

A glome is the 4D analogue of a sphere.
"""
import itertools
import numpy as np

import vispy
vispy.use("PyQt6")
from vispy import scene
from vispy.app import Timer

speed = 0.003
movement = [1,0,0,1]
rotation_speed = 0.0000001

#Geometry in 4d
def glome(n_psi=8, n_theta=8, n_phi=8): # each arg being the number of samples we are taking

    #take evely spaced points around 
    psi_values = np.linspace(0, np.pi, n_psi) 
    theta_values = np.linspace(0, np.pi, n_theta)
    phi_values = np.linspace(0, 2 * np.pi, n_phi, endpoint=False)  # phi wraps around

    vertices, vertex_index = [], {}
    for psi_i, psi in enumerate(psi_values):
        for theta_i, theta in enumerate(theta_values):
            for phi_i, phi in enumerate(phi_values): 
                vertex_index[(psi_i, theta_i, phi_i)] = len(vertices)
                sin_psi, sin_theta = np.sin(psi), np.sin(theta)
                vertices.append((sin_psi * sin_theta * np.cos(phi), sin_psi * sin_theta * np.sin(phi),    sin_psi * np.cos(theta), np.cos(psi)))
    vertices = np.array(vertices, dtype=np.float32)

    #Connect each grid point to its successor along each parameter. phi is periodic so it wraps, psi/theta are open so they stop at the boundary.
    edges = []
    for psi_i, theta_i, phi_i in itertools.product(range(n_psi), range(n_theta), range(n_phi)):
        current = vertex_index[(psi_i, theta_i, phi_i)]
        if psi_i + 1 < n_psi:
            edges.append((current, vertex_index[(psi_i + 1, theta_i, phi_i)]))
        if theta_i + 1 < n_theta:
            edges.append((current, vertex_index[(psi_i, theta_i + 1, phi_i)]))
        edges.append((current, vertex_index[(psi_i, theta_i, (phi_i + 1) % n_phi)])) #need to mod here since loop
    return vertices, np.array(edges)


#Rotation in a plane (4D rotates in planes, not about axes, which feels insane)
def rotation_4d(plane, angle):
    axis_a, axis_b = plane
    matrix = np.eye(4, dtype=np.float32)
    cos_angle, sin_angle = np.cos(angle), np.sin(angle)
    matrix[axis_a, axis_a], matrix[axis_a, axis_b] = cos_angle, -sin_angle
    matrix[axis_b, axis_a], matrix[axis_b, axis_b] = sin_angle, cos_angle
    return matrix


#Translation in 4d. Moving is just adding an offset
def move_4d(position, direction, speed):
    return position + np.asarray(direction, dtype=np.float32) * speed


#Perspective projection 4d to 3d
def project_to_3d(verts4, distance=3.0):
    factor = distance / (distance - verts4[:, 3:4])  # shape (N, 1),broadcasts over xyz
    return verts4[:, :3] * factor


#Render
def main():
    verts4, edges = glome()

    canvas = scene.SceneCanvas(title="Glome", size=(900, 900),
                               bgcolor="black", keys="interactive", show=True)
    view = canvas.central_widget.add_view()
    view.camera = scene.cameras.TurntableCamera(fov=45, distance=6)

    line = scene.visuals.Line(connect=edges, color="cyan", width=1, parent=view.scene)

    state = {"angle": 0.0, "position": np.zeros(4, dtype=np.float32)}

    def on_timer(_event):
        state["angle"] += rotation_speed
        # Rotate in two w-planes so the surface turns "inside-out" through 4D. harvested from tesseract
        rotation = rotation_4d((0, 3), state["angle"]) @ rotation_4d((2, 3), state["angle"])
        state["position"] = move_4d(state["position"], movement, speed)
        # rotate first, then translate (add), then project
        line.set_data(pos=project_to_3d(verts4 @ rotation.T + state["position"]))

    timer = Timer(interval=1 / 60, connect=on_timer, start=True)
    vispy.app.run()
    return timer  # keep alive


#main
if __name__ == "__main__":
    main()