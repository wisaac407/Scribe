"""
__init__.py: Pull together the entire add-on, provide the register/unregister functions.

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

import bpy
from bpy.app.handlers import persistent

from SRDRenderer import SRDRenderer

import hooks.cycles
import hooks.general

srd_renderer = None


def cleanup(scene):
    """Remove any intermediate props stored on the scene."""
    global srd_renderer
    srd_renderer = None


@persistent
def render_write(scene):
    # If we are writing a file then we should be writing the stats also.
    srd_renderer.can_render = True

@persistent
def render_cancel(scene):
    """Just cleanup the scene because rendering was canceled."""
    cleanup(scene)

@persistent
def render_init(scene):
    """Initialize the intermediate props set on the scene."""
    global srd_renderer
    srd_renderer = SRDRenderer(scene)

@persistent
def render_complete(scene):
    # If we haven't written any files then we shouldn't write our stats.
    srd_renderer.render()
    cleanup(scene)

@persistent
def render_pre(scene):
    srd_renderer.frame_begin()

@persistent
def render_post(scene):
    srd_renderer.frame_complete()


class SRDRenderSettings(bpy.types.PropertyGroup):
    enable = bpy.props.BoolProperty(
        description="Save the render data to file at render.",
        name="Save Render Data",
        default=True
    )
    filename = bpy.props.StringProperty(
        description="Name of output file",
        name="File Name",
        default="render_settings.txt",
        subtype="FILE_NAME"
    )


class SRDRenderPanel(bpy.types.Panel):
    """Puts the panel in the render data section."""
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    bl_idname = 'RENDER_PT_SRD'
    bl_label = "Save Render Data"

    def draw_header(self, context):
        self.layout.prop(context.scene.srd_settings, "enable", text="")

    def draw(self, context):
        layout = self.layout
        layout.active = context.scene.srd_settings.enable
        layout.prop(context.scene.srd_settings, 'filename')

        cur_group = ''  # Keep track of our current group.

        split = layout.split()
        col1 = split.column()  # Left column
        col2 = split.column()  # Right column

        use_left = True  # Used for switching columns.
        for hook in SRDRenderer.get_hooks():
            if hook.is_valid_renderer(context):
                # Only check if the group has changed if the renderer is valid because some groups
                # are only valid for one renderer.
                if hook.hook_group != cur_group:
                    # The current hook has changed, add a new label and switch columns.
                    cur_group = hook.hook_group

                    # Grab either the left or the right column, then switch next time around.
                    col = col1 if use_left else col2
                    use_left = not use_left

                    # Add the group label.
                    col.separator()
                    col.label(SRDRenderer.get_group(cur_group)[0] + ':')

                col.prop(context.scene.srd_settings, hook.hook_idname)



def register():
    # Add handlers
    bpy.app.handlers.render_write.append(render_write)
    bpy.app.handlers.render_cancel.append(render_cancel)
    bpy.app.handlers.render_init.append(render_init)
    bpy.app.handlers.render_complete.append(render_complete)
    bpy.app.handlers.render_pre.append(render_pre)
    bpy.app.handlers.render_post.append(render_post)

    bpy.utils.register_class(SRDRenderPanel)
    bpy.utils.register_class(SRDRenderSettings)

    bpy.types.Scene.srd_settings = \
        bpy.props.PointerProperty(type=SRDRenderSettings)

    # Register the hooks.
    hooks.general.register()
    hooks.cycles.register()


def unregister():
    # # BEGIN DEBUG CODE ##
    bpy.utils.unregister_class(bpy.types.SRDRenderSettings)  # Unregister whatever is already registered.
    del bpy.types.Scene.srd_settings

    bpy.app.handlers.render_write.pop()
    bpy.app.handlers.render_cancel.pop()
    bpy.app.handlers.render_init.pop()
    bpy.app.handlers.render_complete.pop()
    bpy.app.handlers.render_pre.pop()
    bpy.app.handlers.render_post.pop()
    # # END DEBUG CODE ##

    # Remove handlers
    # bpy.app.handlers.render_write.remove(render_write)
    # bpy.app.handlers.render_cancel.remove(render_cancel)
    # bpy.app.handlers.render_init.remove(render_init)
    # bpy.app.handlers.render_complete.remove(render_complete)
    # bpy.app.handlers.render_pre.remove(render_complete)
    # bpy.app.handlers.render_post.remove(render_complete)


if __name__ == "__main__":
    try:
        unregister()
    finally:
        register()