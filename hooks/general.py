"""
hooks/general.py: General render independent hooks.

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


import time
import bpy
from scribe.renderer import RenderHook, register_hook, register_group


class RenderEngineHook(RenderHook):
    """Which render engine is used to render."""
    hook_label = 'Render engine'
    hook_idname = 'engine'

    def post_render(self):
        engine_id = self.scene.render.engine
        # The built in blender render and blender game are special cases.
        if engine_id == 'BLENDER_RENDER':
            return 'Blender Render'
        elif engine_id == 'BLENDER_GAME':
            return 'Blender Game'
        else:
            # First see if the render engine is registered with the class name the same as the bl_idname
            engine = getattr(bpy.types, engine_id, None)
            if engine is not None and engine.bl_idname == engine_id:
                return engine.bl_label
            else:
                # Find the render engine by looking through bpy.types (dirty but it works)
                for typ in dir(bpy.types):
                    engine = getattr(bpy.types, typ)
                    # If this type is a render engine and it has the same bl_idname than we found the right one.
                    if issubclass(engine, bpy.types.RenderEngine) and engine.bl_idname == engine_id:
                        return engine.bl_label


class TimeHook(RenderHook):
    """Total render time."""
    hook_label = 'Time'
    hook_idname = 'time'

    t = 0
    ft = 0
    peakframe = 0
    peaktime = 0

    def pre_render(self):
        self.t = time.time()

    def post_render(self):
        return '%.2fs(Peak: %.2fs on frame %s)' % (time.time() - self.t, self.peaktime, self.peakframe)

    def pre_frame(self):
        self.ft = time.time()

    def post_frame(self):
        frametime = time.time() - self.ft
        if frametime > self.peaktime:
            self.peaktime = frametime
            self.peakframe = self.scene.frame_current


class FrameRateHook(RenderHook):
    """Frame rate of the rendered animation."""
    hook_label = 'Frame Rate'
    hook_idname = 'fps'

    def post_render(self):
        return '%sfps' % self.scene.render.fps


class FrameRangeHook(RenderHook):
    """The output frame range."""
    hook_label = 'Frame Range'
    hook_idname = 'framerange'

    def post_render(self):
        start = self.scene.frame_start
        end = self.scene.frame_end
        return "%s - %s(Total Frames: %s)" % (start, end, end - (start-1))


### Resolution group
class ResolutionHook(RenderHook):
    """Target resolution."""
    hook_label = 'Resolution'
    hook_idname = 'resolution'
    hook_group = 'resolution'

    def post_render(self):
        x = self.scene.render.resolution_x
        y = self.scene.render.resolution_y
        return "%sx%spx" % (x, y)


class TrueResolutionHook(RenderHook):
    """Actual output resolution."""
    hook_label = 'True resolution'
    hook_idname = 'trueres'
    hook_group = 'resolution'

    def post_render(self):
        fac = self.scene.render.resolution_percentage / 100
        x = self.scene.render.resolution_x * fac
        y = self.scene.render.resolution_y * fac
        return "%sx%spx" % (x, y)


def register():
    # General.
    register_hook(RenderEngineHook)
    register_hook(TimeHook)
    register_hook(FrameRateHook)
    register_hook(FrameRangeHook)

    # Resolution group.
    register_group('resolution', 'Output Resolution')
    register_hook(ResolutionHook)
    register_hook(TrueResolutionHook)
