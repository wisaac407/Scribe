# Scribe
Have you ever rendered out an animation in [blender][0], then a few weeks later come back to it and wish you remembered what settings you had used to render it? If you have, this addon is for you. With Scribe you can write all the render settings to a text file for later reference.

## Installation
Same as any addon. Download the .zip file, then in the blender user preferences click Install from file, find the .zip and click install. After it's installed be sure to enable it in the user preferences.

## How to use
After it's been installed, it should show up in the render section of the properties window. Before you can use it you need to click the checkbox on the tab header to tell blender to use it when rendering. At this point all you need to do is render out an animation. After the animation is complete you should see a file called `render-settings.txt` in your render directory.

## Options

* **File Name**: The name of the output file relative to the output directory. Default is 'render-settings.txt'
* **Use all hooks**: If checked, Scribe will save all the render settings. Otherwise you can choose which hooks you want to render out.

[0]: http://www.blender.org
