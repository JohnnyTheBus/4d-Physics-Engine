import math
import numpy as np

# OpenGL related imports for creating a scene and timer.
import vispy
vispy.use("PyQt6")
from vispy import scene
from vispy.app import Timer

# Try accessing Cuda for operations, otherwise default to cpu
try:
    import cupy as cp 
    name = cp.cuda.runtime.getDeviceProperties(0)["name"].decode()
    GPU_AVAILABLE = True
    print(f"GPU: {name}")
except:
    GPU_AVAILABLE = False
    print(f"GPU is not available ({e}). Using CPU instead.")

class Simulation:
    def __init__(self, use_gpu=True) -> None: # We will need to pass all our variables to our simulation generator here.
        

        self.use_gpu = use_gpu and GPU_AVAILABLE


def _world_engine():
    print("Creating World.")
    sim = Simulation(use_gpu=True)

    canvas = scene.SceneCanvas(
        title="4d World Simulation",
        size=(1100, 850),
        show=True,
        bgcolor="grey",
        keys="interactive",
        resizable=True, # Allows users to resize the screen.
        fullscreen=False,
        decorate=True, # Gives a toggle to titles.
        vsync=True, # Auto locks framerate to users monitor refresh rate.
    )
    view = canvas.central_widget.add_view()
    view.camera = scene.cameras.TurntableCamera(
        fov=40,
        elevation=0, # Starting at orgin 0 height.
        azimuth=35, # Sets inital viewpoint angle.
        distance=14, # distance away from origin camera starts.
        up="+z", # registers z axis as up.
        interactive=True, # Set this false if you do not want user to have access to the inputs during simulation.
    )

    # markers = scene.visuals.Markers() # Add data here to have it visually appear at each set marker.

    # Adding a 3d axis marker.
    axis_len = 0.5
    for direction, clr in [
        ([axis_len,0,0], [1,0,0,0.6]),
        ([0,axis_len,0], [0,1,0,0.6]),
        ([0,0,axis_len], [0,0,1,0.6]),
    ]:
        scene.visuals.Line(
            pos=np.array([[0,0,0], direction], dtype=np.float32),
            color=clr,
            parent=view.scene,
            width=2,
        )
    
    timer = Timer(interval=1.0 / 60.0, start=True)
    vispy.app.run()
    return timer # Helps keep the reference alive.




if __name__ == "__main__":
    print("Starting Program")
    sim1 = _world_engine()