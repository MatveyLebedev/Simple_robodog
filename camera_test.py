import nanocamera as nano
import matplotlib.pyplot as plt
# Create the Camera instance for No rotation (flip=0) with size of 1280 by 800
camera = nano.Camera(device_id=1, flip=0, width=1280, height=800, fps=30)

frame = camera.read()
print(frame)
plt.imshow(frame)
