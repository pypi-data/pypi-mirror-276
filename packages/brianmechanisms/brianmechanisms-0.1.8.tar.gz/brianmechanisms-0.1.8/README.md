# Brian Mechanisms
Brian Mechanisms is a Python module designed for engineers and developers to easily design and simulate various mechanical mechanisms and robots. It provides a collection of tools and algorithms for kinematic analysis, motion planning, and visualization of mechanical systems.

## Features
- Kinematic analysis for various types of mechanisms, including linkages, gears, and robotic arms.
- Motion planning algorithms for path generation and trajectory optimization.
- Visualization tools to create interactive plots and animations of mechanical systems.
- Integration with popular libraries such as NumPy and Matplotlib for scientific computing and visualization.

## Installation
ou can install Brian Mechanisms using pip:

```bash
Copy code
pip install brianmechanisms
```

## Usage
### Locii
The `Locii` class is used for plotting and/or animating output paths of rigid link mechanisms with a `θ` input. Each link has a number of `points` whose lengths are given relative to the pivot point for that mechanism. The pivot point has its length set to `0`.

### Link Configuration
Each link is defined by a dictionary containing the following keys:

- `points`: A dictionary defining the points on the link and their respective lengths.
- `speed`: The speed of the link (optional).
- `equation`: A string representing the equation for the displacement of the link.
- `origin`: The origin point of the link.
- `len_factor`: A length factor for scaling the link (optional).
- `speed_factor`: A factor for scaling the speed of the link (optional).
- `speed_source`: The source of the speed, referencing another link's speed (optional).
- `theta0`: The initial angle for the link (optional).
- `output`: The output point of the link (optional).

Example of defining links:

```python
link1 = {
    "points": {
         "O": 0, "A": 1
    },
    "speed": 1,
    "equation": "np.cos(x), np.sin(x)",
    "origin": "{0,0}"
}

link2 = {
    "points": {
        "A": 0, "B": 1
    },
    "len_factor": 1,
    "speed_factor": 2,
    "speed_source": "link1.speed",
    "equation": "np.cos(speed_factor * speed_source * x), np.sin(speed_factor * speed_source * x)",
    "origin": "link1.A",
    "theta0": 1,
    "output": "B"
}
```


### Plotting the Locus
By default, the function will plot the loci of all the given points of the mechanism using dashed lines. The output is plotted using a solid line, specified by the output property in the link's settings.

#### Plotting the Mechanism
To draw the mechanism in addition to the loci, define the mechanism_theta property. The mechanism will be drawn at `0 = mechanism_theta`.


#### Examples
##### Tusi Couple
This example demonstrates how to define links and use the `Locii` class to plot and animate the Tusi Couple mechanism.

```python
from brianmechanisms import Locii
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

link1 = {
    "points": {
         "O": 0, "A": 1
    },
    "speed": 1,
    "equation": "np.cos(x), np.sin(x)",
    "origin": "{0,0}"
}

link2 = {
    "points": {
        "A": 0, "B": 1
    },
    "len_factor": 1,
    "speed_factor": 1,
    "speed_source": "link1.speed",
    "equation": "np.cos(speed_factor * speed_source * x), np.sin(speed_factor * speed_source * x)",
    "origin": "link1.A",
    "theta0": 1,
    "output": "B"
}

linksTemplate = {
    "link1": link1.copy(),
    "link2": link2.copy()
}

fig, axs = plt.subplots(1, 1)
locii = Locii(linksTemplate, {})
fig, ax = locii.plotOutPutPaths(title={"title": "Tusi Couple", "sub": "Subtitle Example"}, plotConfig={"ax": axs, "fig": fig, "legend": False, "axes": False, "mechanism_theta": 45, "ani": True})

ani3 = FuncAnimation(fig, locii.update, frames=np.arange(0, 360, 10), fargs=(ax, {"title": "Example Plot", "sub": "Subtitle Example"}, {"ax": axs, "fig": fig, "legend": False, "axes": False, "mechanism_theta": 45, "ani": True}), interval=100)

plt.show()

HTML(ani3.to_jshtml())
```

##### Animating and Saving the Animation
To animate the plot and save it as a video file (e.g., MP4), use the FuncAnimation class from matplotlib.animation and specify the writer (e.g., FFMpegWriter):

```python
from matplotlib.animation import FFMpegWriter

writer = FFMpegWriter(fps=10, metadata={'title': 'Tusi Couple', 'artist': 'brianmechanisms', 'comment': 'Tusi Couple Animation'})
ani3.save('tusicouple.mp4', writer=writer)
```

This documentation provides a basic overview of how to use the brianmechanisms module, specifically focusing on the Locii class for plotting and animating rigid link mechanisms. For more detailed information and additional features, refer to the official documentation and examples provided in the module.

##### plotConfig Settings
The `plotConfig` dictionary allows you to customize various aspects of your plot and animation. Here are the key settings you can use:

-`ax`: Specifies the Matplotlib axes object to use for plotting. If not provided, a new axes object will be created.
- `fig`: Specifies the Matplotlib figure object to use for the plot. This allows you to add the plot to an existing figure.
- `legend`: A boolean flag that controls whether a legend should be displayed on the plot. If set to False, no legend will be shown.
- `axes`: A boolean flag that controls whether the axes should be displayed on the plot. If set to False, the axes will be hidden.
- `mechanism_theta`: Specifies the angle (in degrees) at which the mechanism should be drawn. This setting allows you to visualize the mechanism at a specific angle.
- `ani`: A boolean flag that indicates whether the plot should be animated. If set to True, the animation will be enabled.


## Hypocycloids

![Tusi Couple](examples/TusiCouple.gif)

![Tusi Couple](examples/TusiCouple1.gif)

![Hypocycloids](examples/hypocycloids.png)

![Hypoctrochoids](examples/hypotrochoids.png)

![Epictrochoids](examples/epitrochoids.png)


