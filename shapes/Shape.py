"""4D geometry + 4D to 3D projection, rendered with vispy (which does 3D to 2D).

The pipeline:  4D world to our code to  3D  to vispy/GPU to 2D screen

Base shape code"""

from abc import ABC, abstractmethod

import numpy as np
from vispy import scene

#geometry
from shapes.glome import glome, rotation_4d, project_to_3d, move_4d
from shapes.tesseract import tesseract


class Shape(ABC):
#basis for 4d shapes, only desgined to handle basic shapes
    @abstractmethod
    def attach(self, view):
        #Create this shape's visual
        pass
    def update(self):
        #march one animation frame. Static shapes need not override since they technically arent animated. 
        pass

class Wireframe4D(Shape):
    #A 4D wireframe: spin in 4d, project to 3d, let vispy do 3d to screen

    width = 1  # override for a GIRTHIER line

    def __init__(self, geometry, scale=1.0, color="cyan", offset=(0, 0, 0),
                 velocity=(0, 0, 0, 0), speed=0.0):
        verts4, self.edges = geometry()
        self.verts4 = (verts4 * scale).astype("float32")
        self.color = color
        self.offset = np.asarray(offset, dtype="float32")
        self.angle = 0.0
        self.position4 = np.zeros(4, dtype="float32")  # where the shape sits in 4D
        self.velocity = np.asarray(velocity, dtype="float32")  # 4D direction to drift each frame
        self.speed = speed

    def attach(self, view):
        self.line = scene.visuals.Line(connect=self.edges, color=self.color,
                                       width=self.width, parent=view.scene)
        self.update()

    def update(self):
        self.angle += 0.01
        self.move_4d(self.velocity, self.speed)  # drift through 4D each frame
        # Rotate in two w-planes for the classic "inside-out" roll
        r = rotation_4d((0, 3), self.angle) @ rotation_4d((2, 3), self.angle * 0.7)
        # rotate, then translate in 4D (add), then project to 3D, then nudge by the 3D offset
        rotated = self.verts4 @ r.T + self.position4
        self.line.set_data(pos=project_to_3d(rotated) + self.offset)

    def move_4d(self, direction, speed):
        # accumulate a step into the 4D position; update() applies it next frame
        self.position4 = move_4d(self.position4, direction, speed)
        return self.position4


#need to make these for new basis shapes

class Glome(Wireframe4D):
#inheirits everything from shapes/glome.py
    def __init__(self, **kwargs):
        super().__init__(glome, **kwargs)


class Tesseract(Wireframe4D):
#inheirits everything from shapes/tesseract.py
    width = 2
    def __init__(self, **kwargs):
        super().__init__(tesseract, **kwargs)
