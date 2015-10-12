# Scribe
Have you ever rendered out an animation in [blender][0], then a few weeks later come back to it and wish you remembered what settings you had used to render it? If you have, this addon is for you. With Scribe you can write all the render settings to a text file for later reference.

## Installation
Same as any addon. Download the .zip file, then in the blender user preferences click Install from file, find the .zip and click install. After it's installed be sure to enable it in the user preferences.

## How to use
After it's been installed, it should show up in the render section of the properties window. Before you can use it you need to click the checkbox on the tab header to tell blender to use it when rendering. At this point all you need to do is render out an animation. After the animation is complete you should see a file called `render-settings.txt` in your render directory.

## Options

* **File Name**: The name of the output file relative to the output directory. Default is 'render-settings.txt'
* **Use all hooks**: If checked, Scribe will save all the render settings. Otherwise you can choose which hooks you want to render out.


### Render hooks:

####General:
* **Render engine**: Which render engine is used to render.
* **Time**: Total render time.
* **Frame Rate**: Frame rate of the rendered animation.
* **Frame Range**: The output frame range.

####Output Resolution:
* **Resolution**: Target resolution.
* **True resolution**: Actual output resolution.

####Seed:
* **Seed**: Cycles sampling seed.
* **Seed is Animated**: Weather or not the seed is animated from frame to frame.

####Volume Sampling:
* **Step Size**: Cycles volume step size.
* **Max Steps**: Maximum number of cycles volume steps.

####Performance:
* **Tile Size**: Tile size.
* **Tile Order**: Cycles tile order.
* **Threads Mode**: Which scheme is used to determine the number of threads.
* **Threads**: How many threads are being used to render.

####Bounces:
* **Total Bounds**: Bounds of the number of reflection bounces.
* **Diffuse**: Maximum number of diffuse reflection bounces.
* **Glossy**: Maximum number of glossy reflection bounces.
* **Transmission**: Maximum number of transmission reflection bounces.
* **Volume**: Maximum number of volume reflection bounces.

####Light Paths:
* **Shadows**: Use transparency of surfaces for rendering shadows.
* **Reflective Caustics**: Using reflective caustics.
* **Refractive Caustics**: Using refractive caustics.
* **Filter Glossy**: Cycles filter glossy threshold.

####Sampling:
* **Samples**: Number of cycles samples used(accounting for square samples).
* **Clamp Direct**: How much we are clamping direct light.
* **Clamp Indirect**: How much we are clamping indirect light.

[0]: http://www.blender.org
