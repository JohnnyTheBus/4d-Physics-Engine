import vispy
from vispy import app
vispy.use("PyQt6")
import sys
from vispy import scene
from vispy.scene import SceneCanvas
from vispy.scene.visuals import Polygon, Ellipse, Rectangle, RegularPolygon
from vispy.color import Color

import numpy as np

class _create_tesseract:
    def __init__(self, object: str, scene_title: str, scale: float, color: str, viewer_distance: float):
        self.object = object
        self.scene_title = scene_title
        self.scale = scale
        self.color = Color(color)
        self.viewer_distance = viewer_distance
        self.angle_xw = 0.0
        self.angle_yw = 0.0
        self._build_geometry()

    def _build_geometry(self):
        coords = [-1.0, 1.0]
        self.vertices_4d = np.array(
            [[x, y, z, w] for x in coords for y in coords for z in coords for w in coords]
        ) * self.scale
        self.edges = [
            (i, j) for i in range(16) for j in range(i + 1, 16)
            if np.sum(self.vertices_4d[i] != self.vertices_4d[j]) == 1
        ]

    def _rotate_xw(self, verts, a):
        R = np.eye(4)
        R[0, 0] = R[3, 3] = np.cos(a)
        R[0, 3] = -np.sin(a)
        R[3, 0] =  np.sin(a)
        return verts @ R.T

    def _rotate_yw(self, verts, a):
        R = np.eye(4)
        R[1, 1] = R[3, 3] = np.cos(a)
        R[1, 3] = -np.sin(a)
        R[3, 1] =  np.sin(a)
        return verts @ R.T

    def _project_to_3d(self, verts):
        w = verts[:, 3]
        s = self.viewer_distance / (self.viewer_distance - w)
        return verts[:, :3] * s[:, np.newaxis]

    def _get_line_segments(self):
        rotated = self._rotate_yw(self._rotate_xw(self.vertices_4d, self.angle_xw), self.angle_yw)
        projected = self._project_to_3d(rotated)
        segments = []
        for i, j in self.edges:
            segments.extend([projected[i], projected[j]])
        return np.array(segments)


class _create_cube:
    def __init__(self, scene_title: str, object: str, dimensions: list[float], color: str, edge_color: str) -> None:
        self.scene_title=scene_title
        self.object=object
        self.dimensions=dimensions
        self.color=Color(color)
        self.edge_color=Color(edge_color)

class _scene_engine:
    def __init__(self, shape_type):
        self.type=shape_type

    def _create_cube(self, view):
        cube = scene.visuals.Box(self.type.dimensions[0], self.type.dimensions[1], self.type.dimensions[2], color=self.type.color, edge_color=self.type.edge_color, parent=view.scene)
        return cube

    def _create_tesseract(self, view):
        tesseract = scene.visuals.Line(
            pos=self.type._get_line_segments(),
            color=self.type.color,
            connect='segments',  # treat every pair of points as one segment
            parent=view.scene
        )
        return tesseract

    def _create_scene(self):
        canvas = SceneCanvas(keys='interactive', title=self.type.scene_title, show=True)
        view = canvas.central_widget.add_view()
        view.bgcolor = 'black'
        view.camera = 'turntable'
        view.padding = 100

        color = Color("yellow")

        if self.type.object == "cube":
            object = self._create_cube(view)
        elif self.type.object == "tesseract":
            object = self._create_tesseract(view)

        canvas.app.run()

def _terminal_ui():
    print(80*"=")
    print("= User Module for showing 4 dimensonial objects in a 3d plane.")
    print(80*"=")
    
    print("Shape options")
    print(80*"-")
    print("1. Cube\n2. Sphere")
    object_type = input("What shape type would you like to visualize? ")

    object_type = object_type.lower()
    if object_type == "cube":
        scene_title = "Cube Represented in 4D"

        print("Select Cube Dimensions, input should look like 1,2,3 separating each dimension by a comma")
        print(80*"-")
        user_dimensions = input("Input user dimensions: ")
        dimensions = user_dimensions.split(",")
        dimensions = list(map(int, dimensions))
        print(dimensions)

        print("select shape colouring")
        print(80*"-")
        base_colour = input("Input fill colour for cube (e.g. yellow): ")
        border_colour = input("Input border colour (e.g. black): ")

        canvas = _create_cube(scene_title, object_type, dimensions, base_colour, border_colour)
        canvas._create_scene()

    else:
        print("This shape has not been added.")
        

if __name__ == '__main__' and sys.flags.interactive == 0:
    # _terminal_ui()
    # canvas = _create_cube('Object Example', "cube", [1, 1, 1], "yellow", "black")
    # set1 = _scene_engine(canvas)
    # set1._create_scene()

    t = _create_tesseract("tesseract", "Tesseract", scale=1.0, color="red", viewer_distance=7.0)
    tesseract_scene = _scene_engine(t)
    tesseract_scene._create_scene()

    # canvas = _object_engine('Object Example', "cube", [1, 1, 1], "yellow", "black")
    # canvas._create_scene()
