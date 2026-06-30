from vispy import scene
from vispy.app import Timer

#our classes
from shapes.Shape import Glome, Tesseract


class ObjectEngine:
    #Owns a vispy scene and animates a collection of shapes.

    def __init__(self, title, shapes):
        self.title = title
        self.shapes = shapes

    def _tick(self, _event):
        for shape in self.shapes:
            shape.update()

    def run(self):
        canvas = scene.SceneCanvas(keys="interactive", title=self.title, show=True)
        view = canvas.central_widget.add_view()
        view.bgcolor = "black"
        view.camera = "turntable" #this has to be, but idk why
        view.padding = 100

        for shape in self.shapes:
            shape.attach(view)

        timer = Timer(interval=1 / 60, connect=self._tick, start=True)
        canvas.app.run()
        return timer  #frankinstien the ref

#main, start point here
ObjectEngine("Tesseract + Tesseract", [Tesseract(color="green", offset=(-1.5, 2, 0), velocity=(1, 0, 0, 1), speed=0.001),Tesseract(color="greens", offset=(1.5, 2, 0), velocity=(1, 0, 0, 1), speed=0.001), ]).run()
