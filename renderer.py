"""
renderer.py: The class that will keep track of hooks and handle outputting the stats file.

Copyright (C) 2015 Isaac Weaver
Author: Isaac Weaver <wisaac407@gmail.com>

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""


import os
import bpy


class RenderHook:
    """
    Base class for all settings hooks.

    Doc string will become the tooltip.
    """
    # Really no need for this to be changed in any instances.
    hook_label = 'Unset'  # Every sub-class should define their own name.
    hook_idname = ''  # This is how other hooks can reference this one.
    hook_group = 'default'  # Hooks can be assigned to layout groups.
    hook_handler = None

    @classmethod
    def poll(cls, context):
        """Return true if this hook can be used with current context."""
        return True

    def __init__(self, scene):
        self.scene = scene
        self.handler = self.hook_handler()

    def get_result(self):
        """
        Called by the renderer to get the final result form this hook
        
        Most hooks won't have to override this method.
        """

        self.handler.data = self.post_render()
        return self.handler.dump()

    def pre_render(self):
        """Called before the rendering starts."""

    def post_render(self):
        """Called after all the rendering has finished."""
        # Every instance should implement this function.
        raise NotImplementedError

    def pre_frame(self):
        """Called before the rendering of each frame."""

    def post_frame(self):
        """Called after the rendering of each frame"""


_registered_hooks = []
_registered_groups = {'default': ('General', 0)}
_group_id = 1


def register_hook(hook):
    """Add hook to the list of available hooks and add a bool property to the property group."""
    _registered_hooks.append(hook)

    # Sort the list of hooks based on the hook groups.
    def get_group(h):
        if h.hook_group not in _registered_groups:
            raise Exception("Group '%s' has not yet been registered." % h.hook_group)
        return _registered_groups[h.hook_group][1]
    _registered_hooks.sort(key=get_group)

    setattr(bpy.types.ScribeRenderSettings, hook.hook_idname, bpy.props.BoolProperty(
        name=hook.hook_label,
        description=hook.__doc__,
        default=True
    ))


def register_group(idname, label):
    global _group_id
    _registered_groups[idname] = (label, _group_id)
    _group_id += 1


def get_hooks():
    return _registered_hooks


def get_group(idname):
    return _registered_groups[idname]


class Renderer:
    """Hold the current state of the render, ie if currently rendering."""

    def __init__(self, scene):
        self.scene = scene
        self._active_hooks = []
        self.can_render = False  # Weather or not the settings should be rendered.

        # For every active hook, initialize it with the current scene, run the pre_render function
        # and add it to the active hooks list.

        advanced_settings = scene.scribe.advanced_settings
        for hook in _registered_hooks:
            # Only add it if it's active and available in the current context.
            if (not advanced_settings or getattr(scene.scribe, hook.hook_idname)) and hook.poll(bpy.context):
                hook = hook(scene)
                hook.pre_render()
                self._active_hooks.append(hook)

    def render(self):
        # Return if we can't render.
        if not self.can_render:
            return
        # Get the file paths.
        render_dir = bpy.path.abspath(self.scene.render.filepath)
        path = os.path.join(render_dir, self.scene.scribe.filename)

        ### Collect all the data.
        s = self.format_render_data()
        print(s)

        ### Write the data to the info file.
        with open(path, 'w') as f:
            f.write(s)

    def frame_begin(self):
        for hook in self._active_hooks:
            hook.pre_frame()

    def frame_complete(self):
        for hook in self._active_hooks:
            hook.post_frame()

    def format_render_data(self):
        maxlen = 0
        for hook in self._active_hooks:
            if len(hook.hook_label) > maxlen:
                maxlen = len(hook.hook_label)
        template = '{name:>%s}: {data}' % (maxlen + 1)

        s = ""
        lastgroup = ''
        for hook in self._active_hooks:
            if hook.hook_group != lastgroup:
                s += '\n\n %s:\n%s\n' % (_registered_groups[hook.hook_group][0], '='*50)
                lastgroup = hook.hook_group
            s += template.format(name=hook.hook_label, data=hook.get_result())
            s += '\n'
        return s[2:]  # Cut out the first new line character.
