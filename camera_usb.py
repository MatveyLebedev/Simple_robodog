import nanocamera as nano
import matplotlib.pyplot as plt
# Create the Camera instance for No rotation (flip=0) with size of 640 by 480
camera = nano.Camera(camera_type=1, device_id=0, width=1280, height=720, fps=30)

print(camera.isReady())

#nvgstcapture-1.0 --camsrc=0 --cap-dev-node=0
#nvgstcapture-1.0 --mode=2 --automate --capture-aut
