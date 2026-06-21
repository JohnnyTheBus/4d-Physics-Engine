import vispy
from vispy import app
vispy.use("PyQt6")
import sys
from vispy import scene
from vispy.scene import SceneCanvas
from vispy.scene.visuals import Polygon, Ellipse, Rectangle, RegularPolygon
from vispy.color import Color

class _create_cube:
    def __init__(self, scene_title: str, object: str, dimensions: list[float], color: str, edge_color: str) -> None:
        self.scene_title=scene_title
        self.object=object
        self.dimensions=dimensions
        self.color=Color(color)
        self.edge_color=Color(edge_color)

    def _create_cube(self, view):
        cube = scene.visuals.Box(self.dimensions[0], self.dimensions[1], self.dimensions[2], color=self.color, edge_color=self.edge_color, parent=view.scene)
        return cube

    def _create_sphere(self, view):
        # sphere = scene.visuals.Sphere(radius=)
        return

    def _create_scene(self):
        canvas = SceneCanvas(keys='interactive', title=self.scene_title, show=True)
        view = canvas.central_widget.add_view()
        view.bgcolor = 'black'
        view.camera = 'turntable'
        view.padding = 100

        color = Color("yellow")

        if self.object == "cube":
            object = self._create_cube(view)

        canvas.app.run()

class _object_engine:
    def __init__(self, scene_title: str, object: str, dimensions: list[float], color: str, edge_color: str) -> None:
        self.scene_title=scene_title
        self.object=object
        self.dimensions=dimensions
        self.color=Color(color)
        self.edge_color=Color(edge_color)

    def _create_cube(self, view):
        cube = scene.visuals.Box(self.dimensions[0], self.dimensions[1], self.dimensions[2], color=self.color, edge_color=self.edge_color, parent=view.scene)
        return cube
    
    def _create_sphere(self, view):
        # sphere = scene.visuals.Sphere(radius=)
        return

    def _create_scene(self):
        canvas = SceneCanvas(keys='interactive', title=self.scene_title, show=True)
        view = canvas.central_widget.add_view()
        view.bgcolor = 'black'
        view.camera = 'turntable'
        view.padding = 100

        color = Color("yellow")

        if self.object == "cube":
            object = self._create_cube(view)

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
        

if __name__ == "__main__" and sys.flags.interactive == 0:
    _terminal_ui()
    # canvas = _object_engine('Object Example', "cube", [1, 1, 1], "yellow", "black")
    # canvas._create_scene()