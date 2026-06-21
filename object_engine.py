import vispy
from vispy import app
vispy.use("PyQt6")
import sys
from vispy import scene
from vispy.scene import SceneCanvas
from vispy.scene.visuals import Polygon, Ellipse, Rectangle, RegularPolygon
from vispy.color import Color

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


if __name__ == "__main__" and sys.flags.interactive == 0:
    canvas = _object_engine('Object Example', "cube", [1, 1, 1], "yellow", "black")
    canvas._create_scene()