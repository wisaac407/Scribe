"""
render_hook.py: Base class for all hooks.

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


class RenderHook:
    """Base class for all settings hooks.

    Doc string will become the tooltip."""
    # Really no need for this to be changed in any instances.
    hook_label = 'Unset'  # Every sub-class should define their own name.
    hook_idname = ''  # This is how other hooks can reference this one.
    hook_group = 'default'  # Hooks can be assigned to layout groups.

    @classmethod
    def poll(cls, context):
        """Return true if this hook can be used with current context."""
        return True

    def __init__(self, scene):
        self.scene = scene

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
