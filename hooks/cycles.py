import bpy

from SRDRenderHook import SRDRenderHook
from SRDRenderer import SRDRenderer

### Seed Group
class SeedHook(SRDRenderHook):
    """Cycles sampling seed."""
    hook_label = 'Seed'
    hook_idname = 'seed'
    hook_group = 'seed'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return str(self.scene.cycles.seed)


class SeedAnimatedHook(SRDRenderHook):
    """Weather or not the seed is animated from frame to frame."""
    hook_label = 'Seed is Animated'
    hook_idname = 'animated_seed'
    hook_group = 'seed'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return str(self.scene.cycles.use_animated_seed)


## Volume Sampling group
class VolumeStepHook(SRDRenderHook):
    """Cycles volume step size."""
    hook_label = 'Step Size'
    hook_idname = 'step_size'
    hook_group = 'vol_sample'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return str(self.scene.cycles.volume_step_size)


class VolumeStepMaxHook(SRDRenderHook):
    """Maximum number of cycles volume steps."""
    hook_label = 'Max Steps'
    hook_idname = 'step_max_size'
    hook_group = 'vol_sample'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return str(self.scene.cycles.volume_max_steps)


## Performance group.
class TileSizeHook(SRDRenderHook):
    """Tile size."""
    hook_label = 'Tile Size'
    hook_idname = 'tile_size'
    hook_group = 'perf'
    hook_render_engine = {'CYCLES', 'BLENDER_RENDER'}

    def post_render(self):
        return '%sx%s' % (self.scene.render.tile_x, self.scene.render.tile_y)


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


class ThreadsModeHook(SRDRenderHook):
    """Which scheme is used to determine the number of threads."""
    hook_label = 'Threads Mode'
    hook_idname = 'threads_mode'
    hook_group = 'perf'
    hook_render_engine = {'CYCLES', 'BLENDER_RENDER'}

    def post_render(self):
        return self.scene.render.threads_mode.capitalize()


class ThreadsHook(SRDRenderHook):
    """How many threads are being used to render."""
    hook_label = 'Threads'
    hook_idname = 'threads'
    hook_group = 'perf'
    hook_render_engine = {'CYCLES', 'BLENDER'}

    def post_render(self):
        return str(self.scene.render.threads)


## Light Paths group.
class LBMaxHook(SRDRenderHook):
    """Total Minimum number of reflection bounces."""
    hook_label = 'Total Max'
    hook_idname = 'lb_max'
    hook_group = 'light_bounces'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return str(self.scene.cycles.max_bounces)


class LBMinHook(SRDRenderHook):
    """Total Minimum number of reflection bounces."""
    hook_label = 'Total Min'
    hook_idname = 'lb_min'
    hook_group = 'light_bounces'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return str(self.scene.cycles.min_bounces)


class LBDiffuseHook(SRDRenderHook):
    """Maximum number of diffuse reflection bounces."""
    hook_label = 'Diffuse'
    hook_idname = 'lb_diffuse'
    hook_group = 'light_bounces'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return str(self.scene.cycles.diffuse_bounces)


class LBGlossyHook(SRDRenderHook):
    """Maximum number of glossy reflection bounces."""
    hook_label = 'Glossy'
    hook_idname = 'lb_glossy'
    hook_group = 'light_bounces'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return str(self.scene.cycles.glossy_bounces)


class LBTransHook(SRDRenderHook):
    """Maximum number of transmission reflection bounces."""
    hook_label = 'Transmission'
    hook_idname = 'lb_trans'
    hook_group = 'light_bounces'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return str(self.scene.cycles.transmission_bounces)


class LBVolumeHook(SRDRenderHook):
    """Maximum number of volume reflection bounces."""
    hook_label = 'Volume'
    hook_idname = 'lb_volume'
    hook_group = 'light_bounces'
    hook_render_engine = {'CYCLES'}

    def post_render(self):
        return str(self.scene.cycles.volume_bounces)


def register():
    # Seed group.
    SRDRenderer.register_group('seed', 'Seed')
    SRDRenderer.register_hook(SeedHook)
    SRDRenderer.register_hook(SeedAnimatedHook)

    # Volume sampling group.
    SRDRenderer.register_group('vol_sample', 'Volume Sampling')
    SRDRenderer.register_hook(VolumeStepHook)
    SRDRenderer.register_hook(VolumeStepMaxHook)

    # Performance group.
    SRDRenderer.register_group('perf', 'Performance')
    SRDRenderer.register_hook(TileSizeHook)
    SRDRenderer.register_hook(TileOrderHook)
    SRDRenderer.register_hook(ThreadsModeHook)
    SRDRenderer.register_hook(ThreadsHook)

    # Light Paths group.
    SRDRenderer.register_group('light_bounces', 'Bounces')
    SRDRenderer.register_hook(LBMaxHook)
    SRDRenderer.register_hook(LBMinHook)
    SRDRenderer.register_hook(LBDiffuseHook)
    SRDRenderer.register_hook(LBGlossyHook)
    SRDRenderer.register_hook(LBTransHook)
    SRDRenderer.register_hook(LBVolumeHook)
