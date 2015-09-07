import time
from SRDRenderHook import SRDRenderHook
from SRDRenderer import SRDRenderer


class TimeHook(SRDRenderHook):
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

SRDRenderer.register_hook(TimeHook)


class FrameRateHook(SRDRenderHook):
    """Frame rate of the rendered animation."""
    hook_label = 'Frame Rate'
    hook_idname = 'fps'

    def post_render(self):
        return '%sfps' % self.scene.render.fps

SRDRenderer.register_hook(FrameRateHook)


class FrameRangeHook(SRDRenderHook):
    """The output frame range."""
    hook_label = 'Frame Range'
    hook_idname = 'framerange'

    def post_render(self):
        start = self.scene.frame_start
        end = self.scene.frame_end
        return "%s - %s(Total Frames: %s)" % (start, end, end - (start-1))

SRDRenderer.register_hook(FrameRangeHook)


### Resolution group
SRDRenderer.register_group('resolution', 'Output Resolution')


class ResolutionHook(SRDRenderHook):
    """Target resolution."""
    hook_label = 'Resolution'
    hook_idname = 'resolution'
    hook_group = 'resolution'

    def post_render(self):
        x = self.scene.render.resolution_x
        y = self.scene.render.resolution_y
        return "%sx%spx" % (x, y)

SRDRenderer.register_hook(ResolutionHook)


class TrueResolutionHook(SRDRenderHook):
    """Actual output resolution."""
    hook_label = 'True resolution'
    hook_idname = 'trueres'
    hook_group = 'resolution'

    def post_render(self):
        fac = self.scene.render.resolution_percentage / 100
        x = self.scene.render.resolution_x * fac
        y = self.scene.render.resolution_y * fac
        return "%sx%spx" % (x, y)

SRDRenderer.register_hook(TrueResolutionHook)