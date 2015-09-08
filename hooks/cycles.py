import bpy

from SRDRenderHook import SRDRenderHook
from SRDRenderer import SRDRenderer

### Seed Group
SRDRenderer.register_group('seed', 'Seed')


class SeedHook(SRDRenderHook):
    """Cycles sampling seed."""
    hook_label = 'Seed'
    hook_idname = 'seed'
    hook_group = 'seed'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return str(self.scene.cycles.seed)

SRDRenderer.register_hook(SeedHook)


class SeedAnimatedHook(SRDRenderHook):
    """Weather or not the seed is animated from frame to frame."""
    hook_label = 'Seed is Animated'
    hook_idname = 'animated_seed'
    hook_group = 'seed'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return str(self.scene.cycles.use_animated_seed)

SRDRenderer.register_hook(SeedAnimatedHook)


## Volume Sampling group
SRDRenderer.register_group('vol_sample', 'Volume Sampling')


class VolumeStepHook(SRDRenderHook):
    """Cycles volume step size."""
    hook_label = 'Step Size'
    hook_idname = 'step_size'
    hook_group = 'vol_sample'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return str(self.scene.cycles.volume_step_size)

SRDRenderer.register_hook(VolumeStepHook)


class VolumeStepMaxHook(SRDRenderHook):
    """Maximum number of cycles volume steps."""
    hook_label = 'Max Steps'
    hook_idname = 'step_max_size'
    hook_group = 'vol_sample'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return str(self.scene.cycles.volume_max_steps)

SRDRenderer.register_hook(VolumeStepMaxHook)


## Performance group.
SRDRenderer.register_group('perf', 'Performance')


class TileSizeHook(SRDRenderHook):
    """Tile size."""
    hook_label = 'Tile Size'
    hook_idname = 'tile_size'
    hook_group = 'perf'
    hook_render_engine = {'CYCLES', 'BLENDER_RENDER'}

    def post_render(self):
        return '%sx%s' % (self.scene.render.tile_x, self.scene.render.tile_y)

SRDRenderer.register_hook(TileSizeHook)


class TileOrderHook(SRDRenderHook):
    """Cycles tile order."""
    hook_label = 'Tile Order'
    hook_idname = 'tile_order'
    hook_group = 'perf'
    hook_render_engine = {'CYCLES', 'BLENDER_RENDER'}

    # Dictionary mapping order idname -> order label. i.e. {'CENTER': 'center'}
    orders = dict((idname, label) for idname, label, _ in
        bpy.types.CyclesRenderSettings.tile_order[1]['items'])

    def post_render(self):
        return self.orders[self.scene.cycles.tile_order]

SRDRenderer.register_hook(TileOrderHook)


class ThreadsModeHook(SRDRenderHook):
    """Which scheme is used to determine the number of threads."""
    hook_label = 'Threads Mode'
    hook_idname = 'threads_mode'
    hook_group = 'perf'
    hook_render_engine = {'CYCLES', 'BLENDER_RENDER'}

    def post_render(self):
        return self.scene.render.threads_mode.capitalize()

SRDRenderer.register_hook(ThreadsModeHook)


class ThreadsHook(SRDRenderHook):
    """How many threads are being used to render."""
    hook_label = 'Threads'
    hook_idname = 'threads'
    hook_group = 'perf'
    hook_render_engine = {'CYCLES', 'BLENDER'}

    def post_render(self):
        return str(self.scene.render.threads)

SRDRenderer.register_hook(ThreadsHook)