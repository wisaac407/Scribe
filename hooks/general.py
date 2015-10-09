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
from ..ScribeRenderHook import ScribeRenderHook
from ..ScribeRenderer import ScribeRenderer


class TimeHook(ScribeRenderHook):
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


class FrameRateHook(ScribeRenderHook):
    """Frame rate of the rendered animation."""
    hook_label = 'Frame Rate'
    hook_idname = 'fps'

    def post_render(self):
        return '%sfps' % self.scene.render.fps


class FrameRangeHook(ScribeRenderHook):
    """The output frame range."""
    hook_label = 'Frame Range'
    hook_idname = 'framerange'

    def post_render(self):
        start = self.scene.frame_start
        end = self.scene.frame_end
        return "%s - %s(Total Frames: %s)" % (start, end, end - (start-1))


### Resolution group
class ResolutionHook(ScribeRenderHook):
    """Target resolution."""
    hook_label = 'Resolution'
    hook_idname = 'resolution'
    hook_group = 'resolution'

    def post_render(self):
        x = self.scene.render.resolution_x
        y = self.scene.render.resolution_y
        return "%sx%spx" % (x, y)


class TrueResolutionHook(ScribeRenderHook):
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
    ScribeRenderer.register_hook(TimeHook)
    ScribeRenderer.register_hook(FrameRateHook)
    ScribeRenderer.register_hook(FrameRangeHook)

    # Resolution group.
    ScribeRenderer.register_group('resolution', 'Output Resolution')
    ScribeRenderer.register_hook(ResolutionHook)
    ScribeRenderer.register_hook(TrueResolutionHook)